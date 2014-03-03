#-*- coding:utf-8 -*-
import sys,os
import re
import time
import urllib2
import threading
#import htmlcontent
from sgmllib import SGMLParser


url = "http://konachan.com/post?page="
startpage = endpage = startnum = 1
filepath = ""
threadnum = 3
event = threading.Event()
lock = threading.Lock()

class PageParser(SGMLParser):

    data = []
    ulswi = False
    """Parse the web pages"""
    def start_ul(self,attrs):
        for k,v in attrs:
            if k == 'id' and v == 'post-list-posts':
                self.ulswi = True

    def end_ul(self):
        self.ulswi = False

    def start_a(self,attrs):
        for k,v in attrs:
            if k == 'href' and self.ulswi == True and v[0] == 'h':
                self.data.append(v)

    def getData(self):
        return self.data

def getUrl(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT6.1; en-US; rv:1.9.1.6) Firefox/3.5.6'}
    req = urllib2.Request(url, headers=headers)
    content = urllib2.urlopen(req).read()
    print "正在解析:%s" % url
    type = sys.getfilesystemencoding()
    return content.decode("UTF-8").encode(type)

def desc():
    print """
        图片下载软件简要使用说明
        爬取konachan.com上的图片
        输入页数范围(例:15 20)回车，即可下载15页到20页的所有图片
        紧接着输入开始下载的位置(例:5)，即可从15页的第5张图片开始下载
        输入盘符(例如:d)，即可将图片下载到d:/downloadpic/文件夹中
        """

def download(url,path):
    global threadnum
    if threadnum <= 0:
        event.clear()
    else:
        if lock.acquire():
            threadnum = threadnum - 1
            lock.release()
        event.set()

    filename = os.path.basename(url)
    socket = urllib2.urlopen(url)
    data = socket.read()
    path = path + filename
    print "正在下载图片"
    with open(path,"wb") as jpg:
        jpg.write(data)
    socket.close()

    if lock.acquire():
        threadnum = threadnum + 1
        lock.release()
    event.set()

def page_download(low,up):
    up = up + 1
    global filepath
    for pagenum in range(low,up):
        print "正在下载第 %d 页" % pagenum
        dataurl = url + str(pagenum)
        htmlcontent = getUrl(dataurl)
        parser.feed(htmlcontent)
        DataSet = parser.getData()
        if pagenum == startpage:
            for i in range(startnum,len(DataSet)):
                downthread = threading.Thread(target=download,args=(DataSet[i],filepath))
                downthread.start()
                event.wait()
                #print "正在下载第 %d 张图片" % i
                #download(DataSet[i],filepath)
        else:
            for i in range(1,len(DataSet)):
                print "正在下载第 %d 张图片" % i
                download(DataSet[i],filepath)
        print "第 %d 页下载完毕！" % pagenum


def init():
    las,nex=raw_input("请输入页数范围:").split(' ')
    startpage=int(las)
    endpage=int(nex)
    startnum=raw_input("从第几张图片开始下载？")
    global filepath
    filepath=raw_input("将图片下载到哪个盘？")
    filepath=filepath+r":/downloadpic/"
    if not os.path.exists(filepath):
        os.mkdir(filepath)


if __name__=="__main__":
    parser=PageParser()
    desc()
    init()
    #htmlc=htmlcontent.htmlcontent
    #pp.feed(htmlc)
    #DataSet=pp.getData()
    page_download(startpage,endpage)
    print "本次下载任务圆满结束！！"
    #download(DataSet,0)
