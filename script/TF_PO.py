# -*- coding: utf-8 -*
#!user/bin/env python3
#from pyltp import SentenceSplitter
import jieba.posseg as pseg
import jieba
import tensorflow as tf
from nltk.tag.stanford import StanfordNERTagger
import sys
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
#os.chdir('/Users/rain/todo-api/flask/duty')  #这里我改变了路径进入到指定的最大的文件夹中（若使用需要手动调整到自己的路径！！！）
# 查看当前路径位置
os.getcwd()  # 路径需要在最外层文件夹！！
from models.namedEntityTools import *
from models.loadTools import *
from models.zh_ner_tf.main import *

#查看当前版本
from platform import python_version
print(python_version())


# 查看当前路径位置
os.getcwd()
stop_words_path = './dictionary/black.txt'
stopwords_set = ()
if stop_words_path is not None:
    jieba.analyse.set_stop_words(stop_words_path)  # 加载黑名单
    stopwords_set = [x.strip() for x in open(stop_words_path).readlines()]

# 导入技术词库
tech_path = './dictionary/tech.txt'
tech_set = ()
if tech_path is not None:
    tech_set = [x.strip() for x in open(tech_path).readlines()]


def NER_PO(articleType, data, contentMode=[1, 1, 0],
           useExpanded=[1, 0, 1], accurateMode=False, similarity = 50, dirName='outputs'):
    '''
    input:  articleType: string, 'AIDaily' or other, case insensitive; 目前使用的是aidaily 的数据csv
            contentMode: list of int, 1 for use, 0 for ignore. 3 digits stand for: [title, content, description] 
            useExpanded: whether or not to use expanded words, 1 for use, 0 for not, 3 digits stand for: [organization, people, undefined]
            accurateMode: whether or not to use StanfordNERTagger, which is more accurate but computationaly more expensive.
            similarity: 允许同一个entity组内最多可以出现多少相似度的词
            dirName: string, deafult to 'test.txt'
    output: list

    '''
    investKeyWords = ['融资', '领投', '跟投', '收购', '合并', '投资', '创投', '获投', '注资', '并购', '参投', '出资', '斥资', '筹资', '筹集', '入股', '增持']
    cooporationKeyWords = ['合作', '结盟', '联合', '对接', '携手', '提供商', '供应商', '联盟', '联手', '牵手', '共建']
    specialN = ['nr', 'ns', 'nt', 'nz', 'nl', 'ng', 'nrt', 'nrfg', 'vn', 'CONF']
    engSpecialN = ['eng','CONF','x','m','w']
    tagInterpret = ['ORG', 'PEO', 'O']
    lastNameDict = txtToDict("./dictionary/last name.txt")
    StanfordTagger = StanfordNERTagger('./dictionary/stanford-ner-2014-08-27/classifiers/english.all.3class.distsim.crf.ser.gz','./dictionary/stanford-ner-2014-08-27/stanford-ner.jar')
    titleList = createDict('./dictionary/titles.txt')
    loadDicts(investKeyWords + cooporationKeyWords)
    title = data['title'] # 需要注意导入的数据情况哦！
    content = data['content']
    if articleType == 'AIDaily':
        description = ''
    else: 
        description = data['description']
        
    def helper(title, content, description, contentMode, useExpanded, accurateMode, similarity):
        sentences = splitSentence(title, content, description, contentMode)
        #sentences = SentenceSplitter.split(title+content+description)
        peopleList = []
        orgList = []
        relationList = []
        financialDict = defaultdict(list)
        titleDict = defaultdict(list)
        try:
            tf.reset_default_graph() #引入reset_default_graph() 使得 zh_ner_master 重置 导出一个错误的部分，不要对这个部分进行改动 
            people_0, loc_0, org_0 = zh_NER_TF_master(title+content+description)
            for ele in people_0:
                if not re.findall('[/, 。,(,),《, 》, ）, （]', ele):
                    if ele not in peopleList + stopwords_set:
                        peopleList.append(ele)
            for ele in org_0:
                if not re.findall('[/, 。,(,),《, 》, ）, （]', ele):
                    if ele not in orgList + stopwords_set:
                        orgList.append(ele)
            
        except:
            title = 'not accept' + title
        #比较peoplelist 与 orglist的词（将相关性过强的词删除）
        if len(peopleList) > 1:
            for ele in peopleList:
                extract = process.extract(ele, peopleList, limit=2)
                if extract[1][1] > similarity:
                    if len(ele) <= len(extract[1][0]):
                        peopleList.remove(extract[1][0])
                    else:
                        peopleList.remove(ele)
        if len(orgList) > 1:
            for ele in orgList:
                extract = process.extract(ele, orgList, limit=2)
                if extract[1][1] > similarity:
                    if len(ele) <= len(extract[1][0]):
                        orgList.remove(extract[1][0])
                    else:
                        orgList.remove(ele)
                        
        for sen in sentences:
            currPeople = containKeyWords(sen, peopleList)
            currOrg = containKeyWords(sen, orgList)
            currTitle = containKeyWords(sen, titleList)
            keyWords = []
            verbList = containKeyWords(sen, investKeyWords + cooporationKeyWords)
            currRoundList = getRound(sen)
            currRoundString = ', 轮次: ' + ''.join(currRoundList) if ''.join(currRoundList).strip() else ''

            if (not currPeople and currOrg) and (not verbList):
                continue
            PEOList = []
            TTLList = []
            ORGList = []
            for word in currPeople:
                it = re.finditer(word, sen.lower())
                for target in it:
                    if not isPeople(word, lastNameDict):
                        continue
                    keyWords.append([(target.start(), target.end()), 'PEO', word])
                    PEOList.append([(target.start(), target.end()), word])
            for word in currOrg:
                it = re.finditer(word, sen.lower())
                for target in it:
                    keyWords.append([(target.start(), target.end()), 'ORG', word])
                    ORGList.append([(target.start(), target.end()), word])
            for word in currTitle:
                it = re.finditer(word, sen.lower())
                for target in it:
                    keyWords.append([(target.start(), target.end()), 'TTL', word])
                    TTLList.append([(target.start(), target.end()), word])

            # jieba标注其他词
            sortedKeyWords = sorted(keyWords, key = lambda k:k[0][0])
            prev = 0
            words = []
            for interval, tag, word in sortedKeyWords:
                words += generatorToList(pseg.cut(sen[prev:interval[0]]))
                words += [[word, tag]]
                prev = interval[1]
            words += generatorToList(pseg.cut(sen[prev:]))

            #print ('sen', sen)
            #print ('words',words)

            # merging and tagging eng words
            i = 0
            while i < len(words):
                word, tag = words[i]
                if tag == 'eng':
                    start, end, expandedWord = expandNoun(i, words, engSpecialN)
                    words[i][0] = expandedWord
                    words[i][1] = tagInterpret[engTagging(expandedWord, accurateMode, StanfordTagger)]
                    if words[i][1] == 'PEO':
                        if words[i][0] not in peopleList + stopwords_set:
                            if not re.findall('[/, 。,(,),《, 》,）,（]', words[i][0]):
                                peopleList.append(words[i][0])
                                titleDict[words[i][0].strip()] = []
                    if words[i][1] == 'ORG':
                        if words[i][0] not in orgList + stopwords_set:
                            if not re.findall('[/, 。,(,),《,》,）,（]', words[i][0]):
                                orgList.append(words[i][0])

                    i = end
                else:
                    i += 1
                
            currMoneyList = [num for num in findNumber(words) if containKeyWords(num, ['亿', '元', '万'])]
            currMoneyString = ', 金额: ' + ''.join(currMoneyList) if ''.join(currMoneyList).strip() else ''
            currTimeList = [num for num in findNumber(words) if containKeyWords(num, ['月', '日', '年'])]
            currTimeString = ', 时间: ' + ''.join(currTimeList) if ''.join(currTimeList).strip() else ''

            # 匹配职位信息
            for _, p in PEOList:
                titleDict[p.strip()] = []
            titleDict = trimTitle(pairTitle(PEOList, TTLList, ORGList, words, titleDict, currTimeString))


            # 找金融动作
            #findFinancialRelation(verbs, sen, ORGList
            financialWords = [k for k in words if k[1] in ['ORG','FNC','x']]
            findFinancialRelation(financialWords, financialDict,currRoundString,currMoneyString,currTimeString)


            # 找动词
            i = 0
            prevNER = ''
            prevTag = ''
            prevVerb = ''
            while i < len(words):
                word, tag = words[i]
                if tag in ['PEO','ORG']:
                    if prevNER and prevVerb:
                        if (prevNER.strip()+' ('+prevVerb.strip()+') '+word.strip()+currTimeString not in relationList) and tag != prevTag:
                            relationList.append(prevNER.strip()+' ('+prevVerb.strip()+') '+word.strip()+currTimeString)
                    prevNER = word
                    prevTag = tag
                    prevVerb = ''
                if tag in ('v', 'vn'):
                    prevVerb += word
                i += 1
                
                
        # 在peoplelist 与 orglist添加完毕后，需要进行删除
        #比较peoplelist 与 orglist的词（将相关性过强的词删除）
        if len(peopleList) > 1:
            for ele in peopleList:
                extract = process.extract(ele, peopleList, limit=2)
                if extract[1][1] > similarity:
                    if 2 < len(ele) <= len(extract[1][0]):
                        peopleList.remove(extract[1][0])
                    else:
                        peopleList.remove(ele)
        if len(orgList) > 1:
            for ele in orgList:
                extract = process.extract(ele, orgList, limit=2)
                if extract[1][1] > similarity:
                    if 2 < len(ele) <= len(extract[1][0]):
                        orgList.remove(extract[1][0])
                    else:
                        orgList.remove(ele)
        
        # 排除过长或者过短的词，如果遇到与或者和就拆开，如果遇到公司两个字就只要前几个
        for ele in peopleList:
            if (len(ele) > 10 or len(ele) < 2):
                peopleList.remove(ele)

    
        
        for ele in orgList:
            if (len(ele) > 30 or len(ele) < 3):
                orgList.remove(ele)
            elif re.findall('[与和]', ele):
                ele_new = re.split('[与和]', ele)
                for i in ele_new:              #保证拆分是有意义的
                    if len(i) <2:
                        ele_new.remove(i)
                orgList.remove(ele)
                orgList = orgList+ele_new
            elif ele.find('公司') > 0:      #如果找不到会返回-1 ！！
                orgList.remove(ele)
                orgList.append(ele[:ele.find('公司')+2])
        
        orgList = list(set(orgList).difference(set(tech_set)))  # 去掉技术词 取差集
        peopleList = list(set(peopleList).difference(set(tech_set)))  # 人物去掉tech里面的词
        peopleList = list(set(peopleList).difference(set(orgList)))  # 人物去掉org里面的词
        


        #writeList1 = [orgList, titleDict, relationList]
        writeList1 = [orgList, peopleList, relationList]
        writeList2 = ['机构', '人物', '人物机构关系对']
        if financialDict:
            writeList1.append(financialDict)
            writeList2.append('投融资、合作信息')

        #saveToTxt(title, writeList1, writeList2, fileName=fileName)
        ##
        #return senDict, nameDict, peopleList, orgList, undfList
        return [title, writeList1, writeList2]
        ##
    l = helper(title, content, description, contentMode, useExpanded, accurateMode, similarity)  # l 为最后输出的关系
    return (l)

#测试 运用 dailynew 测试,未删除依然保留（仅测试作用）
if __name__ == '__main__':
    import pandas as pd
    data = pd.read_csv('/Users/rain/Desktop/aidaily_articles.csv').iloc[:200,:]
    time = []
    title = []
    orgnization = []
    person = []
    relation = []
    for i in range(len(data)):
        result = NER_PO('AIDaily', data.iloc[i, :])
        time.append(data.date[i])
        title.append(result[0])
        orgnization.append(result[1][0])
        person.append(result[1][1])
        relation.append(result[1][2])
        print (i)
    dic = {'时间': time,'标题': title, '机构': orgnization,'人物':person, '机构人物关系对': relation}
    new_data = pd.DataFrame(dic)
    new_data.to_csv('new_data_entity_add.csv')