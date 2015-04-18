#!/bin/env python
#coding=utf8
from util import tryExec
import base64
import urllib2
import urllib
import json
import re
import logging
import rsa
import binascii
from Crypto.PublicKey import RSA

def defaultWeiboErrorHandler(*args):
    for exception in args:
        print exception

def getCommonData(data = {}, access_token = ''):
    data["access_token"] = access_token
    return urllib.urlencode(data)
        
def send_weibo(message, access_token):
    url_sendWeibo = 'https://api.weibo.com/2/statuses/update.json'
    data = {}
    data['status'] = message
    data = getCommonData(data, access_token)

    try:
        httpreq = urllib2.Request(url_sendWeibo)
        response = urllib2.urlopen(httpreq, data).read()
        jsonobj = json.loads(response)
    except urllib2.HTTPError, e:
        print e
        print e.read()
        print e.reason
    if not 'idstr' in jsonobj:
        print '发送失败'
    return jsonobj['idstr']

@tryExec(1)
def getWeiboByID(weiboid):
    weibo_get_url = 'https://api.weibo.com/2/statuses/show.json'
    data = {'id': weiboid}
    data = getCommonData(data)
    url = weibo_get_url + "?" + data 
    req = urllib2.Request(url)
    response = urllib2.urlopen(req).read()
    jsonobj = json.loads(response)
    return jsonobj

