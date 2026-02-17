import logging
import sys
import os

def setup_logging():
    """Configures logging to both console and file."""
    log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    
    # Ensure log file is in a writable location
    log_file = "app.log"
    
    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logging.info("Logging initialized. Outputting to console and app.log")

def get_logger(name):
    return logging.getLogger(name)
