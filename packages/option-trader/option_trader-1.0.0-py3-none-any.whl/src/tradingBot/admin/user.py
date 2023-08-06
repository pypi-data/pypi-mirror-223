
import traceback
import shutil
import pandas as pd
import os
import json   

from tradingBot.settings import app_settings  as settings    
from tradingBot.settings import schema as schema  

from tradingBot.utils.line_norify import lineNotifyMessage 
from tradingBot.admin.account import account
from tradingBot.settings import app_settings
import re
import sqlite3

from pathlib import Path

import logging



class user():  
    def __init__(self, site, user_name):
        self.site = site
        self.user_name = user_name
        self.email = ""
        self.default_strategy = []
        self.logger = logging.getLogger(__name__)
        self.user_home_dir = settings.USER_ROOT_DIR+'/'+self.user_name        

        if os.path.exists(self.user_home_dir) == False:        
            os.mkdir(self.user_home_dir)

        if settings.DATABASES == 'sqlite3':      
            self.db_path = self.user_home_dir+"/"+self.user_name+"_user.db"                     
            try:   
                if os.path.exists(self.db_path): 
                    self.db_conn  = sqlite3.connect(self.db_path)                   
                    self.email = self.get_user_email()
                    self.default_strategy = self.get_default_strategy()
                    return                                         
                self.db_conn  = sqlite3.connect(self.db_path)  
                cursor = self.db_conn.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS user_profile("+schema.user_profile+")")
                cursor.execute("CREATE TABLE IF NOT EXISTS account_list("+schema.account_list+")")
                cursor.execute("CREATE TABLE IF NOT EXISTS watchlist("+schema.watchlist+")")                                             
                sql = "INSERT INTO user_profile (name, email, default_strategy) VALUES (?, ?, ?)"              
                self.default_strategy = site.get_default_strategy()                
                self.email = "askme@outlook.com"
                cursor.execute(sql, [user_name, self.email, json.dumps(self.default_strategy)])
                self.db_conn.commit()
                self.create_watchlist('default', site.get_monitor_list())                    
            except Exception as e:
                self.logger.error(e)       
        else:
            self.logger.error('Unsupported database engine %s' % settings.DATABASES)

    def __enter__(self):
        return self
 
 
    def __exit__(self, *args):
        try:
            self.db_conn.close()
        except Exception as ex:
            self.logger.exception(ex)
            raise ex
                    

    # create new account        
    def create_account(self, account_name, initial_balance=app_settings.DEFAULT_ACCOUNT_INITIAL_BALANCE):       
        if settings.DATABASES == 'sqlite3':                
            try:
                account_list = self.get_account_list()
                if account_name in account_list:
                    self.logger.error('Account %s alreadt exist return existing one' % account_name)
                    return account(self, account_name)
                
                a = account(self, account_name, initial_balance=initial_balance)             
                sql = "INSERT INTO account_list VALUES (?,?)"       
                cursor = self.db_conn.cursor()
                cursor.execute(sql, [account_name, a.db_path]) 
                self.db_conn.commit()
                return a
            except Exception as e:
                self.logger.error(e)
                return False     

    def get_account_list(self):
        if settings.DATABASES == 'sqlite3':                
            try:
                cursor = self.db_conn.cursor()                    
                account_name_list = [account_name[0] for account_name in cursor.execute("SELECT account_name FROM account_list")]
                return account_name_list
            except Exception as e:
                self.logger.error(e)
                return []
        else:
            self.logger.error('Unsupported database engine %s' % settings.DATABASES)

    def get_watchlist_name_list(self):
        if settings.DATABASES == 'sqlite3':                
            try:
                cursor = self.db_conn.cursor()                    
                names = [name[0] for name in cursor.execute("SELECT name FROM watchlist")]
                return names
            except Exception as e:
                self.logger.error(e)
                return []
        else:
            self.logger.error('sqlite 3 only %s' % settings.DATABASES)

    def get_watchlist(self, watchlist_name):
        if settings.DATABASES == 'sqlite3':                
            try:
                wl = self.get_watchlist_name_list()
                if watchlist_name not in wl:
                    self.logger.error('Watchlist %s Not exist!' % watchlist_name)
                    return pd.DataFrame()
                                 
                sql = "SELECT symbol_list FROM watchlist WHERE name='"+watchlist_name+"'"               
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                profile = cursor.fetchone()
                return json.loads(profile[0]) 
            except Exception as e:
                self.logger.exception(e)
                return []
        else:
            self.logger.error('sqlite 3 only %s' % settings.DATABASES)

    def create_watchlist(self, watchlist_name, symbol_list):
        if settings.DATABASES == 'sqlite3':
            wl = self.get_watchlist_name_list()
            if watchlist_name in wl:
                self.logger.error('Watchlist %s already exist!' % watchlist_name)
                return            
            try:
                sql = "INSERT INTO watchlist (name, symbol_list) VALUES (?, ?)"              
                cursor = self.db_conn.cursor()
                cursor.execute(sql, [watchlist_name, json.dumps(symbol_list)])
                self.db_conn.commit()                    
                self.site.expand_monitor_list(symbol_list)
            except Exception as e:
                self.logger.error(e)           
        else:
            self.logger.error('sqlite3 only %s' % settings.DATABASES)

    def update_watchlist(self, watchlist_name, symbol_list):
        if settings.DATABASES == 'sqlite3':
            wl = self.get_watchlist_name_list()
            if watchlist_name not in wl:
                self.logger.error('Watchlist %s not exits!' % watchlist_name)
                return            
            try:                
                sql = "UPDATE watchlist SET symbol_list='"+json.dumps(symbol_list)+"' WHERE name='"+watchlist_name+"'"                    
                cursor = self.db_conn.cursor()
                cursor.execute(sql)
                self.db_conn.commit()                    
            except Exception as e:
                self.logger.error(e)           
        else:
            self.logger.error('sqlite3 only %s' % settings.DATABASES)

    def get_user_profile(self):
        if settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT email, default_strategy FROM user_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                profile = cursor.fetchone()
                return profile[0], json.loads(profile[1]) 
            except Exception as e:
                self.logger.error(e)
        else:
            self.logger.error("sqlite3 only for now %s")
        return None, None
    
    def get_default_strategy(self):
        if settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT default_strategy FROM user_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return json.loads(cursor.fetchone()[0])                   
            except Exception as e:
                self.logger.error(e)
                return []
        else:
            self.logger.error("sqlite3 only for now %s")
           
    def get_user_email(self):
        if settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT email FROM user_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return cursor.fetchone()[0]
            except Exception as e:
                self.logger.error(e)
                return []
        else:
            self.logger.error("sqlite3 only for now %s")

    def update_default_strategy(self, default_strategy):
        if len(default_strategy) == 0:
            return        
        if settings.DATABASES == 'sqlite3':                 
            try:                              
                sql = "UPDATE user_profile SET default_strategy='"+json.dumps(default_strategy)+"' WHERE name='"+self.user_name+"'"                    
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                self.db_conn.commit()                 
            except Exception as e:
                self.logger.error(e)
                return []
        else:
            self.logger.error("sqlite3 only for now %s")

    def update_user_email(self, email):

        if len(email) == 0:
            return    
            
        if settings.DATABASES == 'sqlite3':                 
            try:                              
                sql = "UPDATE user_profile SET email='"+email+"' WHERE name='"+self.user_name+"'"                    
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                self.db_conn.commit()                 
            except Exception as e:
                self.logger.error(e)
                return []
        else:
            self.logger.error("sqlite3 only for now %s")

    def update_account_strategy(self, account_name, strategy_list):
        with account(self.user_name, account_name) as ac:        
            ac.update_strategy_list(strategy_list)              

    def update_account_positions(self, account_name):
        with account(self.user_name, account_name) as ac:           
            ac.update_positions()

    def submit_account_orders(self, account_name):        
        with account(self.user_name, account_name) as ac:           
            ac.submit_orders()
                
    def get_account(self, account_name):
        return account(self.user_name, account_name)
    
if __name__ == '__main__':

    from tradingBot.admin import user as u              
    me = u.user('jihuang')
    me.update_account('condor')
    #me.update_account('spread')