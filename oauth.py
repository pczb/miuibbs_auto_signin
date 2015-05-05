#coding=utf8
import base64
import urllib2
import urllib
import json
import re
import logging
import rsa
import binascii
from Crypto.PublicKey import RSA
import cookielib
import sys
import time

class WeiboOauth:

    def __init__(self, appkey, redirect_uri, appsecret):
        self.appkey = appkey
        self.redirect_uri = redirect_uri
        self.appsecret = appsecret
        self.__initOpener()
        

    def __initOpener(self):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; InfoPath.3'), 
                ('Referer', self.buildAuthUrl())]
        self.opener = opener


    def defaultWeiboErrorHandler(*args):
        for exception in args:
            print exception

    def tokenProcess(self, username):
        url = 'https://login.sina.com.cn/sso/prelogin.php?'
        preProcessData = {
                'entry': 'openapi',
                'callback': 'sinaSSOController.preloginCallBack',
                'su': base64.b64encode(urllib2.quote(username)), 
                'rsakt': 'mod', 
                'checkpin': '1',
                'client': 'ssologin.js(v1.4.15)',
#                '_': str(int(time.time() * 1000)) 
                }

        url += urllib.urlencode(preProcessData)
        loginData_json = self.preProcess(username, preProcessData) 
        return loginData_json

    def tokenTicket(self, username, pwd):
        
        preData =  self.tokenProcess(username)
        url = 'https://login.sina.com.cn/sso/login.php?'

        data = {
                'su': base64.b64encode(urllib2.quote(username)), 
                'service': 'miniblog',
                'servertime': preData['servertime'],
                'nonce': preData['nonce'],
                'pwencode': 'rsa2',
                'rsakv': preData['rsakv'],
                'sp': WeiboOauth.encryptPWD(pwd, preData),
                'sr': '1440*900',
                'encoding': 'UTF-8',
                'cdult': '2',
                'domain': 'weibo.com',
                'prelt': '750',
                'returntype': 'TEXT',
                'callback': 'sinaSSOController.loginCallBack',
                'client': 'ssologin.js(v1.4.15)',
#                '_': str(int(time.time() * 1000))
                }

        re_ticket =  re.compile('({.+?})')
        html = self.opener.open(url + urllib.urlencode(data)).read()
        data_ret = json.loads(re_ticket.findall(html)[0])

        if data_ret['retcode'] != '0':
            print data_ret['reason']
            sys.exit(1)
        return data_ret['ticket']

    
    def getToken(self, username, pwd):
        url = 'https://api.weibo.com/oauth2/authorize'
        tokenTicket_ = self.tokenTicket(username, pwd)

        data = {
                'action': 'login',
                'display': 'default',
                'withOfficalFlag': '0',
                'quick_auth': 'null',
                'withOfficalAccount': '',
                'scope': '',
                'ticket': tokenTicket_, 
                'isLoginSina': '',
                'response_type': 'code',
                'regCallback': self.regCallback(), 
                'redirect_uri': self.redirect_uri, 
                'client_id': self.appkey, 
                'appkey62': self.appkey62(),
                'state': '',
                'verifyToken': 'null',
                'from': '',
                'switchLogin': '0',
                'userId': '', 
                'passwd': ''
                }
        
        req = self.opener.open(url, urllib.urlencode(data))
        code_url = req.geturl()
        re_retcode = re.compile(r'code=(.+?)$')
        
        if not self.redirect_uri[7:] in code_url:
            code_url = self.verifyAccess(req.read())
    
        return re_retcode.findall(code_url)[0]

    def verifyAccess(self, html):
        re_uid = re.compile('uid" value="(.+?)"')
        re_verifyToken = re.compile('"verifyToken" value="(.+?)"')

        uid_ = re_uid.findall(html)[0]
        re_verifyToken_ = re_verifyToken.findall(html)[0]

        url = 'https://api.weibo.com/oauth2/authorize'

        data = {
                'display': 'default',
                'action': 'authorize',
                'scope': '',
                'withOfficalFlag': '0',
                'withOfficalAccount': '',
                'ticket': '',
                'isLoginSina': '',
                'response_type': 'code',
                'regCallback': self.regCallback(), 
                'redirect_uri': self.redirect_uri,
                'client_id': self.appkey,
                'appkey62': self.appkey62(),
                'state': '',
                'from': '',
                'uid': uid_,
                'url': 'https://api.weibo.com/oauth2/authorize?client_id=3164632801&redirect_uri=http://github.com/pczb',
                'verifyToken': re_verifyToken_,
                'visible': '0',
                }

        self.opener.addheaders = [('Referer', 'https://api.weibo.com/oauth2/authorize')]
        response = self.opener.open(url, urllib.urlencode(data))
        return response.geturl()

    @staticmethod
    def preProcess(userName, data):
        PRE_LOGIN_URL = 'http://login.sina.com.cn/sso/prelogin.php?'
        PRE_LOGIN_URL += urllib.urlencode(data)

        loginData_rep = re.compile('[(]({.+?})[)]')
        loginData_json = json.loads(loginData_rep.findall(urllib2.urlopen(PRE_LOGIN_URL).read())[0])
        return loginData_json

    @staticmethod
    def encryptPWD(originPWD, login_data):
        rsaPubkey = int(login_data['pubkey'], 16)
        key_10001 = int('10001', 16)

        key = rsa.PublicKey(rsaPubkey, key_10001)
        message = str(login_data['servertime']) + "\t" + str(login_data['nonce']) + "\n" + originPWD
        enPWD = rsa.encrypt(message, key)  
        enPWD = binascii.b2a_hex(enPWD)
        return enPWD    

    def buildAuthUrl(self):
        ret = 'https://api.weibo.com/oauth2/authorize?'
        data = 'client_id=%s' %(self.appkey)
        data += '&redirect_uri=%s' %(self.redirect_uri)
        return ret + data

    def appkey62(self):
        url = self.buildAuthUrl()
        re_62 = re.compile('appkey62" value="(.+?)"')
        return re_62.findall(urllib2.urlopen(url).read())[0]

    def regCallback(self):
        url = self.buildAuthUrl()
        re_62 = re.compile('regCallback" value="(.+?)"')
        return re_62.findall(urllib2.urlopen(url).read())[0]

    def get_access_token(self, code):
        accecc_token = ''
        access_url = 'https://api.weibo.com/oauth2/access_token'
        grant_type = 'authorization_code'
        request = urllib2.Request(access_url)
        data = {}
        data['client_id'] = self.appkey
        data['client_secret'] = self.appsecret
        data['grant_type'] = grant_type
        data['code'] = code
        data['redirect_uri'] = self.redirect_uri
        response = self.opener.open(request,urllib.urlencode(data))
        access_token = json.loads(response.read())['access_token']
        print access_token
        return access_token


