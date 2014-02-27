# Copyright (c) 2014 Keun Hoi Kim
import httplib
import urllib
import json
import hashlib
import hmac

class api(object):
    def __init__(self, api_key, api_secret, HTTPSConnection, url):
        # API key data
        self.api_key = api_key
        self.api_secret = api_secret
        self.HTTPSConnection = HTTPSConnection
        self.url = url #set it to "/tapi" for BTC-e
     
    def POST(self,method,params):
        #"POST"
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

    def GET():
        #"GET"
        
        
