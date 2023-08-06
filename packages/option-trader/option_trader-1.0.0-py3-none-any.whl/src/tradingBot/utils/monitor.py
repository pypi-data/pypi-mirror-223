
import os

import pandas as pd
import pandas_ta as ta
import yfinance as yf

from datetime import time, date, datetime, timedelta
from pytz import timezone

import pymannkendall as mk
import math
import numpy as np

from tradingBot.consts import RGB
from tradingBot.consts import asset as at

from tradingBot.utils.dataGetter import get_price_history
from tradingBot.utils.dataGetter import get_next_earning_date
from tradingBot.utils.dataGetter import get_support_resistence_levels
from tradingBot.utils.dataGetter import get_option_exp_date
from tradingBot.utils.dataGetter import get_option_leg_details
from tradingBot.utils.dataGetter import get_option_leg_IV_delta


from tradingBot.backtest.stock.bollingerBands import BB_strategy, plot_BB
from tradingBot.backtest.stock.macd import MACD_strategy, plot_MACD
from tradingBot.backtest.stock.mfi import MFI_strategy, plot_MFI
from tradingBot.backtest.stock.rsi import RSI_strategy, plot_RSI

from tradingBot.settings.taStrategy import CustomStrategy
from  tradingBot.settings import app_settings


import logging


import warnings
warnings.filterwarnings( "ignore", module = "matplotlib\..*" )

from tradingBot.settings import app_settings  as settings    

def refresh_monitor_list(df, filter=[]):
    logger = logging.getLogger(__name__)
    for i, r in df.iterrows(): 
        if len(filter) > 0 and r['symbol'] not in filter:
             continue               
        try:  
            refresh_asset_info(i, df)
        except:
            logger.error('Cannot refresh %s' % r['symbol'])
            pass

    return df

def refresh_asset_info(i, df):

    logger = logging.getLogger(__name__)

    symbol = df.at[i, 'symbol']
    data = get_price_history(symbol)
    data.ta.cores = 2
    data.ta.strategy(CustomStrategy)
    data.dropna(subset=["BBL_20_2.0"])        
    refresh_asset_basic_info(i, df, data)        
    refresh_BB(i, df, data)
    refresh_RSI(i, df, data)        
    refresh_MFI(i, df, data)        
    refresh_MACD(i, df, data)        
    logger.debug('%s refreshed' %symbol)
     
def refresh_asset_basic_info(i, df, data):        
    logger = logging.getLogger(__name__)
    symbol = df.at[i, 'symbol']        

        #sheet = WatchListBook.load_fundamentalSheet(MonitorLists[0])
    #q = yf.Ticker(symbol).get_info()   
    q = yf.Ticker(symbol).fast_info

    df.at[i, 'quote_time'] = datetime.now(timezone(app_settings.TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S %Z")
    last_price = data['Close'][-1]
    day_high =  q['dayHigh'] if 'dayHigh' in q else np.nan
    day_low  =  q['dayLow']  if 'dayLow' in q else np.nan
    if math.isnan(last_price) == False and day_high-day_low > 0:
        day_range_pos = ((last_price - day_low)/(day_high-day_low)) * 100
    else:
        day_range_pos = np.nan

    fifty_two_weeks_low = q['yearLow'] if 'yearLow' in q else np.nan
    fifty_two_weeks_high = q['yearHigh'] if 'yearHigh' in q else np.nan
    fifty_two_weeks_range_pos = ((last_price - fifty_two_weeks_low)/(fifty_two_weeks_high-fifty_two_weeks_low))*100 if 'yearLow'  in q else np.nan

    if 'lastVolume' in q:
        volume = q['lastVolume']
        avg_volume = float(q['threeMonthAverageVolume'])
        volume_range_pos = (volume/avg_volume)*100   if avg_volume > 0 else np.nan         
    else:
        volume_range_pos = np.nan     

    df.at[i, 'forward_PE'] = q['forwardPE']  if 'forwardPE' in q else np.nan
    report_date = get_next_earning_date(symbol)        
    df.at[i, 'earning'] = '' if report_date == None else report_date.strftime('%m-%d-%Y')                                  
    df.at[i, 'last_price'] = last_price       
    df.at[i, 'day_range_pos'] =  round(day_range_pos,2)
    df.at[i, 'fifty_weeks_range_pos'] = round(fifty_two_weeks_range_pos,2)
    df.at[i, 'volume_range_pos'] = round(volume_range_pos,2)                      
    support, resistence = get_support_resistence_levels(symbol, data)
    df.at[i, 'support'] = round(support,2) if support != None else np.nan
    df.at[i, 'resistence'] = round(resistence,2) if resistence != None else np.nan                    

    '''
    df.at[i, 'forward_PE'] = "{:.2f}".format(q['forwardPE'])  if 'forwardPE' in q else np.nan
    report_date = get_next_earning_date(symbol)        
    df.at[i, 'earning'] = '' if report_date == None else report_date.strftime('%m-%d-%Y')                                  
    df.at[i, 'last_price'] = "{:.2f}".format(last_price)       
    df.at[i, 'day_range_pos'] = "{:.2f}".format(day_range_pos)
    df.at[i, 'fifty_weeks_range_pos'] = "{:.2f}".format(fifty_two_weeks_range_pos)
    df.at[i, 'volume_range_pos'] = "{:.2f}".format(volume_range_pos)                      
    support, resistence = get_support_resistence_levels(symbol, data)
    df.at[i, 'support'] = "{:.2f}".format(support) if support != None else np.nan
    df.at[i, 'resistence'] = "{:.2f}".format(resistence) if resistence != None else np.nan                    
    '''
    s = settings.TREND_WINDOW_SIZE
    gfg_data = [0] * s
    # perform Mann-Kendall Trend Test   
    last_date_index = len(data.index)-1        
    for j in range(s):        
        gfg_data[j] = data['BBM_20_2.0'][last_date_index-s+1+j]    
    x = mk.original_test(gfg_data)            

    df.at[i, 'trend'] = x.trend
    df.at[i, 'slope'] = round(x.slope,2)                      
        
    TRADING_DAYS =252
    returns = np.log(data['Close']/data['Close'].shift(1))
    returns.fillna(0, inplace=True)
    volatility = returns.rolling(window=20).std()*np.sqrt(TRADING_DAYS)
    hv = round(volatility[-1],2)    

    df.at[i, 'HV'] = hv #"{:.2f}".format(hv*100)

    def get_iv_list(symbol, data, count):     
        exp_tbl = get_option_exp_date(symbol)               
        iv = []
        delta=[]
        for exp_date in exp_tbl:    
            eiv, edelta = get_option_leg_IV_delta(symbol, exp_date, at.CALL)           
            iv.append(eiv)
            delta.append(edelta)
            count -= 1
            if count == 0:
                return iv, delta            
        return iv, delta 
    
    iv, delta = get_iv_list(symbol, data, 4)
        
    if len(iv) > 0:        
        df.at[i, 'IV1']  = round(iv[0],3) # "{:.2f}".format(iv[0]*100)
        df.at[i, 'delta1'] = round(delta[0],3) #"{:.2f}".format(delta[0])    

    if len(iv) > 1:            
        df.at[i, 'IV2']  = round(iv[1],3) #"{:.2f}".format(iv[1]*100)
        df.at[i, 'delta2'] = round(delta[1],3) #"{:.2f}".format(delta[1])

    if len(iv) > 2:                  
        df.at[i, 'IV3']  =  round(iv[2],3) #"{:.2f}".format(iv[2]*100)
        df.at[i, 'delta3'] = round(delta[2],3) #"{:.2f}".format(delta[2])
    
    if len(iv) > 3:
        df.at[i, 'IV4']  =  round(iv[3],3) #"{:.2f}".format(iv[3]*100)       
        df.at[i, 'delta4'] = round(delta[2],3) #"{:.2f}".format(delta[3])
                              
    df.at[i, 'rating'] = float(q['recommendationMean']) if 'recommendationMean' in q else 0
           
def refresh_BB(i, df, data):            
    bb_pos = data['BBP_20_2.0'][-1]        
    last_action, last_action_price, recent, total_profit = BB_strategy(data, settings.TREND_WINDOW_SIZE)  
    #BB_display = last_action + " {:.2f}".format(last_action_price) if (last_action != '' and recent) else "{:.2f}".format(bb_pos)                  
    BB_display = "{:.2f}".format(bb_pos)                  
    address = plot_BB(df.at[i, 'symbol'], data)
    df.at[i, 'bb_pos'] =  round(bb_pos,2) # BB_display
    df.at[i, 'bb_link'] = address 
     
def refresh_RSI(i, df, data):     
    last_action, last_action_price, recent, total_profit = RSI_strategy(data)          
    rsi = data['RSI_14'][-1]
    #RSI_display = last_action + " {:.2f}".format(last_action_price) if (recent and last_action != '') else "{:.2f}".format(rsi)      
    RSI_display = "{:.2f}".format(rsi)      
    address =  plot_RSI(df.at[i, 'symbol'], data)                 
    df.at[i, 'rsi'] =  round(rsi,2) #RSI_display
    df.at[i, 'rsi_link'] = address                  

def refresh_MFI(i, df, data):           
    last_action, last_action_price, recent, total_profit = MFI_strategy(data)  
    mfi = data['MFI_14'][-1]
    address =  plot_MFI(df.at[i, 'symbol'], data) 
    #MFI_display = last_action + " {:.2f}".format(last_action_price) if (recent and last_action != '') else "{:.2f}".format(mfi)          
    MFI_display = "{:.2f}".format(mfi)          
    df.at[i, 'mfi'] =  round(mfi,2) #MFI_display
    df.at[i, 'mfi_link'] = address    
    
def refresh_MACD(i, df, data):                
    last_action, last_action_price, recent, total_profit = MACD_strategy(data)  
    macd = data['MACD_12_26_9'][-1]
    address = plot_MACD(df.at[i, 'symbol'], data)
    #MACD_display = last_action + " {:.2f}".format(last_action_price) if (recent and last_action != '') else"{:.2f}".format(macd)          
    MACD_display = "{:.2f}".format(macd)          
    df.at[i, 'macd'] =  round(macd,2)#MACD_display
    df.at[i, 'macd_link'] = address                             
