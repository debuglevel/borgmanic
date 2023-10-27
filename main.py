#!/usr/bin/env python3

import logging.config
import shutil
import subprocess
import sys

import configuration
import metrics

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# def stop_ssh_agent():
#     print("Stopping ssh-agent...")
#
#     # Use the `ssh-agent -k` command to kill the running ssh-agent
#     subprocess.run(["ssh-agent", "-k"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


# def start_ssh_agent():
#     logger.debug("Starting ssh-agent...")
#
#     # Start the ssh-agent
#     ssh_agent_process = subprocess.Popen(["ssh-agent"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#     ssh_agent_output, _ = ssh_agent_process.communicate()
#
#     # Extract the SSH_AUTH_SOCK and SSH_AGENT_PID from ssh-agent's output
#     for line in ssh_agent_output.splitlines():
#         if line.startswith("export SSH_AUTH_SOCK="):
#             ssh_auth_sock = line.replace("export SSH_AUTH_SOCK=", "")
#             os.environ["SSH_AUTH_SOCK"] = ssh_auth_sock
#         elif line.startswith("export SSH_AGENT_PID="):
#             ssh_agent_pid = line.replace("export SSH_AGENT_PID=", "")
#             os.environ["SSH_AGENT_PID"] = ssh_agent_pid
#
#     # Add the SSH key to the agent
#     ssh_add_process = subprocess.Popen(["ssh-add", SSH_KEY], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#     _, ssh_add_error = ssh_add_process.communicate()
#
#     if ssh_add_process.returncode != 0:
#         print("Error adding SSH key to ssh-agent:", ssh_add_error)


def is_tool_installed(tool):
    """Check whether `name` is on PATH and marked as executable."""
    logger.debug(f"Checking if {tool} is installed...")
    result = shutil.which(tool) is not None
    logger.debug(f"Checked if {tool} is installed: {result}
    return result


def check_tools():
    logger.debug("Checking if needed tools are installed...")

    tools = [
        "jq",
        "borg",
        "ssh-agent",
        "tee",
    ]

    for tool in tools:
        if not is_tool_installed(tool):
            logger.error(f"{tool} is not installed (running 'msys2-setup-borg.sh' might help)")
            sys.exit(1)


def usage():
    if len(sys.argv) != 2:
        print("Usage: {} <instance>".format(sys.argv[0]))
        print(
            "  where <instance> defines the name of the configuration file in this scheme: configuration-<instance>.yaml")
        sys.exit(1)


def create_archive_name():
    import datetime
    import socket

    hostname = socket.gethostname()
    now = datetime.datetime.now()
    formatted_string = f"{hostname}-{now.strftime('%Y-%m-%dT%H:%M:%S.%f')}"
    return formatted_string


def create_backup(config):
    logger.info("Creating backup...")

    borg_local_executable = config.get("local_path", "borg")
    borg_remote_executable = config.get("remote_path", "borg")
    borg_upload_ratelimit = config.get("upload_rate_limit", "0")
    borg_compression = config.get("compression", "lz4")
    borg_ssh_command = config.get("ssh_command", "ssh")
    borg_source_directories = config.get("source_directories", [])
    borg_repositories = config.get("repositories", [])
    borg_lock_wait = config.get("lock_wait", 1)
    borg_relocated_repo_access_is_ok = config.get("relocated_repo_access_is_ok", False)
    borg_keep_within = config.get("keep_within", "48H")
    borg_keep_secondly = config.get("keep_secondly", 60)
    borg_keep_minutely = config.get("keep_minutely", 60)
    borg_keep_hourly = config.get("keep_hourly", 24)
    borg_keep_daily = config.get("keep_daily", 7)
    borg_keep_weekly = config.get("keep_weekly", 4)
    borg_keep_monthly = config.get("keep_monthly", 12)
    borg_keep_yearly = config.get("keep_yearly", 2)
    archive_name = create_archive_name()

    # TODO: actually, we only support one repository at the moment.
    for repository in borg_repositories:
        borg_repository = repository.get("path", None)

        if borg_repository is None:
            logger.error("Repository path is not defined")
            sys.exit(1)

        command = [
            borg_local_executable,
            "create",
            "--verbose",
            "--stats",
            "--progress",
            "--list",
            "--filter=ACEM",
            "--log-json",
            "--json",
            f"--remote-path={borg_remote_executable}",
            f"--upload-ratelimit={borg_upload_ratelimit}",
            f"--compression={borg_compression}",
            f"{borg_repository}::{archive_name}"
        ]
        command.extend(borg_source_directories)

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate()  # TODO: Probably waits until finished, would be nicer if we could redirect in into a file so we can watch it.
            # TODO: Put stdout into json log file

            borg_json = stdout

            borg_rc = process.returncode
            logger.debug(f"borg return code: {borg_rc}")

            if borg_rc == 0:
                logger.debug(f"borg returned with success exit code; see log file for details.")
            elif borg_rc == 1:
                logger.warning(f"borg returned with warning exit code; see log file for details.")
            elif borg_rc > 1:
                logger.error(f"borg returned with error exit code; see log file for details.")

            import json
            borg_data = json.loads(borg_json)

            data = {
                "borg_rc": borg_rc,
                "borg_data": borg_data
            }

            return data
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    logger.info("Starting borgmanic...")

    usage()
    instance = sys.argv[1]

    config = configuration.load(f"configuration-{instance}.yaml")
    configuration.print(config)

    check_tools()

    # start_ssh_agent()

    borg_data = create_backup(config)

    # stop_ssh_agent()

    metrics.write(borg_data)
