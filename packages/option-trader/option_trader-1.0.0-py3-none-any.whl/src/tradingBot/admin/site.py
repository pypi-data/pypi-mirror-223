
import sqlite3
from pathlib import Path
import os
import json      

import pandas as pd

import logging


from tradingBot.settings import app_settings   
from tradingBot.settings import schema as schema  
from tradingBot.admin import user
from tradingBot.utils.monitor import refresh_monitor_list
from tradingBot.consts import strategy 
from tradingBot.consts import asset



class site():

    def __init__(self, site_name, default_strategy=[]):        
        
        self.site_name = site_name
        self.user_root = app_settings.USER_ROOT_DIR
        self.site_root = app_settings.SITE_ROOT_DIR
        self.data_root = app_settings.DATA_ROOT_DIR
        self.logger = logging.getLogger(__name__)

        if app_settings.DATABASES == 'sqlite3':
            try:                
                self.db_path = app_settings.SITE_ROOT_DIR+"/"+site_name+"_site.db"

                if os.path.exists(self.db_path ):
                    self.db_conn   = sqlite3.connect(self.db_path)  
                    if len(default_strategy) > 0:
                        self.update_default_strategy(default_strategy)                        
                    return
                 
                self.db_conn   = sqlite3.connect(self.db_path)  
                cursor = self.db_conn.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS site_profile("+schema.site_profile+")")
                cursor.execute("CREATE TABLE IF NOT EXISTS user_list("+schema.user_list+")")
                cursor.execute("CREATE TABLE IF NOT EXISTS monitor("+schema.site_monitor_db+")")                                             
                sql = "INSERT INTO site_profile (site_name, default_strategy) VALUES (?, ?)"              
                if len(default_strategy) == 0:
                    default_strategy = strategy.ALL_STRATEGY
                cursor.execute(sql, [site_name, json.dumps(default_strategy)])
                self.db_conn.commit()    
            except Exception as e:
                self.logger.exception(e)    
        return

    def __enter__(self):
        return self
 
    def __exit__(self, *args):
        try:
            self.db_conn.close()
        except Exception as ex:
            self.logger.exception(ex)
            raise ex
                    
    def create_user(self, user_name):        
        if user_name in self.get_user_list():
            self.logger.error('User %s already exists return existing user' % user_name)
            return user.user(self, user_name)
        
        if app_settings.DATABASES == 'sqlite3':        
            try:
                u = user.user(self, user_name)                
                sql = "INSERT INTO user_list VALUES (?,?)"       
                cursor = self.db_conn.cursor()
                cursor.execute(sql, [user_name, u.db_path]) 
                self.db_conn.commit()
                return u                
            except Exception as e:
                self.logger.exception(e)   
                return False
        else:
            self.logger.error('Unsupported database engine %s' % app_settings.DATABASES)

    def get_user(self, user_name):        
        if app_settings.DATABASES == 'sqlite3':        
            user_list = self.get_user_list()
            if user_name not in user_list:
                self.logger.error('User %s not found in this site' % user_name)
                return None                                                      
        else:
            self.logger.error('Unsupported database engine %s' % app_settings.DATABASES)

        return user.user(self, user_name=user_name)    
        
    def get_user_list(self):
        if app_settings.DATABASES == 'sqlite3':                
            try:
                cursor = self.db_conn.cursor()                    
                users = [name[0] for name in cursor.execute("SELECT user_name FROM user_list")]
                return users
            except Exception as e:
                self.logger.exception(e)   
                return []
        else:
            self.logger.error('Unsupported database engine %s' % app_settings.DATABASES)
            return []
        
    def expand_monitor_list(self, asset_list):
        if app_settings.DATABASES == 'sqlite3':                 
            monitor_list = self.get_monitor_list()
            cursor = self.db_conn.cursor()
            filter=[]               
            for symbol in asset_list:
                if symbol in monitor_list:
                    continue             
                #cursor.execute("CREATE TABLE IF NOT EXISTS monitor("+schema.site_monitor_db+")")                                             
                sql = "INSERT INTO monitor ("+asset.SYMBOL+") VALUES (?)"              
                try:
                    cursor.execute(sql, [symbol])
                    self.db_conn.commit()
                except Exception as e:                    
                    self.logger.warning('Add %s failed %s' % (symbol, str(e)))
                    continue
                filter.append(symbol)                
        else:
            self.logger.error("sqlite3 only for now %s")

        if len(filter) > 0:
            self.refresh_site_monitor_list(filter=filter)

    def get_default_strategy(self):
        if app_settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT default_strategy FROM site_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return json.loads(cursor.fetchone()[0])                
            except Exception as e:
                self.logger.exception(e)   
                return []
        else:
            self.logger.error("sqlite3 only for now %s")
           
    def update_default_strategy(self, default_strategy):
        if len(default_strategy) == 0:
            return
        
        if app_settings.DATABASES == 'sqlite3':                 
            try:                              
                sql = "UPDATE site_profile SET default_strategy='"+json.dumps(default_strategy)+"' WHERE site_name='"+self.site_name+"'"                    
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                self.db_conn.commit()                 
            except Exception as e:
                self.logger.exception(e)   
                return []
        else:
            self.logger.error("sqlite3 only for now %s")

    def get_monitor_list(self):
        if app_settings.DATABASES == 'sqlite3':                 
            try:    
                cursor = self.db_conn.cursor()                    
                symbols = [symbol[0] for symbol in cursor.execute("SELECT "+asset.SYMBOL+ " FROM monitor")]
                return symbols
            except Exception as e:
                self.logger.exception(e)   
                return []
        else:
            self.logger.error("sqlite3 only for now %s")

    def get_monitor_df(self, filter=[]):
        if app_settings.DATABASES == 'sqlite3':                 
            try:    
                import pandas as pd                
                df = pd.read_sql_query("SELECT * FROM monitor", self.db_conn)                           
                df = df[df[asset.SYMBOL].isin(filter)] if len(filter)>0 else df           
                #df[asset.IV1] = pd.to_numeric(df[asset.IV1], errors='coerce')
                #df[asset.HV] = pd.to_numeric(df[asset.HV], errors='coerce')
                return df
            except Exception as e:
                self.logger.exception(e)   
                return []
        else:
            self.logger.error("sqlite3 only for now %s")

    def refresh_site_monitor_list(self, filter=[]):    
        if app_settings.DATABASES == 'sqlite3':                 
            try:
                import pandas as pd                
                df = pd.read_sql_query("SELECT * FROM monitor", self.db_conn)                          
                refresh_monitor_list(df, filter=filter)                
                df.to_sql('monitor', self.db_conn, if_exists='replace', index=False, schema=schema.site_monitor_db)
                self.db_conn.commit()                
                return df
            except Exception as e:
                self.logger.exception(e)   
                raise e
                #return []
        else:
            self.logger.error("sqlite3 only for now %s")

    def select_high_IV_HV_ratio_asset(self, ratio, filter=[]):
        df = self.get_monitor_df(filter=filter)
        df[asset.IV1] = pd.to_numeric(df[asset.IV1], errors='coerce')
        df[asset.HV] = pd.to_numeric(df[asset.HV], errors='coerce')
        dd = df[df[asset.IV1]/df[asset.HV] >= ratio]
        return dd[asset.SYMBOL].to_list()  

    def select_low_IV_HV_ratio_asset(self, ratio, filter=[]):
        df = self.get_monitor_df(filter=filter)
        df[asset.IV1] = pd.to_numeric(df[asset.IV1], errors='coerce')
        df[asset.HV] = pd.to_numeric(df[asset.HV], errors='coerce')
        dd = df[df[asset.IV1]/df[asset.HV] <= ratio]
        return dd[asset.SYMBOL].to_list()  
    

        

