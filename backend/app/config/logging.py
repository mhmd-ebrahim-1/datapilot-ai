import logging
import sys

def setup_logging(app_env: str):
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    if app_env == "production":
        log_format = '{"time": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}'
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[logging.StreamHandler(sys.stdout)]
    )
