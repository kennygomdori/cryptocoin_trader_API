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
        conn = http.client.HTTPSConnection(self.HTTPSConnection)
        conn.request("GET", url+"/"+params)
        response = conn.getresponse()
        encoding = response.headers.get_content_charset()
        print(type(response))
        data = json.load(response.read().decode(encoding))
        conn.close()
        return data
        
class BTCe(exchangeAPI):
    #BTCe subclass of exchangeAPI where BTC-e specific functions are stored. One for each account.
    def fee(self):
        #returns fee in %.
        return self.GET('/api/2/btc_usd/fee')
        

        
class Bitstamp(exchangeAPI):
    def fee(self):
        pass


account = BTCe('hello', 'secret', "btc-e.com")
print(json.load(account.fee()))
