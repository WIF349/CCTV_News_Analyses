#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
__author__ = '王益夫'
__mtime__ = '2019/12/20'
'''
'''
版本修改：
V 1.0:用来获取文件的链接和信息，并存储在txt文件中；
V 1.0.1：参照调整headers，新增logging模块输入日志信息；
V 1.0.2: 独立写文本函数，增加已采集列表统计, 修复末页bug不退出爬虫问题。

'''


#import 相关的库
import requests
from bs4 import BeautifulSoup
import sys
import os
import time
import random
import logging


#方法1：设置文件写入，不设置输出控制台
# LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
# logging.basicConfig(filename='./temp/CCTV_news.log', level=logging.info, format=LOG_FORMAT, datefmt=DATE_FORMAT)

#方法2：handler同时输出到控制台和文件
logger = logging.getLogger()
logger.setLevel('WARNING')
BASIC_FORMAT = "%(asctime)s:%(levelname)s:%(message)s"
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
chlr = logging.StreamHandler() # 输出到控制台的handler
chlr.setFormatter(formatter)
chlr.setLevel('INFO')  # 也可以不设置，不设置就默认用logger的level
fhlr = logging.FileHandler('./temp/CCTV_news.log') # 输出到文件的handler
fhlr.setFormatter(formatter)
logger.addHandler(chlr)
logger.addHandler(fhlr)

#增加多个浏览器头，避免检测
headers_list = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
]

global headers
headers = {'User-Agent': random.choice(headers_list)}

def getRespose(url):
    '''requests获取response文本'''
    global ERR_List
    global headers
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except Exception as e:
        #print('链接异常：'+ url)
        logging.error('链接异常：%s', url)
        ERR_List.add(url)
        raise e


def getNowUrls(url,mode=1):
    global ERR_List
    ''' 解析列表文章的链接和文章名 '''
    URL_all_set = set()
    URL_next_page_set = set()
    soup = BeautifulSoup(getRespose(url), 'html.parser')
    if mode == 1:
        try:
            for line in soup.body.find(class_='xwlist').find_all(name='a'):
                url_point = line.attrs['href']
                #logging.warning('采集列表链接：%s', url_point)
                if url_point not in URL_all_set:
                    URL_all_set.add(url_point)
            return URL_all_set
        except Exception as e:
            raise e
            logging.error('采集列表链接失败：%s', url)
            ERR_List.add(url)
            return False

    else:
        try:
            url_next = soup.body.find(class_='page now-page').next_sibling.next_sibling.attrs['href']
            if url_next == url:
                URL_next_page_set.add('end')
                logging.warning('已到末页：%s', url_next)
                return URL_next_page_set
            else:
                if url_next not in URL_next_page_set:
                    URL_next_page_set.add(url_next)
                    return URL_next_page_set
                else:
                    logging.warning('链接已存在：%s', url_next)

        except:
            logging.error('获取下一页链接失败：%s', url)
            ERR_List.add(url)
            return False


def pageParsing(url):
    global ERR_List
    try:
        demo = getRespose(url)
        soup_text = BeautifulSoup(demo, 'html.parser')
        textTitle = soup_text.head.title.string
        textContent = []
        for line in soup_text.body.find(attrs={'class': 'text_content'}).find_all(name='p'):
            textContent.append(line.string)
            #针对多个P标签，获取对应的string内容
        logging.warning('新闻解析成功：%s', url)
        if len(textTitle) != 0 or len(textContent) != 0:
            return textTitle, str(textContent)
        else:
            logging.error('标题或正文解析失败： %s', url)
    except:
        logging.error('新闻页面解析失败： %s', url)
        ERR_List.add(url)
        return False


def textWrite(url_title, url_text, file_path=r'.\temp', file_name=r'新闻联播.txt'):
    file_all = file_path + '\\' + file_name
    if not os.path.exists(file_path):  # os库判断路径是否存在
        os.mkdir(file_path)  # 不存在创建路径
    try:
        with open(file_all, r'a+', encoding="utf8") as f:
            f.write(url_title + '\n')
            f.write(url_text + '\n')  # 此处写入失败的原因为该文本url_text内文本为list格式，需要转化为str
            f.flush()  # 将缓存写入
            f.close()
            logging.warning('文件写入成功：%s', url_title)
            return True
    except:
        #print('文本写入失败')
        logging.error('文件写入失败：%s', url_title)
        return False


def main(url):
    global All_List
    URL_all = getNowUrls(url, 1)
    URL_next_page = getNowUrls(url, 2)
    # logging.warning('采集列表：%s', URL_all)
    # logging.warning('下一页：%s', URL_next_page)
    for url_line in list(URL_all):
        time.sleep(random.random())
        parseText = pageParsing(url_line)
        if parseText:
            url_title = parseText[0]
            url_text = str(parseText[1])
            print(url_title,url_text)
            #logging.warning('采集中的文本：%s  |   %s', url_title, url_text)
            textWrite(url_title, url_text, file_path=r'.\temp', file_name=r'新闻联播.txt')
        URL_all.remove(url_line)
        All_List.add(url_line)
    if 'end' in URL_next_page:
        logging.error('已到末页：%s', url_line)
        logging.error('采集结束，共采集页面： %s ， 错误页面： %s', len(All_List), len(ERR_List))
        sys.exit()
    else:
        if len(URL_all) == 0 and len(URL_next_page) == 1:
            Next_url = list(URL_next_page)[0]
            URL_next_page.remove(Next_url)
            time.sleep(5)
            main(Next_url)


if __name__ == '__main__':
    #url = r'http://www.xwlb.top/xwlb.html'
    All_List = set()
    ERR_List = set()
    url = r'http://www.xwlb.top/xwlb_709.html'
    logging.warning("输入的url为：%s", url)
    main(url)
