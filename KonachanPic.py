#-*- coding:utf-8 -*-
import sys,os
import re
import time
import urllib2
#import htmlcontent
from sgmllib import SGMLParser


class PICParser(SGMLParser):

    data=[]
    ulswi=False
    """Parse the web pages"""
    def start_ul(self,attrs):
        for k,v in attrs:
            if k=='id' and v=='post-list-posts':
                self.ulswi=True

    def end_ul(self):
        self.ulswi=False

    def start_a(self,attrs):
        for k,v in attrs:
            if k=='href' and self.ulswi==True and v[0]=='h':
                #print v
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

def download(dataset,num,path):
    i=0
    for url in dataset:
        if i>=num:
            filenum='%d' %i
            filename=os.path.basename(url)
            print "正在下载第"+filenum+"张图片……"
            socket=urllib2.urlopen(url)
            data=socket.read()
            picpath=path
            picpath=picpath+filename
            with open(picpath,"wb") as jpg:
                jpg.write(data)
            socket.close()
            print "第"+filenum+"张图片下载完毕！"
        i+=1

if __name__=="__main__":
    desc()
    las,nex=raw_input("请输入页数范围:").split(' ')
    lasnum=int(las)
    nexnum=int(nex)
    startnum=raw_input("从第几张图片开始下载？")
    filepath=raw_input("将图片下载到哪个盘？")
    filepath=filepath+r":/downloadpic/"
    if not os.path.exists(filepath):
        os.mkdir(filepath)

    pp=PICParser()
    url="http://konachan.com/post?page="
    #htmlc=htmlcontent.htmlcontent
    #pp.feed(htmlc)
    #DataSet=pp.getData()
    j=lasnum
    for j in range(lasnum,nexnum+1):
        print "正在下载第 %d 页" % j
        dataurl=url+str(j)
        htmlcontent=getUrl(dataurl)
        pp.feed(htmlcontent)
        DataSet=pp.getData()
        if j==lasnum:
            download(DataSet,int(startnum),filepath)
        else:
            download(DataSet,1,filepath)
        print "第 %d 页下载完毕！" % j
        j=j+1
    print "本次下载任务圆满结束！！"
    #download(DataSet,0)
