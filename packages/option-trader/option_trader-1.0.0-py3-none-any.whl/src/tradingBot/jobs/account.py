
#import sys

#sys.path.append(r'\Users\jimhu\option_trader\src')
    

from tradingBot.jobs import core
from tradingBot.admin.site    import site
from tradingBot.admin.user    import user
from tradingBot.admin.account import account

from tradingBot.utils.dataGetter import afterHours

import logging


from tradingBot.settings import app_settings    


class update_position():

    def __init__(self, site_name, user_name, account_name):     
        self.site_name = site_name
        self.user_name = user_name
        self.account_name = account_name        
        return
    
    def execute(self):

        #if afterHours():
        #    logger.info('After hours')
        #    return
        
        with site(self.site_name) as mysite:
            with user(user_name=self.user_name, site=mysite) as this_user:
                with account(this_user, self.account_name) as this_account:
                    this_account.update_position()
                    #this_account.try_open_new_strategy_positions()
        return


class trade():


    def __init__(self, site_name, user_name, account_name):     
        self.site_name = site_name
        self.user_name = user_name
        self.account_name = account_name        
        return
    
    def execute(self):

        #if afterHours():
        #    logger.info('After hours')
        #    return
        
        with site(self.site_name) as mysite:
            with user(user_name=self.user_name, site=mysite) as this_user:
                with account(this_user, self.account_name) as this_account:
                    this_account.try_open_new_strategy_positions()
                                        
        return


if __name__ == '__main__':
    
    from logging.handlers import RotatingFileHandler
    
    FORMAT = '%(asctime)s-%(levelname)s (%(message)s) %(filename)s-%(lineno)s-%(funcName)s'
        
    ch = logging.StreamHandler()    
    #ch.setFormatter(formatter)

    import os

    if os.path.exists(app_settings.LOG_ROOT_DIR) == False:        
        os.mkdir(app_settings.LOG_ROOT_DIR)

    import datetime    
    daily_log_path = app_settings.LOG_ROOT_DIR+'\\my_log-'+datetime.date.today().strftime("%Y-%m-%d")+'.log'
    fh = RotatingFileHandler(daily_log_path)
    #fh.setFormatter(formatter)

    logging.basicConfig(
                level=logging.INFO,
                format=FORMAT,
                handlers=[ch, fh]
            )

    logger = logging.getLogger(__name__)

    # Filter paramiko.transport debug and info from basic logging configuration
    logging.getLogger('urllib3.connectionpool').setLevel(logging.WARN)

    logging.getLogger('yfinance').setLevel(logging.WARN)


    #logger.debug('processing single')
    #t =  trade('mysite', 'jihuang', 'single')
    #t.execute()

    #print('processing spread')    
    #t=  trade('mysite', 'jihuang', 'spread')
    #t.execute()

    #print('processing iron_condor')
    #t =  trade('mysite', 'jihuang', 'iron_condor')
    #t.execute()

    #print('processing butterfly')
    #t =  trade('mysite', 'jihuang', 'butterfly')
    #t.execute()

    print('processing single')
    t =  update_position('mysite', 'jihuang', 'single')
    t.execute()

    print('processing spread')    
    t=  update_position('mysite', 'jihuang', 'spread')
    t.execute()

    print('processing iron_condor')
    t =  update_position('mysite', 'jihuang', 'iron_condor')
    t.execute()

    #print('processing butterfly')
    #t =  update_position('mysite', 'jihuang', 'butterfly')
    #t.execute()
