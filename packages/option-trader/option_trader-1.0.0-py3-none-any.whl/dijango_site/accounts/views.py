from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
 
#from tradingBot.utils.dataGetter_IB import IBClient

#import ib_insync
import logging
import logging.config
import warnings

warnings.filterwarnings("ignore")

logger = logging.getLogger('account_tool')           

#import sys

#sys.path.append(r'\Users\jimhu\option_trader\src')
    
from tradingBot.settings import IBConfig as ic 

from ib_insync import *

#util.startLoop()  # u

def IB_conntect(request):
 
  try:
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        ib = IB()
        ib.connect('127.0.0.1', ic.IBConfig.port, clientId=ic.IBConfig.clientId)            
        # delayed quote
        ib.reqMarketDataType(ic.IBConfig.marketDataType)

        x = ib.portfolio(account='DU7131629')

        ib.isConnected()

        status = x

        #if ib != None:# and  ib.client.isConnected(): 
        #    status = 'OK'         
        #else:
        #    status = 'Cannot connect'

  except Exception as e:
    status = str(e)

  return HttpResponse(status)
