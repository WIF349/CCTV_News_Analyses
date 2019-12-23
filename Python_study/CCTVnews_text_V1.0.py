#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
__author__ = '王益夫'
__mtime__ = '2019/12/20'
'''
'''第一个版本，用来获取文件的链接和信息，并存储在txt文件中'''


#import 相关的库
import requests
from bs4 import BeautifulSoup
import io
import sys
import re
import os
import time
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
#改变标准输出的默认编码，修改如下报错信息
#UnicodeEncodeError: 'gbk' codec can't encode character '\u2039' in position 9064: illegal multibyte sequence


def getRespose(url):
    '''requests获取response文本'''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('链接异常：'+ url)
        return False


def getNowUrls(url,mode=1):
    '''解析列表文章的链接和文章名'''
    URL_all_set = set()
    URL_next_page_set = set()
    soup = BeautifulSoup(getRespose(url), 'html.parser')
    if mode == 1 :
        #try:
        for line in soup.body.find(class_='xwlist').find_all(name = 'a'):
            url_point = line.attrs['href']
            #print(url_point)
            #print(URL_all)
            if url_point not in URL_all_set:
                URL_all_set.add(url_point)
        return URL_all_set
        # except:
        #     print('页面url获取失败,Urls_list')
        #     return False
    else:
        # try:
        url_next = soup.body.find(class_='page now-page').next_sibling.next_sibling.attrs['href']
        if url_next not in URL_next_page_set:
            URL_next_page_set.add(url_next)
            return URL_next_page_set
        else:
            print('链接: ' + url_next + '已存在！')
            return False
        # except:
        #     print('获取下一页地址失败,Url_next')
        #     return False


def gettext(url):
    try:
        demo = getRespose(url)
        soup_text = BeautifulSoup(demo, 'html.parser')

        Text_title = soup_text.head.title.string
        Text_text = soup_text.body.find(attrs={'class':'text_content'}).p.string
        return Text_title, Text_text
    except:
        print('新闻页面解析失败！')
        return False


def TextWriter(url, file_path=r'.\temp', file_name=r'新闻联播.txt'):
    file_all = file_path + '\\' + file_name
    if  gettext(url):
        Get_text_list = gettext(url)
    if not os.path.exists(file_path):  # os库判断路径是否存在
        os.mkdir(file_path)  # 不存在创建路径
    try:
        with open(file_all, r'a+', encoding="utf8") as f:
            f.write(Get_text_list[0] + '\n')
            f.write(str(Get_text_list[1]) + '\n')  # 此处写入失败的原因为该文本为list格式，需要转化为str
            f.flush()  # 将缓存写入
            f.close()
            print('文件写入成功')
    except:
        print('文本写入失败')
        return False

def main(url):
    URL_all = getNowUrls(url,1)
    URL_next_page = getNowUrls(url,2)
    for url_line in list(URL_all):
        TextWriter(url_line, file_path=r'.\temp', file_name=r'新闻联播.txt')
        URL_all.remove(url_line)   #集合为空会报错的问题。
        print('采集列表:',URL_all)
        print('下一页:' , URL_next_page)
        if len(URL_all) == 0 and len(URL_next_page) == 1:
            Next_url = list(URL_next_page)[0]
            URL_next_page.remove(Next_url)
            time.sleep(1)
            main(Next_url)



if __name__ == '__main__':
    url = r'http://www.xwlb.top/xwlb.html'
    main(url)

