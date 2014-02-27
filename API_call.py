# Copyright (c) 2014 Keun Hoi Kim
"""General purpose API call for Bitcoin exchanges"""
import httplib
import urllib
import json
import hashlib
import hmac

#array of exchange, exchage-specific functions, and params and urls for the functions
exchanges=

class api(object):
    def __init__(self, api_key, api_secret, HTTPSConnection):
        # API key data
        self.api_key = api_key
        self.api_secret = api_secret
        # main url for exchanges. e.g.) "https://btc-e.com"
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

    def GET(self,method,params,url):
        #GET is for public functions.
        #params should be in json.
        conn = http.client.HTTPSConnection(self.HTTPSConnection)
        conn.request("GET", url+"/"+param)
        response = conn.getresponse()
        data = json.load(response)
        conn.close()
        return data
        
