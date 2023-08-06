from tradingBot.jobs import core
from tradingBot.admin.site import site
from tradingBot.consts import strategy 

import logging

DEFAULT_SITE_STRATEGY = [strategy.CREDIT_PUT_SPREAD, strategy.CREDIT_IRON_CONDOR]


class refresh_monitorlist():
    def __init__(self, site_name):     
        self.site_name = site_name
        self.logger = logging.getLogger(__name__)        
        return
    
    def execute(self):
        with site(self.site_name, DEFAULT_SITE_STRATEGY) as mysite:
            mysite.refresh_site_monitor_list()     

        return
    
