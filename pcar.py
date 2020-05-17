import urllib.request
from bs4 import BeautifulSoup

with urllib.request.urlopen('http://car.bitauto.com/qichepinpai/') as url:
    s = url.read()

soup = BeautifulSoup(s,features='html.parser')
# print(soup.prettify())

uls = soup.find_all('ul',{'class':'list_pic'})
for ul in uls:
    lis = ul.find_all('li')
    for li in lis:
        print(li.find('a')['title'])
        htmlstr = urllib.request.urlopen(li.find('a')['href']).read()
        soup = BeautifulSoup(htmlstr,features='html.parser')
        div = soup.find('div',{'id':'data_table_MasterSerialList_0'})
        lis = div.find_all('li',{'class','name'})
        for li in lis:
            print(li.find('a').getText()+'  ',end='')
        print()

