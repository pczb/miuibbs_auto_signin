#coding=utf8
from util import tryExec
import urllib2
import urllib
import json

def defaultWeiboErrorHandler(*args):
    for exception in args:
        print exception
       

@tryExec(1)
def get_access_token():
    accecc_token = ''
    client_id = 
    access_url = 'https://api.weibo.com/oauth2/access_token'
    grant_type = 'authorization_code'
    redirect_uri = 'http://github.com/pczb'
    request = urllib2.Request(access_url)
    data = {}
    data['client_id'] = client_id
    data['client_secret'] = client_secret
    data['grant_type'] = grant_type
    data['code'] = code
    data['redirect_uri'] = redirect_uri
    response = urllib2.urlopen(request,urllib.urlencode(data))
    access_token = json.loads(response.read())['access_token']
    print access_token


def getCommonData(data = {}):
    access_token = 
    data["access_token"] = access_token
    return urllib.urlencode(data)
        
@tryExec(3)
def send_weibo(message):
    url_sendWeibo = 'https://api.weibo.com/2/statuses/update.json'
    data = {}
    data['status'] = message
    data = getCommonData(data)

    httpreq = urllib2.Request(url_sendWeibo)
    response = urllib2.urlopen(httpreq, data).read()
    jsonobj = json.loads(response)
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

