# configure log format
import logging

"""
setup logger for healthcare application
"""
def setup_logger():
    """
    create logger for healthcare application
    """
    logger = logging.getLogger('healthcare_logger')
    logger.setLevel(logging.DEBUG)

    # check if logger already has handlers to avoid duplicate logs
    if logger.hasHandlers():
        return logger

    # create file handler to write logs to a healthcare.log file
    file_handler = logging.FileHandler('healthcare.log')
    file_handler.setLevel(logging.DEBUG)

    # create formatter to specify log message format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger