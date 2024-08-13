# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 17:43:45 2021
@discribe: douban_comments_spider
@author: 86150
"""
 
#定义爬取信息的函数，其中参数url是爬取书评首页的地址，n是爬取书评的数量
def getInfo(url, n):
    #导入要用到的第三方库
    import requests 
    from bs4 import BeautifulSoup
    import re
    import time
    count = 0 #用于记录书评数量的计数器
    i = 0 #用于控制翻页的计数器
    lis_comments = [] #用于存放书评内容的列表
    lis_stars = [] #用于存放评分的列表
    
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
#用于向服务器发送请求的头部信息
 
    while count<n:
            url_n=url.split('?')[0]+'?start='+str(i)+url.split('?')[1] #调用字符串的split()方法，以'?'为分隔符将URL分成两个字符串，中间加入'?start='+str(i)字符串组成新的URL
            r = requests.get(url_n,headers=header) #调用requests的get（）方法获取页面信息
            soup = BeautifulSoup(r.text, 'lxml') #以'xml'格式解析r.text
            comments = soup.find_all('span','short') #调用soup对象的find_all方法获取具有“short”属性的所有span标签
            pattern = re.compile('<span class="user-stars allstar(.*?) rating"') #调用正则表达式库的compilere（）方法，将正则表达式赋给pattern对象，(.*?)表示获取一个到多个除换行符以外的任意字符，加上？表示非贪婪匹配
            p = re.findall(pattern, r.text) #调用re的findall方法匹配HTML中的所有评分分数（star）
            for item in comments:
                lis_comments.append(item.string) #调用append方法将每一条书评添加到列表中
            for star in p:
                lis_stars.append(int(star)) #调用append方法将每一条评分添加到列表中
            count=len(lis_comments) #获取列表中的书评数目
            i+=20 #star数加上20，爬取下一个页面
            time.sleep(3) #根据豆瓣网的robot协议，每访问一个页面停留3秒钟，以免被当作恶意爬虫
    return lis_comments, lis_stars #返回书评和评分列表，便于被后面的函数调用
 
#定义显示结果的函数，其中参数num是想要显示的书评数量
def showRst(num):
    c,s = getInfo(url, n) #获取getInfo函数的返回值
    print("前%d条书评如下："%n)
    for i in range(num):
        print(i+1,c[i]) #打印出每一条书评及其序号
        print('--------------------------------------------------------------')
    print("前%d条评分的平均值为："%len(s),sum(s)/len(s))  #调用python的内部函数len()和sum(),计算评分的平均值
    
        
if __name__=="__main__": #程序的入口
    url='https://book.douban.com/subject/35196328/comments/?&limit=20&status=P&sort=new_score'
    n=100
    num=80
    getInfo(url, n) #调用getInfo函数获取前n条书评和评分，因为有些书评可能没有评分，所以评分数可能少于书评数
    showRst(num) #showRst函数显示前num条书评和评分的平均值