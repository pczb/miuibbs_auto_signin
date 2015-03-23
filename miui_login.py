import urllib2
import urllib
import re
import sys
import cookielib


def getLoginUrl(htmlpage):
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

def dailySignIn(opener):
    page = 'http://www.miui.com/home.php?mod=task&do=apply&id=2'
    opener.open(page)

def geekSignIn(opener):
    page = 'http://www.miui.com/home.php?mod=task&do=apply&id=21'
    opener.open(page)

def geekDraw(opener):
    page = 'http://www.miui.com/home.php?mod=task&do=draw&id=21'
    opener.open(page)

def login(base_url, userName, password):
    login_url = 'https://account.xiaomi.com/pass/serviceLoginAuth2'
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('user-agent', 'User-Agent:Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us;')]
    page = opener.open(base_url)
    data =  getLoginUrl(page.read())
    data['user'] = userName
    data['pwd'] = password
    data['json'] = 'true'
    opener.open(login_url, urllib.urlencode(data))
    return opener

miui_url = 'http://www.miui.com/member.php?mod=logging&action=miuilogin'
geek_url = 'http://geek.miui.com/index.php?m=member&c=index&a=login'

def bothSignIn(userName, password):
    opener = login(miui_url, userName, password)
    dailySignIn(opener)
    geekSignIn(opener)
    geek_opener = login(geek_url, userName, password)
    geekDraw(opener)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print '参数错误'
    bothSignIn(sys.argv[2], sys.argv[3])
