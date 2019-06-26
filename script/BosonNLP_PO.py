# -*- coding: utf-8 -*
from __future__ import print_function, unicode_literals
#from pyltp import SentenceSplitter
from nltk.tag.stanford import StanfordNERTagger
from bosonnlp import BosonNLP
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
#os.chdir('/Users/rain/todo-api/flask/duty')  #这里我改变了路径进入到指定的最大的文件夹中（若使用需要手动调整到自己的路径！！！）
# 查看当前路径位置
os.getcwd()  # 路径需要在最外层文件夹！！
from models.namedEntityTools import *
from models.loadTools import *
from models.zh_ner_tf.main import *

from platform import python_version
print(python_version())


# from loadTools import *
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
    specialN = ['nr', 'ns', 'nt', 'nz', 'nl', 'ng', 'nrt', 'nrfg', 'vn']
    engSpecialN = ['nx','w','wd']
    tagInterpret = ['ORG', 'PEO', 'O']
    lastNameDict = txtToDict("./dictionary/last name.txt")
    StanfordTagger = StanfordNERTagger('./dictionary/stanford-ner-2014-08-27/classifiers/english.all.3class.distsim.crf.ser.gz','./dictionary/stanford-ner-2014-08-27/stanford-ner.jar')
    title = data['title'] # 需要注意导入的数据情况哦！
    content = data['content']
    if articleType == 'AIDaily':
        description = ''
    else: 
        description = data['description']
    #nlp = BosonNLP('jj-zE93I.33208.2PLQn2ZwoOOs')
    #nlp = BosonNLP('Q-VXkanb.33198.7UaoJU9ozS-n')
    nlp = BosonNLP('Cpcr3Wym.33210.xQpBxPaHIXmi')

    def helper(title, content, description, contentMode, useExpanded, accurateMode, similarity):
        sentences = splitSentence(title, content, description, contentMode)
        #sentences = list(SentenceSplitter.split(title+content+description))
        peopleList = []
        orgList = []
        relationDict = defaultdict(list)
        financialDict = defaultdict(list)
        titleDict = defaultdict(list)
        results = nlp.ner(sentences)

        for result in results:
            sen = ''.join(result['word'])
            entities = result['entity']
            bosonWords = []
            for i in range(len(result['word'])):
                bosonWords.append([result['word'][i], result['tag'][i]])

            currRoundList = getRound(sen)
            currRoundString = ', 轮次: ' + ''.join(currRoundList) if ''.join(currRoundList).strip() else ''

            words = []
            start = 0
            for entity in entities:
                words += bosonWords[start:entity[0]]
                if entity[2] in ['org_name','company_name']:
                    words.append([''.join(result['word'][entity[0]:entity[1]]), 'ORG'])
                    if ''.join(result['word'][entity[0]:entity[1]]) not in orgList:
                        orgList.append(''.join(result['word'][entity[0]:entity[1]]))
                elif entity[2] == 'person_name':
                    words.append([''.join(result['word'][entity[0]:entity[1]]), 'PEO'])
                    if ''.join(result['word'][entity[0]:entity[1]]) not in peopleList:
                        peopleList.append(''.join(result['word'][entity[0]:entity[1]]))
                elif entity[2] == 'time':
                    words.append([''.join(result['word'][entity[0]:entity[1]]), 'time'])
                elif entity[2] == 'job_title':
                    words.append([''.join(result['word'][entity[0]:entity[1]]), 'TTL'])
                start = entity[1]
            words += bosonWords[start:]          
            
            # merging and tagging eng words
            i = 0
            while i < len(words):
                word, tag = words[i]
                if tag == 'nx' and (word not in peopleList+orgList):
                    start, end, expandedWord = expandNoun(i, words, engSpecialN)
                    words[i][0] = expandedWord
                    if expandedWord in ''.join(currRoundString):
                        i += 1
                        continue
                    words[i][1] = tagInterpret[engTagging(expandedWord, accurateMode, StanfordTagger)]
                    if words[i][1] == 'PEO':
                        if words[i][0] not in peopleList:
                            if not re.findall('[/, =,《,》]', words[i][0]):
                                peopleList.append(words[i][0])
                                titleDict[expandedWord.strip()] = []
                    if words[i][1] == 'ORG':
                        if words[i][0] not in orgList:
                            if not re.findall('[/, =,《]', words[i][0]):
                                orgList.append(words[i][0])
                    i = end
                elif word in investKeyWords+cooporationKeyWords:
                    words[i][1] = 'FNC'
                    i += 1
                else:
                    i += 1
            
            #对peopleList 与 orgList 中的element 进行整理，删除掉相关性比较高的其中几个
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

            currPEOList = [[(i, i+1), words[i][0]] for i in range(len(words)) if words[i][1] == 'PEO']
            currTTLList = [[(i, i+1), words[i][0]] for i in range(len(words)) if words[i][1] == 'TTL']
            currORGList = [[(i, i+1), words[i][0]] for i in range(len(words)) if words[i][1] == 'ORG']

            if (not currPEOList) and (not currORGList):
                continue


            currMoneyList = list(set([num for num in findNumber(words) if containKeyWords(num, ['亿', '元', '万'])]))
            currMoneyString = ', 金额: ' + ''.join(currMoneyList) if ''.join(currMoneyList).strip() else ''
            currTimeList = list(set([num[0] for num in words if num[1] == 'time']))
            currTimeString = ', 时间: ' + ''.join(currTimeList) if ''.join(currTimeList).strip() else ''



            # 匹配职位信息
            for _, p in currPEOList:
                titleDict[p.strip()] = []
            titleDict = pairTitle(currPEOList, currTTLList, currORGList, words, titleDict, currTimeString)


            # 找金融动作
            #findFinancialRelation(verbs, sen, currORGList
            financialWords = [k for k in words if k[1] in ['ORG','FNC','w','wj','ww','wt','wd','wf','wn','wm','ws','wp']]
            findFinancialRelation(financialWords, financialDict, currRoundString, currMoneyString, currTimeString)

            # 找动词
            i = 0
            prevNER = ''
            prevTag = ''
            prevVerb = ''
            while i < len(words):
                word, tag = words[i]
                if tag in ['PEO','ORG']:
                    if prevNER and prevVerb:
                        if ((prevNER.strip()+' ('+prevVerb.strip()+') '+word.strip()) not in relationDict) and tag != prevTag:
                            relationDict[prevNER.strip()+' ('+prevVerb.strip()+') '+word.strip()].append(currTimeString)
                    prevNER = word
                    prevTag = tag
                    prevVerb = ''
                if tag in ('v', 'vd', 'vshi', 'vyou', 'vl', 'vi'):
                    prevVerb += word
                i += 1
        relationDict = dict(relationDict)   #改变datatype 方便之后打印出来
        writeList1 = [orgList, peopleList, relationDict]
        writeList2 = ['机构', '人物', '人物机构关系对']

        if financialDict:
            writeList1.append(financialDict)
            writeList2.append('投融资、合作信息')

        #saveToTxt(title, writeList1, writeList2, fileName=fileName)
        ##
        # return senDict, nameDict, peopleList, orgList, undfList
        # return [orgList, titleDict, relationDict]
        ##
        return [title, writeList1, writeList2]
        ##
    l = helper(title, content, description, contentMode, useExpanded, accurateMode, similarity)  # l 为最后输出的关系
    return (l)





