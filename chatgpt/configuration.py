import ruamel.yaml

# Load the YAML configuration from the file
config_file_path = "borgmatic_config.yml"  # Replace with your YAML configuration file path
with open(config_file_path, "r") as config_file:
    config = ruamel.yaml.safe_load(config_file)

# Extract the relevant configuration values
source_directories = config.get("source_directories", [])
repositories = config.get("repositories", [])
keep_daily = config.get("keep_daily", 7)
keep_weekly = config.get("keep_weekly", 4)
keep_monthly = config.get("keep_monthly", 6)
before_backup = config.get("before_backup", [])
postgresql_databases = config.get("postgresql_databases", [])
healthchecks = config.get("healthchecks", {})

# Now, you can use these configuration values in your script as needed.
# For example, you can set your existing Python constants like this:
BORG_REPOSITORIES_BASE = repositories[0].get("path", "")
ARCHIVE_NAME = time.strftime('%Y-%m-%d_%H-%M-%S')
# And so on...

# Use these configuration values in your backup logic as required.
