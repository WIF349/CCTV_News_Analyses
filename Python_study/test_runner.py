#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

