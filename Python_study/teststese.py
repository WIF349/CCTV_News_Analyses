#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
__author__ = '王益夫'
__mtime__ = '2019/12/20'
'''

from bs4 import BeautifulSoup
import requests

def getRespose(url):
    '''requests获取response文本'''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except Exception as e:
        print('链接异常：'+ url)
        raise e


url = r'http://www.xwlb.top/xwlb_709.html'
url2 = r'http://www.xwlb.top/28321.html'
soup = BeautifulSoup(getRespose(url), 'html.parser')
url_next = soup.body.find(class_='page now-page').next_sibling.next_sibling.attrs['href']
print(url_next)


soup_text = BeautifulSoup(getRespose(url2), 'html.parser')
Text_text = soup_text.body.find(attrs={'class': 'text_content'}).find_all(name='p')
print(Text_text)
#url_now = soup.body.find(class_='page now-page').previous_sibling.next_sibling.attrs['href']

#print(url_now)

