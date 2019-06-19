#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 19:08:04 2019

@author: rain
"""
# 导入包
# -*- coding: utf-8 -*
from pyltp import SentenceSplitter
import jieba.posseg as pseg
from nltk.tag.stanford import StanfordNERTagger
import sys
import os
from models.tfidf import cal_tfidf    
import pandas as pd
import re
import numpy as np
import jieba
import jieba.analyse
os.chdir('/Users/rain/todo-api/flask/duty')  #这里我改变了路径进入到指定的最大的文件夹中（若使用需要手动调整到自己的路径！！！）
# 查看当前路径位置
os.getcwd() 
#引入两个脚本
import models.TF_PO 
from models.extract_keywords import *
import models.BosonNLP_PO


def extract_entity(data, articleType = 'AIDaily', method = 'zh_NER_TF', contentMode=[1, 1, 0],
           useExpanded=[1, 0, 1], accurateMode=False, dirName='outputs'): 
    '''
    输入一个dataframe（csv文件），输出一个新的dataframe（其中包含所有每一条新闻的entity
    input:  articleType: string, 'AIDaily' or other, case insensitive; 目前使用的是aidaily 的数据csv
            method: 输入一个我们想用的找到entity的method，两种： method = 'zh_NER_TF' or BosonNLP_PO
            contentMode: list of int, 1 for use, 0 for ignore. 3 digits stand for: [title, content, description] 
            useExpanded: whether or not to use expanded words, 1 for use, 0 for not, 3 digits stand for: [organization, people, undefined]
            accurateMode: whether or not to use StanfordNERTagger, which is more accurate but computationaly more expensive.
            dirName: string, deafult to 'test.txt' （目前还没用到，如果之后要直接导出file的话可能会用到，所以该参数还未删掉）
    output: dataframe(目前只出现机构，人物，关系对，这三个)

    '''
    time = []
    title = []
    orgnization = []
    person = []
    relation = []
    if method ==  'zh_NER_TF':        
        for i in range(len(data)):
            result = TF_PO.NER_PO(articleType, data.iloc[i, :])
            time.append(data.iloc[i, 2])
            title.append(result[0])
            orgnization.append(result[1][0])
            person.append(result[1][1])
            relation.append(result[1][2])
            print (i)
    if method ==  'BosonNLP_PO':        
        for i in range(len(data)):
            result = BosonNLP_PO.NER_PO(articleType, data.iloc[i, :])
            time.append(data.iloc[i, 2])
            title.append(result[0])
            orgnization.append(result[1][0])
            person.append(result[1][1])
            relation.append(result[1][2])
            print (i)
    dic = {'时间': time,'标题': title, '机构': orgnization,'人物':person, '机构人物关系对': relation}
    new_data = pd.DataFrame(dic)
    return (new_data)


def extract_keywords(data, articleType, title_weight=0.8, cut_method='tfidf', top_k=5, normalize_title_content=True):
    """
    articleType - string, 'AIDaily' or other, case insensitive; 目前使用的是aidaily 的数据csv
    title_weight - 标题所占比重
    input: data 
    cut_method - 使用的评定方法
    top_k -选择多少个关键词
    return dataframe
    """
    title_weight = 0.8
    # 获取标题关键字与相应权重
    title_weight_list = get_keywords(data['title'],
                                          cut_method='tfidf',
                                          normalize_title_content=True)
    # 获取内容关键字与相应权重
    content_weight_list = get_keywords(data['content'],
                                            cut_method,
                                            normalize_title_content)
    # 合并标题关键字与内容关键字的权重
    df = pd.DataFrame()
    df['title'] = data['title']
    if articleType != 'AIDaily':
        df['description'] = data['description']
    df['keywords'] = cal_keywords_weight(title_weight_list,
                                                      content_weight_list,
                                                      top_k=5,
                                                      title_weight=title_weight)
    
    return (df)

#小小测试
new_= extract_entity(data, method = 'zh_NER_TF')