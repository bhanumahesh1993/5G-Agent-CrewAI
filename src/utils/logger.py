import logging
import sys
import os
from datetime import datetime

def setup_logger(name='modem_intelligence', log_file=None, level=logging.INFO):
    """
    Set up a logger with console and optional file output.
    
    Args:
        name (str, optional): Logger name
        log_file (str, optional): Path to log file
        level (int, optional): Logging level
        
    Returns:
        logging.Logger: Configured logger
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers if any
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Create file handler if log file specified
    if log_file:
        # Ensure log directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_default_log_file():
    """
    Get a default log file name based on current timestamp.
    
    Returns:
        str: Default log file path
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = "logs"
    
    # Ensure log directory exists
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    return os.path.join(log_dir, f"modem_analysis_{timestamp}.log")
