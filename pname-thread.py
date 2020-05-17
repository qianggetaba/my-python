
#encoding:utf-8

import threading
import codecs
import urllib2
from bs4 import BeautifulSoup

def getHtml(urlStr):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    request = urllib2.Request(urlStr, headers = header)
    try:
        response = urllib2.urlopen(request)
        return response.read()
    except urllib2.URLError as e:
        print e
    except urllib2.HTTPError, e:
        if (e.code == 404):
            return
    except:
        return
    return

allxing = BeautifulSoup(getHtml('http://www.resgain.net/xsdq.html'),features='html.parser')

divmain = allxing.find_all('div',{'class':'main_'})
divcontainer = divmain[0].find_all('div',{'class':'container'})
divrow = divcontainer[0].find_all('div',{'class':'row'})
divonexing = divrow[0].find_all('div')[1]
allxinga = divonexing.find_all('a')

xingBaseUrlList=[]
for onexinga in allxinga:
    xingBaseUrlList.append('http:'+ onexinga['href'])

# xingBaseUrlList=xingBaseUrlList[0:5]
# print(xingBaseUrlList)

# 多线程读取放入list，最后写入文件
allFinalXM=[]
xmIndex=0
threadLock = threading.Lock()

def getOneXing():
    global xmIndex
    global allFinalXM
    taskCount=0
    oneXingList=[]
    threadName=threading.current_thread().name
    while True:
        threadLock.acquire()
        if (xmIndex + 1 >len(xingBaseUrlList)):
            print( threadName+" TaskDone:"+str(taskCount))
            if (len(oneXingList) > 0):
                allFinalXM.append(oneXingList)
            threadLock.release()
            return
        
        print(threadName +" get:"+str(xmIndex))
        onexingurlbase=xingBaseUrlList[xmIndex]
        xmIndex+=1

        print onexingurlbase+"\n"
        threadLock.release()

        # for i in range(1, 3):
        for i in range(1, 30):
            onexinglisturl = onexingurlbase+"/name_list_"+str(i)+".html"
            print(threadName+'-url:'+onexinglisturl+"\n"),
            htmlContent=getHtml(onexinglisturl)
            print('htmlDone '),
            if (htmlContent is None):
                break

            taskCount+=1
            allxm = BeautifulSoup(htmlContent,features='html.parser')
            allxmlist = allxm.find_all('div',{'class':'namelist'})
            for onexm in allxmlist:
                xingming = onexm.find_all('div')[0]
                oneXingList.append(xingming.getText())
            print('taskDone ')

thread_list = []
for i in range(20):
    t = threading.Thread(target=getOneXing)
    thread_list.append(t)

for t in thread_list:
    t.setDaemon(True)
    t.start()

print('wait sub thead')
for t in thread_list:
    t.join()

print('sub thread done:'+str(len(xingBaseUrlList)) +" :"+str(xmIndex)+" :"+str(len(allFinalXM)))

file = codecs.open("test_text.txt", "a", "utf-8")
for oneList in allFinalXM:
    for oneXM in oneList:
        file.write(oneXM)
        file.write('\n')

file.flush
file.close()
print('done')
