#coding=utf8
import os
import subprocess
import sys
import time
from weibo import send_weibo
from weibo import getWeiboByID
       
def getOldIP():
    oldIP = ''
    if not os.path.exists('/home/pczb/miui_bbs/weibo_id.ini'):
        return oldIP
    with open("/home/pczb/miui_bbs/weibo_id.ini") as ifd:
        weiboid = ifd.readline().rstrip()
        if weiboid != '':
            weibo = getWeiboByID(weiboid)
            if weibo != None and 'id' in weibo:
                oldIP = weibo["text"]

    return oldIP


def updateIP():
    newIP = getDeviceIP('eth1')
    oldIP = getOldIP()
    if newIP != oldIP:
        print newIP, '###',oldIP
        weiboid = send_weibo(newIP)
        if weiboid != None and weiboid != '':
            outfile = open("/home/pczb/miui_bbs/weibo_id.ini","w")
            outfile.write(weiboid)
            outfile.close()
    
def getDeviceIP(interface):
    subp = subprocess.Popen("ifconfig "+interface,stdout = subprocess.PIPE,shell = True)
    outmsg = subp.communicate()[0]
    ipaddr = outmsg.split('\n')[1].split()[1]
    last_ipaddr = ipaddr.split('.')[3]
    return last_ipaddr
	
if __name__ == "__main__":
    updateIP()
