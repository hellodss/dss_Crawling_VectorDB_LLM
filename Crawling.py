#-*- encoding:utf-8 -*-
import requests
import json
import re
from bs4 import BeautifulSoup

seed = "https://cloud.tencent.com/document/product/1709"
baseUrl="https://cloud.tencent.com"
appendUrlList=[]
appendDataList = []

# 获取各栏目URL
def getCrawl(seed):
    seeds = []
    seeds.append(seed)
    textdata = requests.get(seed).text
    soup = BeautifulSoup(textdata,'lxml')
    nodes = soup.select("ul.rno-learning-path-section-list.list-3 li a")
    # print("nodes",nodes)
    
    # 调试信息：检查 nodes 是否为空
    if not nodes:
        print("未找到预期元素，网页内容如下：")
        print(textdata)
        return
    
    seeds.append(nodes)
    getChild(nodes) 

def getChild(nowObj):
     if nowObj is not None:
        for n in nowObj:
            links= n["href"]
            data={"title":n["title"],"link":links}
            appendUrlList.append(data)
            if n.get("children") is not None:
                getChild(n.get("children"))
                
                
def crawlData():
    getCrawl(seed)
    count=0
    for data in appendUrlList:
        url = data["link"]
        print(data["title"]+"        "+data["link"])
        # print(url)
        textdata = requests.get(url).text
        soup = BeautifulSoup(textdata,'lxml')
        nodes = soup.select("div.J-markdown-box")
        if nodes is not None and len(nodes)>0:
            text = nodes[0].get_text()
            text = text[:1000]
            stringText = re.sub('\n+', '\n', text)
            data={"url":url,"title":data["title"],"text":stringText}
            appendDataList.append(data)
        # count=count+1
        # if count>6:
    return appendDataList

if __name__ == "__main__":
    data_list = crawlData()
    print(f"获取的数据条数: {len(data_list)}")
    for i, data in enumerate(data_list[:5]):  # 打印前5条数据
        print(f"数据 {i+1}:")
        print(f"URL: {data['url']}")
        print(f"标题: {data['title']}")
        print(f"文本前100字: {data['text'][:100]}...")
        print("-" * 40)
