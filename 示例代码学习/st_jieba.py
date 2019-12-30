# -*- coding:utf-8 -*-
'''
学习如何使用jieba库进行中文分词
'''

import jieba
from os import path
import jieba.analyse as analyse

# seg_list = jieba.cut("我来到北京清华大学", cut_all=True, HMM=False)
# print("Full Mode: " + "/ ".join(seg_list))  # 全模式
#
# seg_list = jieba.cut("我来到北京清华大学", cut_all=False, HMM=True)
# print("Default Mode: " + "/ ".join(seg_list))  # 默认模式
#
# seg_list = jieba.cut("他来到了网易杭研大厦", HMM=False)
# print(", ".join(seg_list))
#
# seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造", HMM=False)  # 搜索引擎模式
# print(", ".join(seg_list))
#
# # jieba.cut的默认参数只有三个,jieba源码如下
# # cut(self, sentence, cut_all=False, HMM=True)
# # 分别为:输入文本 是否为全模式分词 与是否开启HMM进行中文分词


d = path.dirname(__file__)
print('路径', d)
text_path = './新闻联播.txt' #设置要分析的文本路径

# text = open(path.join(d, text_path)).read()
text = open(text_path, encoding='utf-8').read()  #指定编码格式，修正报错
for key in analyse.extract_tags(text, 50, withWeight=False):
# 使用jieba.analyse.extract_tags()参数提取关键字,默认参数为50
    #print(key.encode('utf-8', errors='ignore'))
    print(key)
    # 设置输出编码为utf-8不然在因为win下控制台默认中文字符集为gbk,所以会出现乱码
    # 当withWeight=True时,将会返回number类型的一个权重值(TF-IDF)


import jieba
TestStr = "2010年底部队友谊篮球赛结束"
# 因为在汉语中没有空格进行词语的分隔，所以经常会出现中文歧义，比如年底-底部-部队-队友
# jieba 默认启用了HMM（隐马尔科夫模型）进行中文分词，实际效果不错

seg_list = jieba.cut(TestStr, cut_all=True)
print("Full Mode:", "/ ".join(seg_list)) # 全模式

seg_list = jieba.cut(TestStr, cut_all=False)
print("Default Mode:", "/ ".join(seg_list) )# 默认模式
# 在默认模式下有对中文歧义有较好的分类方式

seg_list = jieba.cut_for_search(TestStr) # 搜索引擎模式
print("cut for Search", "/".join(seg_list))



import sys
import jieba
from os import path
import jieba.posseg as pseg

d = path.dirname(__file__)
stopwords_path = './stopwords.txt' # 停用词词表

text_path = './新闻联播.txt' #设置要分析的文本路径
#text = open(path.join(d, text_path)).read()
text = open(text_path, encoding='utf-8', errors='ignore').read()
jieba.add_word('央视网消息')
jieba.add_word('新闻联播文字版')
jieba.add_word('国内联播快讯')
def jiebaclearText(text):
    mywordlist = []
    seg_list = jieba.cut(text, cut_all=False)
    liststr="/ ".join(seg_list)
    f_stop = open(stopwords_path, encoding='utf-8', errors='ignore').read()
    # try:
    #     f_stop_text = f_stop.read()
    #     #f_stop_text=unicode(f_stop_text, 'utf-8')
    # finally:

    f_stop_seg_list = f_stop.split('\n')
    for myword in liststr.split('/'):
        if not (myword.strip() in f_stop_seg_list) and len(myword.strip()) > 1:
            mywordlist.append(myword)


    return ''.join(mywordlist)

text1 = jiebaclearText(text)
print(text1)

words=pseg.cut(text)
for word ,flag in words:
    print('%s %s ' % (word,flag))
