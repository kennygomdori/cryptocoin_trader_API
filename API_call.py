# Copyright (c) 2014 Keun Hoi Kim
"""General purpose API call for Bitcoin exchanges"""
import http.client
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
    def __init__(self, api_key, api_secret):
        # API key data
        self.api_key = api_key
        self.api_secret = api_secret
        # main url for exchanges. e.g.) "btc-e.com"

    def get_nonce(self):
        return int(str(time.time()*1.35-1393497454).split('.')[0])
     
    def POST(self,url,params):
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
    def headers(self,method,nonce,params):
        #generates headers for BTC-e function headers
        params['method'] = method
        params['nonce'] = self.get_nonce()
        params = urllib.parse.urlencode(params)
        headers = {"Content-type" : "application/x-www-form-urlencoded",
                   "Key" : self.api_key,
                   "Sign" : hmac.new(self.api_secret, params, digestmod=hashlib.sha512).hexdigest()}
        return headers
    
    def balance(self):
        return self.POST('getInfo', {}, '/tapi')
    
    def TransHistory(self, tfrom, tcount, tfrom_id, tend_id, torder, tsince, tend):
        params = {
        "from"	    : tfrom,
        "count"	    : tcount,
        "from_id"   : tfrom_id,
        "end_id"    : tend_id,
        "order"	    : torder,
        "since"	    : tsince,
        "end"	    : tend}
        return self.POST('TransHistory', params, '/tapi')

    def TradeHistory(self, tfrom, tcount, tfrom_id, tend_id, torder, tsince, tend, tpair):
        params = {
        "from"	    : tfrom,
        "count"	    : tcount,
        "from_id"   : tfrom_id,
        "end_id"    : tend_id,
        "order"	    : torder,
        "since"	    : tsince,
        "end"	    : tend,
        "pair"	    : tpair}
        return self.POST('TradeHistory', params, '/tapi')

    def ActiveOrders(self, tpair):
        params = { "pair" : tpair }
        return self.POST('ActiveOrders', params, '/tapi')

    def Trade(self, tpair, ttype, trate, tamount):
        params = {
        "pair"	    : tpair,
        "type"	    : ttype,
        "rate"	    : trate,
        "amount"    : tamount}
        return self.POST('Trade', params, '/tapi')

    def CancelOrder(self, torder_id):
        params = { "order_id" : torder_id }
        return self.POST('CancelOrder', params, '/tapi')
        
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
    def balance(self):
        return self.POST('getInfo', {}, '/api/balance')
    
    def TransHistory(self, tfrom, tcount, tfrom_id, tend_id, torder, tsince, tend):
        params = {
        "from"	    : tfrom,
        "count"	    : tcount,
        "from_id"   : tfrom_id,
        "end_id"    : tend_id,
        "order"	    : torder,
        "since"	    : tsince,
        "end"	    : tend}
        return self.POST('TransHistory', params, '/tapi')

    def TradeHistory(self, tfrom, tcount, tfrom_id, tend_id, torder, tsince, tend, tpair):
        params = {
        "from"	    : tfrom,
        "count"	    : tcount,
        "from_id"   : tfrom_id,
        "end_id"    : tend_id,
        "order"	    : torder,
        "since"	    : tsince,
        "end"	    : tend,
        "pair"	    : tpair}
        return self.POST('TradeHistory', params, '/tapi')

    def ActiveOrders(self, tpair):
        params = { "pair" : tpair }
        return self.POST('ActiveOrders', params, '/tapi')

    def Trade(self, tpair, ttype, trate, tamount):
        params = {
        "pair"	    : tpair,
        "type"	    : ttype,
        "rate"	    : trate,
        "amount"    : tamount}
        return self.POST('Trade', params, '/tapi')

    def CancelOrder(self, torder_id):
        params = { "order_id" : torder_id }
        return self.POST('CancelOrder', params, '/tapi')


#account1 = BTCe('hello', 'secret')
account2 = Bitstamp('JnU7gg9QQLgZUmQ33pwhue0UXios40Lz', 'hhKNr4cD30yJ4iZ5vxSzhKrZ0XydS9vS')
#print(account1.depth())
print(account2.trades())
#print(account2.balance())
