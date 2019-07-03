#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:51:49 2019

@author: rain
记得结束后关闭进程： ps -fA | grep python  kill。。
"""
#!flask/bin/python
import sys
import flask
import os
import main
import pandas as pd
#from pyltp import SentenceSplitter
import jieba.posseg as pseg
from nltk.tag.stanford import StanfordNERTagger   
import re
import numpy as np
import jieba
import jieba.analyse
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd

from flask import request, jsonify

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

data = pd.read_csv('./models/test/aidaily_articles.csv').iloc[:3 ,:].reset_index()
#data = pd.read_csv('./models/test/articles_1000.csv').iloc[:10,:]  
# 补充分词词库
dic_title = main.add_dict(data['title'])    # 找到在（） 或者「」 或者《》内的词语
dic_content = main.add_dict(data['content']) # # 找到在（） 或者「」 或者《》内的词语
# 加载自定义词库
jieba.load_userdict('./dictionary/dict.txt')   
data_keywords =  main.extract_keywords(data, 'AIDaily')
data_entity = main.extract_entity(data, 'AIDaily')
L = []
for i in range(len(data_entity)):
    L.append(data_entity['机构'][i]+data_entity['人物'][i])      
new_keywords = list(map(check_similar, L, list(data_keywords['keywords'])))
data_keywords['keywords'] = new_keywords


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>主题主题提取与关键词提取</h1><p>This site is a prototype API for extract entity and keywords.</p>"

@app.route('/api/resources/entity', methods=['GET'])
def api_query_entity():
    # Check if an query was provided as part of the URL.
    # If query is provided, assign it to a variable.
    # If no query is provided, display an error in the browser.
    list_output = []
    if 'query' in request.args:
        query= (request.args['query'])
        articleType = query
    else:
        articleType = 'AIDaily'

    for i in range(len(data_entity)):
        #dic = new_data.iloc[i,:].to_dict(orient = 'dict')  将dataframe转换成dic
        dic = data_entity.iloc[i,:].to_dict()  # 将series转成dic 输出
        list_output.append(dic)
        print (list_output)
    return jsonify(list_output)

@app.route('/api/resources/keywords', methods=['GET'])
def api_query_keyword():
    # Check if an query was provided as part of the URL.
    # If query is provided, assign it to a variable.
    # If no query is provided, display an error in the browser.
    list_output = []
    if 'query' in request.args:
        query= (request.args['query'])
        articleType = query
    else:
        articleType = 'AIDaily'
        
    for i in range(len(data_keywords)):
        #dic = new_data.iloc[i,:].to_dict(orient = 'dict')  将dataframe转换成dic
        dic = data_keywords.iloc[i,:].to_dict()  # 将series转成dic 输出
        list_output.append(dic)

    # Loop through the data and match results that fit the requested query and query type.
    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(list_output)

if __name__== '__main__':
    app.run(
        host = '0.0.0.0',
        port = 80,  
        debug = False)

