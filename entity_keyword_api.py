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
from flask import request, jsonify
data_ai = pd.read_csv('./models/test/aidaily_articles.csv').iloc[:10,:]
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
 
    new_data = main.extract_entity(data_ai, articleType)

    for i in range(len(new_data)):
        #dic = new_data.iloc[i,:].to_dict(orient = 'dict')  将dataframe转换成dic
        dic = new_data.iloc[i,:].to_dict()  # 将series转成dic 输出
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
    new_data = main.extract_keywords(data_ai,articleType, cut_method='tfidf', top_k=5, normalize_title_content=True)

    for i in range(len(new_data)):
        #dic = new_data.iloc[i,:].to_dict(orient = 'dict')  将dataframe转换成dic
        dic = new_data.iloc[i,:].to_dict()  # 将series转成dic 输出
        list_output.append(dic)

    # Loop through the data and match results that fit the requested query and query type.
    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(list_output)

if __name__== '__main__':
    app.run(
        port = 8000,  
        debug = True)

