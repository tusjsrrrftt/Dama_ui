import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

def setup_logging(log_level=logging.INFO):
    """
    Set up logging for the Dama UI application.

    This function configures logging to output to both console and a file.
    The log file is stored in a 'logs' directory within the application's root directory.

    :param log_level: The logging level to use (default: logging.INFO)
    """
    # Create a logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Generate a filename based on the current date
    log_filename = f"dama_ui_{datetime.now().strftime('%Y-%m-%d')}.log"
    log_filepath = os.path.join(log_dir, log_filename)

    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = RotatingFileHandler(
        log_filepath, maxBytes=10*1024*1024, backupCount=5
    )

    # Create formatters and add it to handlers
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.info("Logging setup complete.")

def get_logger(name):
    """
    Get a logger with the specified name.

    :param name: The name of the logger (usually __name__)
    :return: A logger instance
    """
    return logging.getLogger(name)

# Example usage and testing
if __name__ == "__main__":
    setup_logging(logging.DEBUG)
    logger = get_logger(__name__)

    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    print(f"Log file should be created in: {os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')}")