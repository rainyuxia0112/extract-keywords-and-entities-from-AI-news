#-*- encoding:utf-8 -*-
import os
#os.chdir('/Users/rain/todo-api/flask/duty') 

from models.tfidf import cal_tfidf    
import pandas as pd
import re
import numpy as np
import jieba
import jieba.analyse
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

# 查看当前路径位置
os.getcwd()
stop_words_path = './dictionary/stop_words.dat'
stopwords_set = ()
if stop_words_path is not None:
    jieba.analyse.set_stop_words(stop_words_path)  # 加载停用词文件
    stopwords_set = set([x.strip() for x in open(stop_words_path).readlines()])

# 导入黑名单
stop_words_path = './dictionary/black.txt'
stopwords_black = ()
if stop_words_path is not None:
    stopwords_black = [x.strip() for x in open(stop_words_path).readlines()]
 
    

def is_number(s):
    '''
    检查输入的文本是不是一个数字型
    '''
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False



def remove_text(text, type='number'):
    """
    从文本中移除特定文本，例如数字或标点

    :param text: 文本
    :param type: 移除的文本类型, 可选'number', 'punc', 'both'
    :return: 移除后的文本
    """
    from zhon.hanzi import punctuation
    import string
    #text = re.sub("<>".format(punctuation, string.punctuation), " ", text)
    text = re.sub('<.*?>', '', text)
    text = re.sub('[.*?]', '', text)
    text = re.sub('([\w\-_]+(?:(?:\.|\s*\[dot\]\s*[A-Z\-_]+)+))([A-Z\-\.,@?^=%&amp;:/~\+#]*[A-Z\-\@?^=%&amp;/~\+#]){2,6}?', '', text)

    return text


def get_keywords(text_list, cut_method='tfidf', normalize_title_content=True):
    """
    给定文本，返回该文本的关键字以及对应权重

    :param text_list: 文本列表
    :param cut_method: 采用的分词方法, 可选 'tf-idf', 'JTextRank'
    :param normalize_title_content: 是否对关键字权重进行归一化
    :return: 关键字及其对应权重
    """
    corpus = ['' for i in range(len(text_list))]
    for i, text in enumerate(text_list):
        text = str(text)
        text = remove_text(text, 'both')
        # print("TFIDF: 分析第 " + str(i + 1) + '/' + str(len(text_list)) + " 段文本")
        seg_list = jieba.cut(text, cut_all=False)
        for word in seg_list:
            if word not in stopwords_set and word.strip() != '':
                corpus[i] += word + ' '
    keyword_weight_list = cal_tfidf(corpus)



    if normalize_title_content == True:  # 归一化
        # print("进行标题/全文关键字权重归一化...")
        for my_dict in keyword_weight_list:
            my_dict = {k: v for k, v in my_dict.items() if v >= 0.03}  # tfidf算法取归一化前分数>=0.03的词

            weight_list = list(my_dict.values())
            for key in my_dict:
                my_dict[key] = np.e ** (my_dict[key]) / np.sum(np.e ** np.array(weight_list))  # softmax 归一化
    return keyword_weight_list

def cal_keywords_weight(title_weight_list, content_weight_list, top_k=5, title_weight=0.8):
    """
    合并 title 中的关键字权重与 content 中的关键字权重. 仅在content中出现的关键字并不舍去.

    :param title_weight_list: title 的关键字与对应权重 (list[dict])
    :param content_weight_list: content 的关键字与对应权重 (list[dict])
    :param title_weight: 标题中关键字的权重 (float).
        计算方式为: title_weight * title_weight + content_weight * (1 - title_weight)
            如果 title_weight = 1, 则仅考虑 title 中的关键字; (title_weight*1 + content_weight*0)
            如果 title_weight = 0, 则仅考虑content中的关键字. (title_weight*0 + content_weight*1)
    :return: 合并后的关键字与对应权重 (list[dict])
    """
    assert len(title_weight_list) == len(content_weight_list)

    keyword_weight_list = []
    for i in range(len(title_weight_list)):
        current_weight = {}
        keys = list(
            set(title_weight_list[i].keys()) | set(content_weight_list[i].keys()))  # title & content 所有关键字的并集
        for key in keys:
            try:
                current_weight[key] = title_weight_list[i][key] * title_weight + content_weight_list[i][key] * (
                        1 - title_weight)  # 关键字在 title 和 content 中均出现
            except:
                if key not in title_weight_list[i].keys():
                    current_weight[key] = content_weight_list[i][key] * (1 - title_weight)  # 仅在 content 中出现的关键字
                else:
                    current_weight[key] = title_weight_list[i][key] * title_weight  # 仅在 title 中出现的关键字
        keyword_weight_list.append(current_weight)

    for i in range(len(keyword_weight_list)):
        curr_key_value_list = [[k,v] for k, v in keyword_weight_list[i].items() if v > 0]  # 去掉关键词权重为0的关键字
        curr_key_list = sorted(curr_key_value_list, key=lambda k:k[1], reverse=True)[:min(top_k,len(curr_key_value_list))]    # 按 weight 讲叙排序
        keyword_weight_list[i] = [item[0] for item in curr_key_list if (not is_number(item[0]) and item[0][-2:] not in stopwords_black)] #去掉数字型的关键词
                   
    return keyword_weight_list



#未删除，依然保留
if __name__ == '__main__':
    title_weight = 0.8
    data = pd.read_csv('/Users/rain/Desktop/aidaily_articles.csv', error_bad_lines=False, encoding='utf-8')
    # 获取标题关键字与相应权重
    title_weight_list = get_keywords(data['title'],
                                          cut_method='tfidf',
                                          normalize_title_content=True)
    # 获取内容关键字与相应权重
    content_weight_list = get_keywords(data['content'],
                                            cut_method='tfidf',
                                            normalize_title_content=True)
    # 合并标题关键字与内容关键字的权重
    df = pd.DataFrame()
    df['title'] = data['title']
    df['description'] = data['description']
    df['keywords'] = cal_keywords_weight(title_weight_list,
                                                      content_weight_list,
                                                      top_k=5,
                                                      title_weight=title_weight)
    fileName = 'aidaily_1000_keywords.csv'
    df.to_csv(fileName)
    print('successfully write to file: ' + fileName)
