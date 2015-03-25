#coding=utf8
import urllib2
import socket
from poll import Poll
from util import tryExec
from miui_util import login

@tryExec(1) #inorder not to throw exception, follows are as the same
def dailySignIn(opener):
    page = 'http://www.miui.com/home.php?mod=task&do=apply&id=2'
    opener.open(page)

@tryExec(1)
def geekSignIn(opener):
    page = 'http://www.miui.com/home.php?mod=task&do=apply&id=21'
    opener.open(page)

@tryExec(1)
def geekDraw(opener):
    page = 'http://www.miui.com/home.php?mod=task&do=draw&id=21'
    opener.open(page)




def autoRun(userName, password):
    miui_url = 'http://www.miui.com/member.php?mod=logging&action=miuilogin'
    geek_url = 'http://geek.miui.com/index.php?m=member&c=index&a=login'

    opener = login(miui_url, userName, password)
    dailySignIn(opener) 
    
    #geek community;1) first take the task; 2)login geek section
    geekSignIn(opener) 
    geek_opener = login(geek_url, userName, password) 
    geekDraw(opener)

    poller = Poll(opener)
    poller.autoPoll()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print '参数错误'
    socket.setdefaulttimeout(10.0)
    autoRun(sys.argv[1], sys.argv[2])
