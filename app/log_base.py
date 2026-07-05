import logging

# creates new log files based on the size specified
from logging.handlers import RotatingFileHandler

#  for daily log rotation and setting it up to keep logs for n (10) days, and appending the date to the log file name.
from logging.handlers import TimedRotatingFileHandler

from app.utils.filters import RequestIDFilter


class SafeRotatingFileHandler(RotatingFileHandler):
    """
    RotatingFileHandler that tolerates rollover failures.

    On Windows, when more than one process holds the log file open (e.g.
    ``uvicorn --reload`` runs a reloader process plus a worker, or multiple
    workers share one log path), the rename performed during rollover raises
    ``PermissionError: [WinError 32]``. The stock handler turns that into a
    noisy traceback on every rollover attempt. Here we swallow it and keep
    logging to the current file, retrying rotation on a later record.
    """

    def doRollover(self):  # noqa: D102 - see class docstring
        try:
            super().doRollover()
        except OSError:
            # Another process owns the file (PermissionError is an OSError);
            # skip this rotation. Reopen the
            # stream (the base implementation closes it before renaming) so
            # logging continues uninterrupted.
            if not self.stream:
                self.stream = self._open()


def get_logger(name):
    """
    Create and configure a logger.

    This function sets up a logger with both file and console handlers. The logger
    will log messages to a file and also print them to the console.

    Parameters
    ----------
    name : str
        The name of the logger.

    Returns
    -------
    logging.Logger
        Configured logger instance.

    Examples
    --------
    >>> logger = get_logger("my_logger")
    >>> logger.info("This is an info message.")
    2024-07-08 10:00:00,000 - my_logger - MainThread -  <module>() - INFO - Line Number : 45: - This is an info message.

    In the log file 'python-agent-definition-service.log':
    2024-07-08 10:00:00,000 - my_logger - MainThread -  <module>() - INFO - Line Number : 45: - This is an info message.

    Working Explained
    --------
    The RotatingFileHandler creates new log files based on the size specified (5 MB in this case). The log rotation does not strictly adhere to a daily rotation but rather triggers when the log file reaches the specified size limit. The backupCount parameter determines how many old log files to keep.

    Here's how it works:

    Size-Based Rotation: When the current log file reaches the size limit (5 MB), a new log file is created.
    Backup Count: If backupCount is 10, up to 10 backup files are maintained. Once the number of log files exceeds this limit, the oldest log files are deleted.
    For instance:

    If you log 10 MB in one day, you will have two log files (python-agent-definition-service.log and python-agent-definition-service.log.1).
    If logging continues and you surpass the 5 MB limit again, a third file is created (python-agent-definition-service.log.2), and so on, up to the 10th backup.
    Once you reach the 11th file, the first log file (python-agent-definition-service.log.1) will be deleted to make space for the new log file.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # Set the overall logging level for the logger

    # Avoid adding duplicate handlers if the logger already has handlers
    if not logger.handlers:
        # File handler with rotation (tolerant of multi-process rollover on Windows)
        file_handler = SafeRotatingFileHandler(
            "python-agent-definition-service.log",
            maxBytes=5 * 1024 * 1024,
            backupCount=10,
            encoding="utf-8",
            delay=True,
        )
        file_handler.setLevel(logging.INFO)

        file_formatter = logging.Formatter(
            "RequestID: %(request_id)s - %(asctime)s - %(name)s - %(threadName)s - %(funcName)s() - %(levelname)s - Line Number : %(lineno)d: - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        console_formatter = logging.Formatter(
            "RequestID: %(request_id)s - %(asctime)s - %(name)s - %(threadName)s - %(funcName)s() - %(levelname)s - Line Number : %(lineno)d: - %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        """
        This module adds a custom logging filter to automatically include the request ID in all log messages.

        Steps:
        1. Add the custom filter:
        - The custom filter (`RequestIDFilter`) is configured and added to the logger to handle request-specific logging.
        
        2. Accessing Request ID in Log Messages:
        - The `RequestIDFilter` automatically appends the `g.request_id` to every log message.
        - This eliminates the need to manually include the request ID in each logging statement.

        3. Log Messages:
        - All log messages generated in route handlers or any other part of the application will include the request ID, ensuring consistent tracking and correlation of logs across requests.
        """
        logger.addFilter(RequestIDFilter())
    return logger
