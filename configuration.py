import logging.config

import ruamel.yaml

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def load(filepath):
    """Returns the borgmatic-like config.yaml"""
    with open(filepath, "r") as config_file:
        config = ruamel.yaml.safe_load(config_file)
        return config


def print(config):
    logger.debug("Printing configuration...")

    logger.debug(f"  instance: {instance}")

    logger.debug(f"  log directory: {LOG_DIRECTORY}")
    logger.debug(f"  borg temporary json log file: {BORG_TEMP_JSON_LOG_FILE}")
    logger.debug(f"  borg json log file: {BORG_JSON_LOG_FILE}")
    logger.debug(f"  borg error log file: {BORG_ERROR_LOG_FILE}")
    logger.debug(f"  bashlog log file: {BASHLOG_JSON_FILE_PATH}")

    logger.debug(f"  ssh key: {SSH_KEY}")

    logger.debug(f"  source directories: {SOURCE_DIRECTORIES}")

    logger.debug(f"  repository base: {BORG_REPOSITORIES_BASE}")
    logger.debug(f"  repository: {BORG_REPOSITORY}")
    logger.debug(f"  archive name: {ARCHIVE_NAME}")

    logger.debug(f"  local executable: {BORG_LOCAL_EXECUTABLE}")
    logger.debug(f"  remote executable: {BORG_REMOTE_EXECUTABLE}")
    logger.debug(f"  remote shell command: {BORG_RSH}")
    logger.debug(f"  upload rate: {BORG_UPLOAD_RATELIMIT}")
    logger.debug(f"  compression: {BORG_COMPRESSION}")
