#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
__author__ = '王益夫'
__mtime__ = '2019/12/20'
'''
'''
版本修改：
V 1.0:get代码获取的文本内容，通过jieba库和词云进行分析
'''
import jieba
from wordcloud import WordCloud
from os import path
import re
import matplotlib.pyplot as plt
#from scipy.misc import imread
import imageio


def jiebaclearText(text):
    mywordslist = []
    seg_list = jieba.cut(text, cut_all=False)
    #seg_list = jieba.cut(TestStr, cut_all=True)    全模式：该模式将语料中所有可以组合成词的词语都构建出来，其优点是速度非常快，缺点是不能解决歧义问题，并且分词结果不太准确。
    #seg_list = jieba.cut(TestStr, cut_all=False)   默认模式:该模式利用其算法将句子最精确地分隔开，适合文本分析，通常采用这种模式进行中文分词。
    #seg_list = jieba.cut_for_search(TestStr)       搜索引擎模式:该模式是在精确模式基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词。
    liststr = "/".join(seg_list)
    f_stop = open(StopWordsPath, encoding='utf-8', errors='ignore')
    try:
        f_stop_text = f_stop.read()
    finally:
        f_stop.close()

    f_stop_seg_list = f_stop_text.split('\n')
    for myword in liststr.split('/'):
        if not (myword.strip() in f_stop_seg_list) and len(myword.strip()) > 1:
            mywordslist.append(myword)
    return ' '.join(mywordslist)

def addWordsRulls(text):
    addwords_list = set()
    try:
        results = re.findall('《[^》]+》', text)
        for result in results:
            addwords_list.add(result)
            #jieba.add_word(result)
        return True
    except Exception as e:
        raise e
        addwords_list.add('EOR:ADD正则解析失败，未获取关键词！')
        return False
    finally:
        with open(AddWordsPath, 'a+', encoding='utf-8', errors='ignore') as file_add:
            for line in list(addwords_list):
                file_add.write(line + '\n')

def StopWordsRulls(text):
    Stopwords_list = set()
    try:
        results = re.findall('\d{4}年\d{1,2}月\d{1,2}日', text)
        for result in results:
            print(result)
            Stopwords_list.add(result)
            #jieba.add_word(result)
        return True
    except Exception as e:
        raise e
        Stopwords_list.add('EOR:Stop正则解析失败，未获取关键词！')
        return False
    finally:
        with open(StopWordsPath, 'a+', encoding='utf-8', errors='ignore') as file_Stop:
            for line in list(Stopwords_list):
                file_Stop.write(line + '\n')

def main():
    file_path = path.dirname(__file__) + r'/temp'
    file_name1 = r'新闻联播.txt'
    file_name2 = r'StopWords.txt'
    file_name3 = r'AddWords.txt'

    TextPath = file_path + '/' + file_name1
    StopWordsPath = file_path + '/' + file_name2
    AddWordsPath = file_path + '/' + file_name3

    with open(TextPath, encoding='utf-8', errors='ignore') as file_Text:
        text = file_Text.read()
    # for key in analyse.extract_tags(text, 50, withWeight=False):
    #     print(key)

    if addWordsRulls(text) and StopWordsRulls(text):
        with open(AddWordsPath, 'r', encoding='utf-8', errors='ignore') as file_read:
            context = set(file_read.read())
            for line in context:
                jieba.add_word(line)

    text_text = jiebaclearText(text)

    color_mask = imageio.imread(file_path + "/1.png")
    cloud = WordCloud(
        # 设置字体，不指定就会出现乱码
        font_path="./temp/HYQiHei-25J.ttf",
        # font_path=path.join(d,'simsun.ttc'),
        # 设置背景色
        background_color='white',
        # 词云形状
        mask=color_mask,
        # 允许最大词汇
        max_words=200,
        # 最大号字体
        max_font_size=40
    )
#    wordcloud = WordCloud(background_color="white", width=1000, height=860, margin=2).generate(text_text)
    word_cloud = cloud.generate(text_text)  # 产生词云
    word_cloud.to_file("test.jpg")  # 保存图片
    #  显示词云图片
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    main()



