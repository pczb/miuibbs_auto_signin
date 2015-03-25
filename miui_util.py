from weibo import send_weibo
from util import tryExec
import urllib2
import urllib
import cookielib
import sys
import re


def loginErrorHandler(exceptions):
    msg = ""
    msg = " ".join([y for y in set(x.message for x in exceptions)])
#    send_weibo(msg[0:50] + '^^^^^^^^*******""""""')
    print msg
    sys.exit(1)

def getLoginData(htmlpage):
    pattern_pdata = re.compile(r'JSP[_]VAR=[{]\s+([^;]+)\s+[}];')
    ret = {}
    for x in pattern_pdata.findall(htmlpage)[0][:-1].split('\n'):
        key, val = x.split(':', 1)
        key = key.lstrip()
        val = val.rstrip()
        if key[0] == '"':
            key = key[1:-1]
        if 'Para' not in key:
            ret[key] = val[1:-2]
        else:
            ret[key] = val[1:]

    return ret


@tryExec(1, loginErrorHandler, 1)
def login(base_url, userName, password):
    login_url = 'https://account.xiaomi.com/pass/serviceLoginAuth2'
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('user-agent', 'User-Agent:Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us;')]
    page = opener.open(base_url)
    data =  getLoginData(page.read())
    data['user'] = userName
    data['pwd'] = password
    data['json'] = 'true'
    opener.open(login_url, urllib.urlencode(data))
    return opener



