
from tradingBot.jobs import core

from tradingBot.settings.tradeConfig import entryCrit, riskManager, marketCondition, runtimeConfig
from tradingBot.excel import accountBook as xlwings_wb
from tradingBot.panda import accountBook as panda_wb
from tradingBot.utils.dataGetter import afterHours

import pandas as pd

import logging

logger = logging.getLogger('account_place_orders_job')

class account_place_orders_job(core.core):
    def __init__(self, 
                 target_path=None,                 
                 use_panda=False):
        
        super().__init__()  
 
        self.target_path = target_path
        self.use_panda = use_panda

    def execute(self):

        if self.use_panda:
            accountBook = panda_wb.accountBook(file_path=self.target_path)          

        else:
            accountBook = xlwings_wb.accountBook(file_path=self.target_path)          

        accountBook.submit_all_opened_strategy_orders()  

        return