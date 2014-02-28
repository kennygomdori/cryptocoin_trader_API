# Copyright (c) 2014 Keun Hoi Kim
"""General purpose API call for Bitcoin exchanges"""
import http.client
import urllib
import json
import hashlib
import hmac

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
    def __init__(self, api_key, api_secret, HTTPSConnection):
        # API key data
        self.api_key = api_key
        self.api_secret = api_secret
        # main url for exchanges. e.g.) "btc-e.com"
        self.HTTPSConnection = HTTPSConnection
     
    def POST(self,method,params,url):
        #POST is for private functions.
        #params is an array of {'method':method,'nonce':nonce}.
        #url is the API url without the main adress. e.g.) "/tapi" for BTC-e for postings
        params['method'] = method
        params['nonce'] = str(time.time()-1393497454).split('.')[0]
        params = urllib.parse.urlencode(params)
        headers = {"Content-type" : "application/x-www-form-urlencoded",
                   "Key" : self.api_key,
                   "Sign" : hmac.new(self.api_secret, params, digestmod=hashlib.sha512).hexdigest()}
        conn = http.client.HTTPSConnection(self.HTTPSConnection)
        conn.request("POST", url, params, headers)
        response = conn.getresponse()
        data = json.load(response)
        conn.close()
        return data

    def GET(self, url, params=''):
        #GET is for public functions.
        #params should be in json.
        #url must include '/'.
        conn = http.client.HTTPSConnection(self.HTTPSConnection)
        conn.request("GET", url+"/"+params)
        response = conn.getresponse()
        print(response.status, response.reason)
        data = json.loads(response.read().decode('utf-8'))
        conn.close()
        return data


        
class BTCe(exchangeAPI):
    #BTCe subclass of exchangeAPI where BTC-e specific functions are stored. One for each account.
    def fee(self):
        #returns fee in %.
        return self.GET('/api/2/btc_usd/fee','{}')
    def ticker(self):
        #needs formatting
        return self.GET('/api/2/btc_usd/ticker','{}')
    def depth(self):
        return self.GET('/api/2/btc_usd/depth','{}')
    def trades(self):
        return self.GET('/api/2/btc_usd/trades','{}')
        
class Bitstamp(exchangeAPI):
    def fee(self):
        pass
    def ticker(self):
        return self.GET('/api/ticker')
    def depth(self):
        #This was a lot longer than I thought. Need to parse.
        return self.GET('/api/order_book')
    def trades(self,timedelta=3600):
        #Returns transactions for the last 'timedelta' seconds.
        return self.GET('/api/transactions')


#account1 = BTCe('hello', 'secret', "btc-e.com")
account2 = Bitstamp('hello', 'secret', "www.bitstamp.net")
#print(account1.depth())
#print(account2.ticker())
print(account2.trades())
