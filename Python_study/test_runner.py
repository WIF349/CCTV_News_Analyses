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
from Test_getNews import *

if __name__=='__main__':
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(Test_getNews))
    #使用makeSuite方法添加所有的测试方法
    #test_suite.addTest(Test_getNews('test_e_run'))
    # 测试套件中添加测试用例
    runner = xmlrunner.XMLTestRunner(output='report-xml')
    #指定报告放的目录
    runner.run(test_suite)

