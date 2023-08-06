#https://algotrading101.com/learn/ib_insync-interactive-brokers-api-guide/

import pandas as pd

from ib_insync import *

import math

from tradingBot.consts import asset as at
from tradingBot.utils.dataGetter_IB import IBClient
from tradingBot.utils.dataGetter import afterHours

from tradingBot.excel import positionSheet as ps

h = ps.positionSheet 

import logging

from tradingBot.settings import app_settings    

def creatOrder(ib, position):

    logger = logging.getLogger(__name__)    
    symbol = position[h.SYMBOL_t]
    exp_date = position[h.EXP_DATE_t].strftime('%Y%m%d')
        
    P1L_contract = P1S_contract = None    
    P2L_contract = P2S_contract = None

    comboLegs = []
    if position[h.P1SK_t] != None:
        strike = position[h.P1SK_t]        
        if position[h.P1ST_t] == at.CALL:
            otype = 'C'
        elif position[h.P1ST_t] == at.PUT:
            otype = 'P'
        else:
            logger.error('Invalid option type %s' % position[h.P1ST_t])
            return [None, None]               
        
        P1S_contract = Option(symbol, exp_date, strike, otype, 'SMART')
        ib.qualifyContracts(P1S_contract)          
        P1S_contract.ratio = 1
        P1S_contract.action = 'SELL'
        P1S_contract.openClose = 0
        P1S_contract.shortSaleSlot = 0
        P1S_contract.exemptCode=0
        P1S_contract.designatedLocation = 0   
      
        comboLegs.append(P1S_contract)
               
    if position[h.P1LK_t] != None:
        strike = position[h.P1LK_t]        
        if position[h.P1LT_t] == at.CALL:
            otype = 'C'
        elif position[h.P1LT_t] == at.PUT:
            otype = 'P'
        else:
            logger.error('Invalid option type %s' % position[h.P1LT_t])
            return [None, None]             
        P1L_contract  = Option(symbol, exp_date, strike, otype, 'SMART')
        ib.qualifyContracts(P1L_contract)   

        P1L_contract.ratio = 1
        P1L_contract.action = 'BUY'        
        P1L_contract.openClose = 0
        P1L_contract.shortSaleSlot = 0
        P1L_contract.exemptCode=0
        P1L_contract.designatedLocation = 0  
      
        comboLegs.append(P1L_contract)      
 
    if position[h.P2SK_t] != None:
        strike = position[h.P2SK_t]        
        if position[h.P2ST_t] == at.CALL:
            otype = 'C'
        elif position[h.P2ST_t] == at.PUT:
            otype = 'P'
        else:
            logger.error('Invalid option type %s' % position[h.P1ST_t])
            return [None, None]     
        
        P2S_contract = Option(symbol, exp_date, strike, otype, 'SMART')
        ib.qualifyContracts(P2S_contract)

        P2S_contract.ratio = 1
        P2L_contract.action = 'SELL'             
        P2S_contract.openClose = 0
        P2S_contract.shortSaleSlot = 0
        P2S_contract.exemptCode=0
        P2S_contract.designatedLocation = 0          
        comboLegs.append(P2S_contract)            
 
    if position[h.P2LK_t] != None:
        strike = position[h.P2LK_t]        
        if position[h.P2LT_t] == at.CALL:
            otype = 'C'
        elif position[h.P2LT_t] == at.PUT:
            otype = 'P'
        else:
            logger.error('Invalid option type %s' % position[h.P2LT_t])
            return [None, None]     
        
        P2L_contract = Option(symbol, exp_date, strike, otype, 'SMART')
        ib.qualifyContracts(P2L_contract)  
        P2L_contract.action = 'BUY'              
        P2L_contract.ratio = 1
        P2L_contract.openClose = 0
        P2L_contract.shortSaleSlot = 0
        P2L_contract.exemptCode=0
        P2L_contract.designatedLocation = 0                     
        comboLegs.append(P2L_contract)     

    contract = Contract(symbol=symbol, secType='BAG', exchange='SMART', currency='USD', comboLegs=comboLegs)

    open_price =  position[h.OPEN_PRICE_t]   

    quantity = position[h.QUANTITY_t]

    order = Order(action='BUY', orderType='LMT', totalQuantity=quantity, lmtPrice=open_price)
    
    return order, contract
               
def placeOrder(position, takeProfitPert=None, stopLossPert=None):

    logger = logging.getLogger(__name__)
    
    if afterHours():
        logger.info('Outside trading hours')
        return [None, None]
        
    ib = IBClient.get_client()
    if ib == None or ib.isConnected() == False:
        logger.info('IB not connected!')
        return [None, None]

    bracketOrder = []

    parent_order, contract = creatOrder(ib, position)

    parent_order.transmit = False

    bracketOrder.append(parent_order)
    
    if takeProfitPert != None:
        takeProfit = Order()
        #takeProfit.orderId = parent_order.orderId+1 
        takeProfit.action = "SELL"
        takeProfit.totalQuantity = parent_order.totalQuantity
        takeProfit.lmtPrice = parent_order.lmtPrice * (1+(takeProfitPert/100)) 
        takeProfit.parentId = parent_order.orderId
        takeProfit.transmit = False
        bracketOrder.append(takeProfit)

    if stopLossPert != None:
        stopLoss = Order()
        #stopLoss.orderId = parent_order.orderId+2 
        stopLoss.action = "SELL"
        stopLoss.orderType = "STP"
        #Stop trigger price
        stopLoss.auxPrice = parent_order.lmtPrice * (1-(stopLossPert/100)) 
        stopLoss.totalQuantity = parent_order.totalQuantity
        stopLoss.parentId = parent_order.orderId
        #In this case, the low side order will be the last child being sent. Therefore, it needs to set this attribute to True 
        #to activate all its predecessors
        stopLoss.transmit = True
        bracketOrder.append(stopLoss)

    bracketOrder[-1].transmit = True

    parent_trade = ib.placeOrder(contract, bracketOrder.pop(0))
    
    for o in bracketOrder:        
        trade = ib.placeOrder(contract, o)

    return parent_order.orderId, parent_trade.orderStatus.status


'''
def BracketOrder(parentOrderId:int, action:str, quantity:Decimal, 
                          limitPrice:float, takeProfitLimitPrice:float, 
                          stopLossPrice:float):
         
        #This will be our main or "parent" order
        parent = Order()
        parent.orderId = parentOrderId
        parent.action = action
        parent.orderType = "LMT"
        parent.totalQuantity = quantity
        parent.lmtPrice = limitPrice
        #The parent and children orders will need this attribute set to False to prevent accidental executions.
        #The LAST CHILD will have it set to True, 
        parent.transmit = False

        takeProfit = Order()
        takeProfit.orderId = parent.orderId + 1
        takeProfit.action = "SELL" if action == "BUY" else "BUY"
        takeProfit.totalQuantity = quantity
        takeProfit.lmtPrice = takeProfitLimitPrice
        takeProfit.parentId = parentOrderId
        takeProfit.transmit = False

        stopLoss = Order()
        stopLoss.orderId = parent.orderId + 2
        stopLoss.action = "SELL" if action == "BUY" else "BUY"
        stopLoss.orderType = "STP"
        #Stop trigger price
        stopLoss.auxPrice = stopLossPrice
        stopLoss.totalQuantity = quantity
        stopLoss.parentId = parentOrderId
        #In this case, the low side order will be the last child being sent. Therefore, it needs to set this attribute to True 
        #to activate all its predecessors
        stopLoss.transmit = True
        bracketOrder = [parent, takeProfit, stopLoss]

        return bracketOrder

        
        bracket = OrderSamples.BracketOrder(self.nextOrderId(), "BUY", 100, 30, 40, 20)
        for o in bracket:
            self.placeOrder(o.orderId, ContractSamples.EuropeanStock(), o)
            self.nextOrderId()  # need to advance this we'll skip one extra oid, it's fine
'''
    
