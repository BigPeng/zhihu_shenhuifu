#!encoding=utf-8
import gzip
import cStringIO
import chardet
from bs4 import BeautifulSoup
import urllib
import urllib2
import time
from datetime import datetime
import math
import sys
def getPage(url):
    try:
        time.sleep(1)
        web = urllib.urlopen(url)
        page = web.read()
        web.close()
        return page
    except:
        return None

def formatStr(s):
    s = s.replace('\n',' ').replace('\t',' ')
    return s.strip()

def getArticle(url):
    page = getPage(url)
    pageSoup = BeautifulSoup(page)
    title = str(pageSoup.title).replace('<title>','').replace('</title>','').strip()
    item = pageSoup.find_all('div',{'class':'zm-item-answer'})
    if item is None or len(item) == 0:
        return None
    anwser = item[0].find('div',{'class':'fixed-summary zm-editable-content clearfix'}).get_text().strip()
    vote = item[0].find('div',{'class':'zm-item-vote-info '}).get('data-votecount').strip()
    anwser = formatStr(anwser)
    ans_len = len(anwser)
    if ans_len > 100:
        anwser = anwser[0:100]
    title = formatStr(title)
    out = [title, anwser, str(ans_len),vote,url]
    return out

def getQuestions(start,offset='20'):
    #cookies = urllib2.HTTPCookieProcessor()
    #opener = urllib2.build_opener(cookies)
    #urllib2.install_opener(opener)

    header = {"Accept":"*/*",
    "Accept-Encoding":"gbk,utf-8,gzip,deflate,sdch",
    "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
    "Connection":"keep-alive",
    "Content-Length":"64",
    "Content-Type":"application/x-www-form-urlencoded; charset=utf-8",
    'Cookie':'*************'
    "Host":"www.zhihu.com",
    "Origin":"http://www.zhihu.com",
    "Referer":"http://www.zhihu.com/log/questions",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36",
    "X-Requested-With":"XMLHttpRequest"
    }

    parms = {'start':start,
            'offset':offset,
            '_xsrf':'*************'}
    url = 'http://www.zhihu.com/log/questions'
    req = urllib2.Request(url,headers=header,data=urllib.urlencode(parms))
    content = urllib2.urlopen( req ).read()
    html = gzip.GzipFile(fileobj = cStringIO.StringIO(content)).read()
    html = eval(html)['msg'][1]
    pageSoup = BeautifulSoup(html)
    questions = []
    items = pageSoup.find_all('div',{'class':'zm-item'})
    for item in items:
        url = item.find_all('a',{'target':'_blank'})[0].get('href').rsplit('/',1)[1]
        questions.append(url)
    lastId = items[-1].get('id').split('-')[1]
    return questions,lastId
    
def craw():
    wf = open('zhihu.txt','a+')
    domain = 'http://www.zhihu.com/question/'
    #lastId = '404659437'
    lastId = '389059437'
    for i in xrange(10000):
        print i,lastId
        ques,lastId = getQuestions(lastId)
        for q in ques:
            try:
                out = getArticle(domain+q)
            except:
                continue
            if out == None:
                continue
            for j in xrange(len(out)):
                each = out[j]
                if j == 1:
                    each = each.encode('utf-8')
                wf.write(each)
                wf.write('\t')
            wf.write('\n')
    wf.close()
if __name__ == '__main__':
    craw()
