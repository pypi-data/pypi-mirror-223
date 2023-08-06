
from logging.handlers import RotatingFileHandler

from django.conf import settings
import sys
sys.path.append(settings.TRADINGBOT_HOME_DIR)

import warnings
import logging

warnings.filterwarnings('ignore')                 

FORMAT = '%(asctime)s-%(levelname)s (%(message)s) %(filename)s-%(lineno)s-%(funcName)s'
    
ch = logging.StreamHandler()    

import os

if os.path.exists(settings.DATA_ROOT_DIR) == False:        
    os.mkdir(settings.DATA_ROOT_DIR)

if os.path.exists(settings.LOG_ROOT_DIR) == False:        
    os.mkdir(settings.LOG_ROOT_DIR)

if os.path.exists(settings.CHART_ROOT_DIR) == False:        
    os.mkdir(settings.CHART_ROOT_DIR)

if os.path.exists(settings.USER_ROOT_DIR) == False:        
    os.mkdir(settings.USER_ROOT_DIR)

import datetime    

daily_log_path = settings.LOG_ROOT_DIR+'/service_log-'+datetime.date.today().strftime("%Y-%m-%d")+'.log'

fh = RotatingFileHandler(daily_log_path)
#fh.setFormatter(formatter)

logging.basicConfig(
            level=logging.INFO,
            format=FORMAT,
            handlers=[ch, fh]
        )

logger = logging.getLogger(__name__)

# Filter paramiko.transport debug and info from basic logging configuration
logging.getLogger('yfinance').setLevel(logging.WARNING)
logging.getLogger('PIL').setLevel(logging.WARNING)    
logging.getLogger('urllib3').setLevel(logging.WARNING)               
logging.getLogger('matplotlib').setLevel(logging.WARNING)    


import sys

sys.path.append(settings.TRADINGBOT_HOME_DIR)