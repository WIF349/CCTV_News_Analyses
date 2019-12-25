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
V 1.0.2 增加单元测试模块
'''

import unittest
import CCTVnews_test.V1.0.1


class Test_getNews(unittest.TestCase):
    url_t1=r'http://www.xwlb.top/xwlb.html'
    url_t2=r'http://www.xwlb.top/28337.html'
    url_t3=r'http://www.xwlb.top/xwlb_2.html'

    def teardown(self):
        #每个测试用例执行之后做操作
        print('Test ended!')

    def setUp(self):
        #么个测试用例执行之前做操作
        print('Test starting...')

    @classmethod
    def tearDownClass(self):
        #必须使用 @classmethod 装饰器，所有的test运行完之后运行一次
        print('case ended！！')

    @classmethod
    def setUpClass(self):
        #必须使用 @classmethod 装饰器，所有的test运行之前运行一次
        print('start to test getnews!')

    def test_a_run(self):
        self.assertTrue(getRespose(url_t1))  #测试用例

    def test_b_run(self):
        self.assertTrue(gettext(url_t2))  #测试用例

    def test_c_run(self):
        self.assertTrue(gettext(url_t2))  #测试用例

    def test_c_run(self):
        self.assertTrue(TextWriter(url_t2))  #测试用例