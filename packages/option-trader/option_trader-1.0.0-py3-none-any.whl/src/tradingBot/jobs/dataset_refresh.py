
import os
from tradingBot.jobs import core
from tradingBot.excel import positionBook as pb

import logging

logger = logging.getLogger('dataset refresh job')

class dataset_refresh_job(core.core):
        
    def __init__(self, file_path):
        super().__init__()            
        self.file_path = file_path


    def execute(self):      
        if  os.path.exists(self.file_path):        
            dataset = pb.positionBook(file_path=self.file_path)  
            dataset.refresh_dataset() 
        else:           
            logger.error('dataset %s not exits 2' % self.file_path)
        return