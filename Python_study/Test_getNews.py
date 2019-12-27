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
import xmlrunner
import os
from CCTVnews_text_V1 import *


class Test_getNews(unittest.TestCase):

    url_t1 = r'http://www.xwlb.top/xwlb.html'
    url_t2 = r'http://www.xwlb.top/xwlb.html'
    url_t3 = r'http://www.xwlb.top/xwlb.html'
    #通过类属性设置unittest的简单参数化
    def teardown(self):
        #每个测试用例执行之后做操作
        print('unittest is ended!')

    def setUp(self):
        #么个测试用例执行之前做操作,可以在这里用JSON设置参数化
        print('Test starting...')

    @classmethod
    def tearDownClass(self):
        #必须使用 @classmethod 装饰器，所有的test运行完之后运行一次
        if os.path.isfile(r'./temp/text.tmp'):
            os.remove(r'./temp/text.tmp')
            print('临时文件清理!')
        print('case ended！！')

    @classmethod
    def setUpClass(self):
        #必须使用 @classmethod 装饰器，所有的test运行之前运行一次
        print('start to test getnews!')

    def test_a_run(self):
        self.assertTrue(getRespose(self.url_t1))
        #测试用例

    def test_b_run(self):
        self.assertTrue(getNowUrls(self.url_t1, 1))

    def test_c_run(self):
        self.assertTrue(getNowUrls(self.url_t1, 2))

    def test_c_run(self):
        self.assertTrue(textWrite('1', '2', file_path=r'.\temp', file_name=r'text.tmp'))

    def test_d_run(self):
        self.assertTrue(pageParsing(self.url_t2))

    def test_e_run(self):
        self.assertTrue(getRespose(self.url_t3))

if __name__=='__main__':
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(Test_getNews))
    #使用makeSuite方法添加所有的测试方法
    #test_suite.addTest(Test_getNews('test_e_run'))
    # 测试套件中添加测试用例
    runner = xmlrunner.XMLTestRunner(output='report-xml')
    #指定报告放的目录
    runner.run(test_suite)