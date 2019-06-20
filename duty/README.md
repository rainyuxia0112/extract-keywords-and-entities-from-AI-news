# 主题提取

这个文件夹主要包含```3```个脚本：


- ```extract_keywords.py```

基于```机器之心```的脚本，使用tfidf方法提取文章的关键词。安装依赖参考：```requirements.txt```。脚本使用文章的```title```和```content```信息进行分析，加以不同权重，输出分数高的前几个关键词。使用时需修改输入文件地址(```csv```格式)、输入文件对应字段名(```title```和```content```)、输出文件名。


- ```TF_PO.py```

使用```zh-NER-TF```：
脚本使用文章的```title```和```content```信息进行分析，以一个csv文件为输入，输出一个dataframe其中包含：新闻title，人物，机构，人物机构关系等entity（该脚本的使用需要改动输入的csv，目前使用的是aidaily), 安装依赖参考：```requirements.txt```。

- ```main```

使用```main```：
[main.py]脚本使用dataframe的```title```,```content```和```description```信息进行分析，以一个csv文件为输入，输出一个dataframe, 是```TF_PO.py```和```extract_keywords.py```的结合，先提取中其中的主题主体词，再进行关键词提取

### Documents
#### Stanford Named Entity Recognizer (NER): [https://nlp.stanford.edu/software/CRF-NER.shtml](https://nlp.stanford.edu/software/CRF-NER.shtml)

* 需要的文件已在```docs```路径下：[stanford-ner-2014-08-27](https://github.com/chainn/synced_datalab/edit/master/Xiaoxue/NER/docs/stanford-ner-2014-08-27)


# 百家姓文件

* 需要的文件已在```docs```路径下：[last name.txt](https://github.com/chainn/synced_datalab/edit/master/Xiaoxue/NER/docs/last%20name.txt)

# 本地词典文件

* 需要的文件已在```docs```路径下：[combined-people.txt](https://github.com/chainn/synced_datalab/edit/master/Xiaoxue/NER/docs/combined-people.txt)  ，[combined-organization.txt](https://github.com/chainn/synced_datalab/edit/master/Xiaoxue/NER/docs/combined-organization.txt) ，[combined-conference.txt](https://github.com/chainn/synced_datalab/edit/master/Xiaoxue/NER/docs/combined-conference.txt) 。


# Deployment
使用工具：[zh-NER-TF](https://github.com/Determined22/zh-NER-TF) 提取内容如下：
* 机构名
* 人名（包含人物相关的职位信息及相关时间）
* 人物-机构关系对
* 机构-机构间的投融资信息（包含时间、轮次、金额）


### Parameters：

* articleType：必填，```string```；
* articleUrl：对于给定url识别文章的情况必填，对于自动识别AIDaily类型的多篇文章可缺省， ```sting```；
* autoCrawlAI：对于自动识别AIDaily类型的多篇文章必填为```True```，其他情况可缺省；
* articleNumberAI：对于自动识别AIDaily类型的多篇文章可选填需要提取的文章数量，```int```，默认为10篇，其他情况可缺省；
* contentMode：(仅对NER_AO)是否使用```[标题，文章内容，短描述]```进行分析，```1```表示使用，```0```表示不使用，默认为```[1,1,0]```，即使用标题和文章内容，不使用短描述；
* paperMode：(仅对NER_PA)是否通过```[关键词, 特殊字符, 长英文]```提取文章，```1```表示使用，```0```表示不使用，默认为```[1,1,1]```，即三种方法均使用；
* useExpanded：是否对```[机构名, 人名, 其他名词]```进行前后扩展，```1```表示扩展，```0```表示不扩展，默认为```[0,0,1]```，即三种方法均使用；
* accurateMode：是否使用```StanfordNERTagger```对英文进行词性标注，```True```表示使用```StanfordNERTagger```(速度较慢，准确度较高)，```False```表示使用```nltk.ne_chunk```，默认为```False```
* dirName：输出文档的储存路径，默认在当前目录下新建一个```outputs```文件夹储存输出的txt文件，文件名为对应的文章标题名。（改动后没有再用到该参数，但是仍然保留了该参数作为keyword）

- 需要改路径的有：
TF_PO.py
entity_keyword_api.py
extract_keywords.py
main.py



# 新闻/文章主题主体及关键词提取

针对数据库（```AIDaily``` 和 ```acticles_1000```）中数据进行主题主题提取（机构，人物，机构人物关系，并将提取出的主体词汇加入词库中；
根据词库词汇提取文章关键词；
针对结果输出成api；

### Prerequisites

certifi [https://pypi.org/project/certifi/]
chardet [https://pypi.org/project/chardet/]
fuzzywuzzy [https://github.com/seatgeek/fuzzywuzzy]
idna [https://pypi.org/project/idna/]
jieba [https://github.com/fxsjy/jieba]
python-dateutil [https://pypi.org/project/python-dateutil/1.4/]
requests [https://2.python-requests.org/en/master/]
scikit-learn [https://scikit-learn.org/stable/]
scipy [https://www.scipy.org/]
urllib3 [https://urllib3.readthedocs.io/en/latest/]
zhon [https://zhon.readthedocs.io/en/latest/]
nltk [https://www.nltk.org/]        
tensorflow [https://www.tensorflow.org/]
pyltp [https://github.com/HIT-SCIR/pyltp]


## 脚本介绍
这个文件夹主要包含```3```个脚本：


- ```extract_keywords.py```

基于```机器之心```的脚本，使用tfidf方法提取文章的关键词。脚本使用文章的```title```和```content```信息进行分析，加以不同权重，输出分数高的前几个关键词。使用时需修改输入文件地址(```csv```格式)、输入文件对应字段名(```title```和```content```)、输出文件名。


- ```TF_PO.py```

使用```zh-NER-TF```：脚本使用文章的```title```和```content```信息进行分析，以一个csv文件为输入，输出一个dataframe其中包含：新闻title，人物，机构，人物机构关系等entity（该脚本的使用需要改动输入的csv，目前使用的是aidaily)。

- ```main```

使用```main```：
[main.py]脚本使用dataframe的```title```,```content```和```description```信息进行分析，以一个csv文件为输入，输出一个dataframe, 是```TF_PO.py```和```extract_keywords.py```的结合，先提取中其中的主题主体词，再进行关键词提取


## Acknowledgments
Author： Yu Xia
Contributor: Mos[https://github.com/mosroot]
