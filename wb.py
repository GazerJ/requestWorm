# -*- coding: utf-8 -*-

import requests
import json
import csv
import datetime
from bs4 import BeautifulSoup



def getweibo(url):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'MWeibo-Pwa': '1',
        'Referer': 'https://m.weibo.cn/search?containerid=100103type%3D1%26q%3Dpython',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'X-XSRF-TOKEN': '7f90eb',
    }

    response = requests.get(url,headers=headers)
    print(response)
    jsondata = json.loads(response.text)['data']['cards']

    for jd in jsondata:
        card_group = jd['card_group']
        if "mblog" in str(card_group):
            for cg in card_group:
                try:
                    mblog = cg['mblog']['text']  # 微博内容
                    mblog = BeautifulSoup(mblog,'lxml').text
                    
                    reposts = cg['mblog']['reposts_count']  # 转发数
                    comments = cg['mblog']['comments_count']  # 评论数
                    attitudes = cg['mblog']['attitudes_count']  # 点赞数
                                        
                except:
                    pass
                else:
                    created = cg['mblog']['created_at'].split(' ') # 发布时间
                    created_at = [created[1], created[2], created[3], created[5]]
                    list2 = [str(i) for i in created_at]
                    list3=' '.join(list2)
                    time = datetime.datetime.strptime(list3, '%b %d %H:%M:%S %Y')
                    if time.year < tarYear:
                        return 0
                    if time.year == tarYear:
                        if time.month < tarMon:
                            return 0
                        if time.month == tarMon:
                            if time.day <tarDay:
                                return 0
                    data = [mblog, time, reposts, comments, attitudes]
                    saveCsv('微博内容',data)
                    return 1

def runx():
    x=1
    label=1
    while label:
        
        #page
        print(f"爬取第{x} 页中....")
        url = f"https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%23劳动法%23&page_type=searchall&page={x}" # 可更喜欢关键词
        label=getweibo(url)
        x+=1



def saveCsv(filename,content):
    "保存数据为CSV文件"
    fp = open(f'{filename}.csv', 'a+', newline='', encoding='utf-8-sig')
    csv_fp = csv.writer(fp)
    csv_fp.writerow(content)
    fp.close()
    print(f"写入了{content}")
tarYear=2021
tarMon=6
tarDay=1


if __name__ == '__main__':
    runx()

