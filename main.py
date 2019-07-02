#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 19:08:04 2019

@author: rain
"""
# 导入包
# -*- coding: utf-8 -*
#from pyltp import SentenceSplitter
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
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd

# 查看当前路径位置
os.getcwd() 
#引入三个脚本
import script.TF_PO as TF_PO
from script.extract_keywords import *
import script.BosonNLP_PO as BosonNLP_PO

# 参数设置
param_grid = {'articleType':'AIDaily',
              'method' : 'zh_NER_TF',
              'contentMode' : [1, 1, 0],
              'useExpanded' : [1, 0, 1],
              'similarity' : 50,
              'title_weight': 0.8,
              'cut_method': 'tfidf', 
              'top_k': 5, 
              'normalize_title_content': True
              
        }




def add_dict(text_list):
    """
    找到在（） 或者「」 或者《》内的词语并加入jieba dictionary 中，为分词做准备
    return - dic 是一个list，包含了在（） 或者「」 或者《》内的词语
    """  
    # 导入jieba cut词
    dict_path = './dictionary/dict.txt'
    dict_set = ()
    if dict_path is not None:
        dict_set = [x.strip() for x in open(dict_path).readlines()]  # dict_set 是分词词典
    diction = []    
    for text in (text_list):
        text = str(text)
        p1 = re.compile(r'[(](.*?)[)]', re.S)  #最小匹配
        p2 = re.compile(r'「(.*?)」', re.S)  #最小匹配
        p3 = re.compile(r'《(.*?)》', re.S)  #最小匹配
        add = re.findall(p1, text)
        add = add + (re.findall(p2, text))
        add = add + (re.findall(p3, text))
        add = [ele for ele in add if (len(ele) < 20 and ele+' 1' not in dict_set)]
        file = open("./dictionary/dict.txt","a") 
        for string in add:
            diction.append(string)
            file.write(string+' 1'+'\n')
    file.close()     
    return (diction)
    


def extract_entity(data, articleType = 'AIDaily', method = 'zh_NER_TF', contentMode=[1, 1, 0],
           useExpanded=[1, 0, 1], accurateMode=False, similarity = 50, dirName='outputs'): 
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
            result = TF_PO.NER_PO(articleType, data.iloc[i, :], contentMode=[1, 1, 0],
           useExpanded=[1, 0, 1], accurateMode=False, similarity = 50)
            time.append(data.date[i])
            title.append(data.title[i])
            orgnization.append(result[1][0])
            person.append(result[1][1])
            relation.append(result[1][2])
            print (i)
    if method ==  'BosonNLP_PO':        
        for i in range(len(data)):
            result = BosonNLP_PO.NER_PO(articleType, data.iloc[i, :], contentMode=[1, 1, 0],
           useExpanded=[1, 0, 1], accurateMode=False, similarity = 50)
            time.append(data.date[i])
            title.append(data.title[i])
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

def check_similar(list1, list2):
    '''
    对比两组list的相似度, 将相似度较高和在dict_title中的词提取出来
    '''
    list3 = []
    if len(list1) >0:
        for ele in list1:
            extract = process.extract(ele, list2, limit = 1)
            if extract[0][1] > 80:
                if len(ele) > 2:
                    list3.append(ele)
                else:
                   list3.append(extract[0][0]) 
    else:
        list3 = []  
    list3 = list(set(list3).union(set(list2).intersection(dic_title)))    
    return (list3)

#小小测试
#new_= extract_entity(data, method = 'zh_NER_TF')
#测试 运用 dailynew 测试,未删除依然保留（仅测试作用）
if __name__ == '__main__':
    data = pd.read_csv('./models/test/aidaily_articles.csv').iloc[:10 ,:].reset_index()
    #data = pd.read_csv('./models/test/articles_1000.csv').iloc[:10,:]  
    # 补充分词词库
    dic_title = add_dict(data['title'])    # 找到在（） 或者「」 或者《》内的词语
    dic_content = add_dict(data['content']) # # 找到在（） 或者「」 或者《》内的词语
    # 加载自定义词库
    jieba.load_userdict('./dictionary/dict.txt')   
    data_keywords =  extract_keywords(data, param_grid['articleType'], param_grid['title_weight'],
                                      param_grid['cut_method'], param_grid['top_k'], param_grid['normalize_title_content'])
    
    data_entity = extract_entity(data, param_grid['articleType'], param_grid['method'], param_grid['contentMode'],
                                 param_grid['useExpanded'], param_grid['similarity'])
    
    #data_entity.to_csv('./models/test/out_entity.csv')
    #data_keywords.to_csv('./models/test/out_keywords.csv')
    L = []
    for i in range(len(data_entity)):
        L.append(data_entity['机构'][i]+data_entity['人物'][i])      
    new_keywords = list(map(check_similar, L, list(data_keywords['keywords'])))
    
    #data_keywords['keywords'] = new_keywords
    #data_keywords.to_csv('./models/test/out_new_keyword.csv')   #经过交叉分析后的keywords
