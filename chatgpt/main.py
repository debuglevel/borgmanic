#!/usr/bin/env python3
import subprocess

# metric = Metric("weather")
# metric.with_timestamp(1465839830100400200)
# metric.add_tag('location', 'Cracow')
# metric.add_value('temperature', '29')
# print(metric)


# Constants
instance = "default"
BORG_REPOSITORIES_BASE = "/path/to/repositories/base"  # Adjust this
BORG_LOCAL_EXECUTABLE = "/path/to/borg/local"  # Adjust this
BORG_REMOTE_EXECUTABLE = "ssh user@remote /path/to/borg/remote"  # Adjust this
BORG_UPLOAD_RATELIMIT = "1000"  # Adjust this
BORG_COMPRESSION = "lz4"  # Adjust this
SOURCE_DIRECTORIES = "/path/to/source/directory"  # Adjust this
ARCHIVE_NAME = "backup_archive"  # Adjust this
LOG_DIRECTORY = "/path/to/log/directory"  # Adjust this

import os

# Load common configurations from credentials.sh
source
credentials.sh  # Note: This is just a reference to the Bash script. You can't directly source it in Python.

# Define Python variables
BORG_REMOTE_EXECUTABLE = "borg-1.2"
BORG_LOCK_WAIT = 600
RELATIVE_REPOSITORIES_PATH = "./BorgBackup"
BORG_REPOSITORIES_BASE = f"ssh://{SSH_USER}@{SSH_HOST}:{SSH_PORT}/{RELATIVE_REPOSITORIES_PATH}"
ARCHIVE_NAME = time.strftime('%Y-%m-%d_%H-%M-%S')
BORG_LOCAL_EXECUTABLE = "borg"  # You can adjust this as needed

# Now, you can use these Python variables in your script as you would use environment variables in Bash.

# General StorageBox credentials
USER = "u253621-sub3"
PASSWORD = "asdsdasda"
HOST = f"{USER}.your-storagebox.de"
SUBDOMAIN = USER  # The subdomain seems to be always the same as the USER (or is an alias or just does not matter)

SSH_USER = USER
SSH_PASSWORD = PASSWORD
SSH_KEY = "/_deployment/backup/StorageBox/u253621-sub3_automatic-backup.ed25519"
SSH_HOST = HOST
SSH_PORT = 23

# In case you need to use an SSH jumphost
SSH_JUMPHOST_HOST = "basdsdasdadsadsda.de"
SSH_JUMPHOST_USER = "marc"
SSH_JUMPHOST = f"{SSH_JUMPHOST_USER}@{SSH_JUMPHOST_HOST}"

# Import the common credentials
source
credentials.sh  # This is just a reference to the Bash script. You can't directly source it in Python.

# Define host-specific configurations
BORG_RSH = f"ssh -J {SSH_JUMPHOST}"  # ENV is picked up by borg

LOG_DIRECTORY = "/c/Logs/borg/"

# Network upload rate limit (for each instance) in kiByte/s; use 0 for unlimited.
BORG_UPLOAD_RATELIMIT = 2000
BORG_COMPRESSION = "auto,zstd,5"

# Define instance-specific configurations
BORG_REPOSITORY = f"{BORG_REPOSITORIES_BASE}/vasdsdasdam"
BORG_PASSPHRASE = "dfsdfsdfdsfsd"  # ENV is picked up by borg

# Note: It's best to use the original SSH_KEY defined earlier, as it's common to all instances on this host.
# However, if you need a specific SSH key for this instance, you can define it here.
# SSH_KEY = "vmhost.corp-network.avm_id_ed25519"

SOURCE_DIRECTORIES = "/d/HyperV-Export/"


# Functions
def run_command(command, log_file):
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
                                text=True)
        log_file.write(result.stdout)
        return result.returncode
    except subprocess.CalledProcessError as e:
        log_file.write(e.stdout)
        log_file.write(e.stderr)
        return e.returncode


def main():
    log_file_path = os.path.join(LOG_DIRECTORY, f"create-backup-{instance}.log")

    with open(log_file_path, "w") as log_file:
        log_file.write("Starting backup...\n")

        # Check if needed tools are installed
        tools = ["jq", BORG_LOCAL_EXECUTABLE, "ssh-agent", "tee"]

        for tool in tools:
            if run_command(f"command -v {tool}", log_file) != 0:
                log_file.write(f"{tool} is not installed\n")
                return

        # Set up ssh-agent
        run_command("eval $(ssh-agent)", log_file)
        run_command(f"cat {SSH_KEY} | ssh-add", log_file)

        # Create backup
        command = f"{BORG_LOCAL_EXECUTABLE} create " \
                  f"--verbose --stats --progress --list --filter=ACEM " \
                  f"--log-json --json " \
                  f"--remote-path={BORG_REMOTE_EXECUTABLE} " \
                  f"--upload-ratelimit {BORG_UPLOAD_RATELIMIT} " \
                  f"--compression {BORG_COMPRESSION} " \
                  f"{BORG_REPOSITORIES_BASE}::{ARCHIVE_NAME} " \
                  f"{SOURCE_DIRECTORIES}"

        borg_rc = run_command(command, log_file)

        log_file.write(f"borg returned with exit code {borg_rc}\n")

        if borg_rc == 0:
            log_file.write(f"borg returned with success exit code; see log file '{BORG_ERROR_LOG_FILE}' for details.\n")
        elif borg_rc == 1:
            log_file.write(f"borg returned with warning exit code; see log file '{BORG_ERROR_LOG_FILE}' for details.\n")
        elif borg_rc > 1:
            log_file.write(f"borg returned with error exit code; see log file '{BORG_ERROR_LOG_FILE}' for details.\n")

        # Cleanup
        run_command("ssh-agent -k", log_file)

    log_file.write("Backup completed.\n")


if __name__ == "__main__":
    main()
