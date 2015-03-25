#coding=utf8
from util import tryExec
import urllib2
import urllib
import re
import random

class Poll:

    def __init__(self, opener):
        self.opener = opener
        self.failedTimes = 0
        self.succTimes = 0


    def parsePollPage(self, htmlpage):
        pattern_poll_section = re.compile(r'name="poll" method="post"(.+?)<button', re.DOTALL)
        pattern_post_url = re.compile(r'action="([^"]+)"')
        pattern_form_hash = re.compile(r'"formhash" value="([^"]+)"')
        pattern_poll_type = re.compile(r'<strong[^>]*>(.+?)<.+?>')
        pattern_poll_ans = re.compile(r'name="pollanswers\[\]" value="(\d+)".+?<label[^>]+>(.+?)<', re.DOTALL) 

        ret = []
        for section_match in pattern_poll_section.finditer(htmlpage):
            section_text = section_match.groups()[0]
            post_url = pattern_post_url.search(section_text).groups()[0]
            ret.append(post_url)
            form_hash = pattern_form_hash.search(section_text).groups()[0]
            ret.append(form_hash)
            pool_type = pattern_poll_type.search(section_text).groups()[0]
            
            for x in pattern_poll_ans.findall(section_text):
                if "国际" in x[1] or "酱油" in x[1]:
                    ret.append(x[0])
                    return ret
            ret.append(x[0])
        
        return ret

    def miui_poll(self, thread_url):
        htmlpage = self.opener.open(thread_url).read()
        ret = self.parsePollPage(htmlpage)
        data = {'formhash': ret[1], 'pollanswers[]': ret[2],
                'pollsubmit':'true'}

        print data

        ret[0] = "".join(ret[0].split('amp;'))
        request = self.opener.open('http://www.miui.com/' + ret[0], data = urllib.urlencode(data))

    @tryExec(5)
    def getPhonesForumPage(self):
        pattern_forum_id = re.compile(r'p_pic">[^<]*<a href="forum-(\d+)-')
        htmlpage = self.opener.open('http://www.miui.com/gid-1.html#tabs_0').read()
        ret = []
        for x in pattern_forum_id.findall(htmlpage):
            ret.append(x)
        return ret

    def getPollUrl(self, url):
        htmlpage = urllib2.urlopen(url).read()
        pattern_poll_url = re.compile(r'(thread-\d+-\d+-\d+.html)" onclick')

        for x in pattern_poll_url.findall(htmlpage):
            ret.append(x)
        return ret



    def autoPoll(self):
        phonesForum = self.getPhonesForumPage()
        if phonesForum == None:
            return 

        pollUrls = []
        visited = set()
        succCount = 0
        tryCount = 0
        poll_list_url = 'http://www.miui.com/forum.php?mod=forumdisplay&fid=%s&filter=specialtype&specialtype=poll'

        def singlePoll():
            pollUrls += self.getPollUrl(poll_list_url%(phonesForum[tryCount if tryCount < len(phonesForum) else len(phonesForum) - 1]))
            random.shuffle(pollUrls)
            if pollUrls[0] not in visited:
                thread_url = 'http://www.miui.com/' + pollUrls[0]
                self.miui_poll(thread_url)
                succCount += 1

        
        while succCount < 10 and tryCount < 20:
            try:
                singlePoll()
            except Exception, e:
                raise
                print e.message
            finally:
                print pollUrls
                visited.add(pollUrls[0])
                tryCount += 1
        


if __name__ == '__main__':
    import socket
    socket.setdefaulttimeout(10)
    from miui_util import login
    miui_url = 'http://www.miui.com/member.php?mod=logging&action=miuilogin'
    opener = login(miui_url, '', '')
    poller = Poll(opener)
#    poller.miui_poll('http://www.miui.com/thread-2486706-1-1.html')
    poller.autoPoll()

