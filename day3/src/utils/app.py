import sys
import os
 
#add project root tp python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
sys.path.append(project_root)
 
from conf.logger_conf import setup_logger
"""
entry point for the healthcare application
"""
logger = setup_logger()
 
def run_app():
    """
    run the healthcare application
    """
    logger.info("app run")
   
    #handle entry point
if __name__ == "__main__":
    run_app()