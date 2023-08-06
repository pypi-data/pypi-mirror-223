
from tradingBot.jobs import core

from tradingBot.settings.tradeConfig import entryCrit, riskManager, marketCondition, runtimeConfig
from tradingBot.excel import accountBook as xlwings_wb
from tradingBot.panda import accountBook as panda_wb
from tradingBot.excel import watchListBook as wb
from tradingBot.utils.dataGetter import afterHours

import pandas as pd

import logging

logger = logging.getLogger('account_create_job')

class account_create_job(core.core):
    def __init__(self, 
                 target_path=None,                 
                 watchlist= pd.DataFrame(), 
                 strategy_list=[],                  
                 entry_crit=None,
                 runtime_config=None,
                 market_condition=None,
                 risk_mgr=None,
                 use_panda=False):
        
        super().__init__()  

        self.use_panda = use_panda
        self.watchlist  = watchlist                
        self.target_path = target_path
        self.strategy_list = strategy_list
        self.entry_crit = entry_crit 
        self.runtime_config = runtime_config
        self.market_condition = market_condition
        self.risk_mgr = risk_mgr 

    def execute(self):                             
        import os

        if self.use_panda:
            accountBook = panda_wb.accountBook(file_path=self.target_path, 
                                            strategy_list=self.strategy_list,
                                            entry_crit = self.entry_crit,
                                            runtime_config = self.runtime_config,
                                            risk_mgr = self.risk_mgr,
                                            market_condition = self.market_condition,
                                            create=True)             
        else:
            accountBook = xlwings_wb.accountBook(file_path=None, 
                                            strategy_list=self.strategy_list,
                                            entry_crit = self.entry_crit,
                                            runtime_config = self.runtime_config,
                                            risk_mgr = self.risk_mgr,
                                            market_condition = self.market_condition)        
        
            accountBook.wb.save(self.target_path)

        accountBook.update_all_strategy_positions()   
                    
        if self.watchlist.empty == False:       
            accountBook.try_open_new_strategy_positions(self.watchlist)   

              
            
        return