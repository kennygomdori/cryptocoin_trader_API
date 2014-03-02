# Copyright (c) 2014 Keun Hoi Kim
"""General purpose API call for Bitcoin exchanges"""
import httplib
import urllib
import json
import hashlib
import hmac
import time
import requests
'''
Ultimate goal is to be able to use a simple call such as btc-e(sell,42,522).
'''

#array of exchange, exchage-specific functions, and params and urls for the functions
'''
fee
ticker
trades
depth
'''


class exchangeAPI(object):
    def __init__(self, api_key, api_secret, client_id = ''):
        # API key data
        self.api_key = api_key
        self.api_secret = api_secret
        self.prev_nonce = 0
        self.client_id = client_id
        # main url for exchanges. e.g.) "btc-e.com"

    def nonce(self):
        #common for all APIs. Maybe need separate ones for security?
        #it adds one to previous nonce to create a different nonce. It allows more than 1 actions per second.
        nonce = int(time.time())
        if self.prev_nonce >= nonce: nonce = prev_nonce + 1
        self.prev_nonce = nonce
        return str(nonce)
     
    def POST(self,url,params,headers):
        #POST is for private functions.
        #url is the API url without the main adress. e.g.) "/tapi" for BTC-e for postings
        conn = requests.post(url, data=json.dumps(params), headers=headers)
        return conn.text

    def GET(self, url, params=''):
        #GET is for public functions.
        #url must include '/'.
        conn = requests.get(url, params = params)
        return conn.text


        
class BTCe(exchangeAPI):
    #BTCe subclass of exchangeAPI where BTC-e specific functions are stored. One for each account.
    #GET functions
    def fee(self):
        #returns fee in %.
        return self.GET('https://btc-e.com/api/2/btc_usd/fee',{})
    
    def ticker(self):
        #needs formatting
        return self.GET('https://btc-e.com/api/2/btc_usd/ticker',{})
    
    def depth(self):
        return self.GET('https://btc-e.com/api/2/btc_usd/depth',{})
    
    def trades(self):
        return self.GET('https://btc-e.com/api/2/btc_usd/trades',{})

    #POST functions
    def POST(self,method,params={},url='https://btc-e.com/tapi/'):
        #special POST function for BTC-e
        params['method'] = method
        params['nonce'] = self.nonce()
        params = urllib.urlencode(params) #necessary
        headers = {"Content-type" : "application/x-www-form-urlencoded",
                   "Key" : self.api_key,
                   "Sign" : hmac.new(self.api_secret, params, digestmod=hashlib.sha512).hexdigest()}
        conn = requests.post(url, data=params, headers=headers)
        return conn.text
        
    def Balance(self):
        return self.POST('getInfo', {})
    
    def TransHistory(self, tfrom='', tcount='', tfrom_id='', tend_id='', torder='', tsince='', tend=''):
        params = {
        "from"	    : tfrom,
        "count"	    : tcount,
        "from_id"   : tfrom_id,
        "end_id"    : tend_id,
        "order"	    : torder,
        "since"	    : tsince,
        "end"	    : tend}
        return self.POST('TransHistory', params)

    def TradeHistory(self, tfrom='', tcount='', tfrom_id='', tend_id='', torder='', tsince='', tend='', tpair=''):
        params = {
        "from"	    : tfrom,
        "count"	    : tcount,
        "from_id"   : tfrom_id,
        "end_id"    : tend_id,
        "order"	    : torder,
        "since"	    : tsince,
        "end"	    : tend,
        "pair"	    : tpair}
        return self.POST('TradeHistory', params)

    def ActiveOrders(self, tpair):
        params = { "pair" : tpair }
        return self.POST('ActiveOrders', params)

    def Trade(self, tpair, ttype, trate, tamount):
        params = {
        "pair"	    : tpair,
        "type"	    : ttype, #'buy' or 'sell'
        "rate"	    : trate,
        "amount"    : tamount}
        return self.POST('Trade', params)

    def Sell(self, rate, amount, pair="btc_usd"):
        return self.Trade(pair, 'sell', rate, amount)

    def Buy(self, rate, amount, pair="btc_usd"):
        return self.Trade(pair, 'buy', rate, amount)

    def Cancel(self, torder_id):
        params = { "order_id" : torder_id }
        return self.POST('CancelOrder', params)
        
class Bitstamp(exchangeAPI):
    def fee(self):
        pass
    
    def ticker(self):
        return self.GET('https://www.bitstamp.net/api/ticker')
    
    def depth(self):
        #This was a lot longer than I thought. Need to parse.
        return self.GET('https://www.bitstamp.net/api/order_book')
    
    def trades(self,timedelta=3600):
        #Returns transactions for the last 'timedelta' seconds.
        return self.GET('https://www.bitstamp.net/api/transactions')

    #private functions from hereon
    def POST(self,url='https://www.bitstamp.net/api/',params={}):
        #special POST function for Bitstamp
        #params = urllib.urlencode(params) #necessary?
        nonce = self.nonce()
        msg = str(nonce) + self.client_id + self.api_key
        signature = hmac.new(self.api_secret,
                            msg=msg,
                            digestmod=hashlib.sha256).hexdigest().upper()
        params.update({'key': self.api_key, 'signature': signature, 'nonce': nonce})           
        conn = requests.post(url, params)
        return conn.text
    
    def Balance(self):
        return self.POST('https://www.bitstamp.net/api/balance/')
    
    def TransHistory(self, offset=0, limit=100, descending=True):
        """
        Bitstamp TransHistory doubles as TradeHistory

            {'usd': u'-39.25',
             'datetime': u'2013-03-26 18:49:13',
             'fee': u'0.20', u'btc': u'0.50000000',
             'type' : transaction type (0 - deposit; 1 - withdrawal; 2 - market trade)
             'id': 213642}
        """
        params = {"offset"    : offset, "limit": limit, "descending": descending}
        return self.POST('https://www.bitstamp.net/api/user_transactions/', params)

    def TradeHistory(self, offset=0, limit=100, descending=True):
        params = {"offset"    : offset, "limit": limit, "descending": descending}
        return self.POST('https://www.bitstamp.net/api/user_transactions/', params)

    def ActiveOrders(self):
        params = {}
        return self.POST('https://www.bitstamp.net/api/open_orders/', params)

    def Sell(self, rate, amount):
        params = {
        "amount"    : amount,
        "rate"	    : rate}
        return self.POST('https://www.bitstamp.net/api/sell/', params)

    def Buy(self, rate, amount):
        params = {
        "amount"    : amount,
        "rate"	    : rate}
        return self.POST('https://www.bitstamp.net/api/sell/', params)

    def Cancel(self, order_id):
        params = { "id" : order_id }
        return self.POST('https://www.bitstamp.net/api/cancel_order/', params)

"""
Bter, and Vircurex
"""


#account1 = BTCe('RJIBB911-VMH9M608-KDLYV5T1-7D6NBBS1-QTTXAYR1', '129515e00cf234be7e12b0e020d574536e24550e2dfce45d3d4c5b2d2c82560b')
account2 = Bitstamp('J1kGBNpC5559mQLs4OkNYWZ1LIfpvNMx', 'sovyntDL2pRPMxyRI5wD3aVQnL1wACi3', '680934')
#print(account1.depth())
#print(account1.TradeHistory())
print(account2.depth())
