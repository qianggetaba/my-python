
#encoding:utf-8

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
file = codecs.open("test_text.txt", "a", "utf-8")

divmain = allxing.find_all('div',{'class':'main_'})
divcontainer = divmain[0].find_all('div',{'class':'container'})
divrow = divcontainer[0].find_all('div',{'class':'row'})
divonexing = divrow[0].find_all('div')[1]
allxinga = divonexing.find_all('a')
for onexinga in allxinga:
    # print(onexinga['href'])
    onexingurlbase='http:'+ onexinga['href']
    # print(onexingurlbase)
    # 开始遍历一个姓下的名字
    file.write('\n\n')
    for i in range(1, 20):
        onexinglisturl = onexingurlbase+"/name_list_"+str(i)+".html"
        print('url:'+onexinglisturl),
        htmlContent=getHtml(onexinglisturl)
        if (htmlContent is None):
            break

        allxm = BeautifulSoup(htmlContent,features='html.parser')
        allxmlist = allxm.find_all('div',{'class':'namelist'})
        for onexm in allxmlist:
            xingming = onexm.find_all('div')[0]
            # print xingming.getText()
            
            file.write(xingming.getText())
            file.write('\n')
        file.flush
        print('done')
        
file.close()

