
import os
from tradingBot.jobs import core
from tradingBot.excel import positionBook as pb
from tradingBot.excel import watchListBook as wb


import logging

logger = logging.getLogger('dataset create job')

class dataset_create_job(core.core):
           
    def __init__(self, 
                 watchlist_path, 
                 target_path,
                 entry_crit,
                 runtime_config,
                 market_condition,
                 risk_mgr 
                 ):
        super().__init__()  
        self.watchlist_path  = watchlist_path        
        self.target_path = target_path
        self.entry_crit = entry_crit 
        self.runtime_config = runtime_config
        self.market_condition = market_condition
        self.risk_mgr = risk_mgr        

    def execute(self):      
        if  os.path.exists(self.watchlist_path):   
            watchBook = wb.watchListBook(self.watchlist_path)        
            watch_list = watchBook.get_all_watch_list()       
        else:
            logger.error('watchlist %s not exits' % self.watchlist_path)
            return

        if  os.path.exists(self.target_path): 
            logger.error('dataset %s already exits' % self.target_path)
        else:                   
            dataset = pb.positionBook(file_path=None,
                                      entry_crit=self.entry_crit,
                                      runtime_config=self.runtime_config,
                                      market_condition=self.market_condition,
                                      risk_mgr=self.risk_mgr)            
            dataset.wb.save(self.target_path) 
            dataset.init_dataset(watch_list)
        return
     