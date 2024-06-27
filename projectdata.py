from bs4 import BeautifulSoup #网页分析
import re #正则表达式， 进行文字匹配
import urllib.request, urllib.error #制定url, 获取网页数据
import xlwt #进行excel操作
import sqlite3 #进行sqlite数据库操作


def main():
    baseurl = "https://movie.douban.com/top250?start="

    #1：爬取网页
    datalist = getData(baseurl)
    savepath = ".\\豆瓣电影top250.xls"
    #2：解析数据
    #3：保存数据
    # saveData(savepath)
    # askURL("https://movie.douban.com/top250?start=")
findLink = re.compile(r'<a href="(.*?)">') 
findImgSrc  = re.compile(r'<img.*src="(.*?)"', re.S) #创建正则表达式对象,表示规则（字符串的模式)
#影片链接的要求筛选条件, Re.S 让换行符包含在其中
# findImgSrc = re.compile(r'')
#影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
#影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')

#找到评价人数
findJudge = re.compile(r'<span>(\d*)人评价<\span>')

#找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')

#找到影片的相关内容
findBd = re.compile(r'<p class="">(.*) </p>', re.S)


def getData(baseurl):
    datalist =[]
    for i in range(0, 1): #调用获取页面信息的函数，十次
        url = baseurl + str(i * 25)
        html = askURL(url)     #保存获取到的网页源码

        
        #2. 逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_= "item"):
            data = [] #保存一部电影的所有信息
            item = str(item)
            print(item)
            #影片详情的链接
            link = re.findall(findLink, item)[0]
            data.append(link)
            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)
            titles = re.findall(findTitle, item) #片名可能只有一个中文名， 没有外文名
            if (len(titles) == 2):
                ctitle = titles[0]          #添加中文名
                data.append(ctitle)
                atitle = titles[1].replace("/","") #去掉无关的符号
                data.append(otitle)           #添加外文名
            else:
                data.append(titles[0])
                data.append(' ')   #外文名字留空
            rating  = re.findall(findRating, item)[0]
            data.append(rating)

            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)     #评价人数

            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace(". ","") #去掉句号
                data.append(inq)   #添加概述
            else:
                data.append(" ") #留空
            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br/(\s+)?/>(\s+)?', " ", bd) #去掉<br/>
            bd = re.sub('/', " ", bd) #替换/
            data.append(bd.strip())    #去掉前后的空格

            datalist.append(data)
            print(link) #re库用正则表达式来查找指定字符串
        #print(item) #测试：查看电影item全部信息') #查找符合要求的内容
    print(datalist)
    return datalist


def saveData(savepath):
    print("saving..")


#得到指定一个url的网页内容
def  askURL(url):
    head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"}
#用户代理， 表示告诉豆瓣服务器， 我们是什么类型的机器，浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html



if __name__ =="__main__":
    main()
