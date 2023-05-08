from loguru import logger
import os
import sys

LOG_FILE = "translation.log"
ROTATION_TIME = "02:00"

class Logger:
    def __init__(self, name="translation", log_dir="logs", debug=False):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file_path = os.path.join(log_dir, LOG_FILE)

        # Remove default loguru handler
        logger.remove()

        # Add console handler with a specific log level
        level = "DEBUG" if debug else "INFO"
        console_format = '[{level}][{time:YYYY-MM-DD HH:mm:ss}][{module}] {message}'
        logger.add(sys.stdout, level=level, format=console_format)

        # Add file handler with a specific log level and timed rotation
        file_format = '[{level}][{time:YYYY-MM-DD HH:mm:ss}][{module}] {message}'
        logger.add(log_file_path, rotation=ROTATION_TIME, level="DEBUG", format=file_format)

        self.logger = logger

LOG = Logger().logger

if __name__ == "__main__":
    log = Logger().logger

    log.debug("This is a debug message.")
    log.info("This is an info message.")
    log.warning("This is a warning message.")
    log.error("This is an error message.")
