import os
import sys

import logging

# Set up logging
log_level = logging.DEBUG if 'BASHLOG_DEBUG' in os.environ and os.environ['BASHLOG_DEBUG'] == '1' else logging.INFO
log_format = '%(asctime)s [%(levelname)s] %(message)s'

# Define log file paths
log_file_path = os.environ.get('BASHLOG_FILE_PATH', f'/tmp/{os.path.basename(sys.argv[0])}.log')
json_log_file_path = os.environ.get('BASHLOG_JSON_FILE_PATH', f'/tmp/{os.path.basename(sys.argv[0])}.log.json')

logger = logging.getLogger('bashlog')
logger.setLevel(log_level)

# Create a file handler
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(log_level)

# Create a JSON file handler
json_file_handler = logging.FileHandler(json_log_file_path)
json_file_handler.setLevel(log_level)

# Create a console handler with a higher log level
console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)

# Create a formatter
formatter = logging.Formatter(log_format)

# Set the formatter for the handlers
file_handler.setFormatter(formatter)
json_file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(json_file_handler)
logger.addHandler(console_handler)

# Define a mapping of log levels from Bash to Python
log_level_mapping = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARN': logging.WARNING,
    'ERROR': logging.ERROR
}


def log(level, message):
    if level in log_level_mapping:
        logger.log(log_level_mapping[level], message)
    else:
        logger.error(f"Undefined log level trying to log: {message}")


def _log_exception(*args):
    log('error', f"Logging Exception: {' '.join(map(str, args))}")


def set_debug(debug_level):
    os.environ['BASHLOG_DEBUG'] = '1' if debug_level > 0 else '0'


def set_log_file(file_path):
    os.environ['BASHLOG_FILE'] = '1'
    os.environ['BASHLOG_FILE_PATH'] = file_path


def set_json_log(json_log):
    os.environ['BASHLOG_JSON_FILE'] = '1'
    os.environ['BASHLOG_JSON_FILE_PATH'] = json_log
