# 新闻/文章主题主体及关键词提取

* 针对数据库（```AIDaily``` 和 ```acticles_1000```）中数据进行主题主题提取（机构，人物，机构人物关系，并将提取出的主体词汇加入词库中；
* 根据词库词汇提取文章关键词；
* 针对结果输出成api；

## Prerequisites

* [certifi](https://pypi.org/project/certifi/) Certifi is a carefully curated collection of Root Certificates
* [chardet](https://pypi.org/project/chardet/) This is a continuation of Mark Pilgrim's excellent chardet
* [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy) It uses Levenshtein Distance to calculate the differences between sequences in a simple-to-use package.
* [idna](https://pypi.org/project/idna/)
* [jieba](https://github.com/fxsjy/jieba) Chinese text segmentation
* [python-dateutil](https://pypi.org/project/python-dateutil/1.4/) The dateutil module provides powerful extensions to the standard datetime module
* [requests](https://2.python-requests.org/en/master/) Requests allows you to send organic, grass-fed HTTP/1.1 requests
* [scikit-learn](https://scikit-learn.org/stable/) Simple and efficient tools for data mining and data analysis
* [scipy](https://www.scipy.org/) a Python-based ecosystem of open-source software for mathematics
* [urllib3](https://urllib3.readthedocs.io/en/latest/) urllib3 is a powerful, sanity-friendly HTTP client for Python
* [zhon](https://zhon.readthedocs.io/en/latest/) Zhon is a Python library that provides constants commonly used in Chinese text processing
* [nltk](https://www.nltk.org/) a leading platform for building Python programs to work with human language data   
* [tensorflow](https://www.tensorflow.org/) TensorFlow is an end-to-end open source platform for machine learning
* [pyltp](https://github.com/HIT-SCIR/pyltp) Language Technology Platform 


## 脚本介绍
这个文件夹主要包含```3```个脚本：


- ```extract_keywords.py```

基于```机器之心```的脚本，使用tfidf方法提取文章的关键词。脚本使用文章的```title```和```content```信息进行分析，加以不同权重，输出分数高的前几个关键词。使用时需修改输入文件地址(```csv```格式)、输入文件对应字段名(```title```和```content```)、输出文件名。


- ```TF_PO.py```

使用```zh-NER-TF```：脚本使用文章的```title```和```content```信息进行分析，以一个csv文件为输入，输出一个dataframe其中包含：新闻title，人物，机构，人物机构关系等entity（该脚本的使用需要改动输入的csv，目前使用的是aidaily)。

- ```main```

使用```main```：
[main.py]脚本使用dataframe的```title```,```content```和```description```信息进行分析，以一个csv文件为输入，输出一个dataframe, 是```TF_PO.py```和```extract_keywords.py```的结合，先提取中其中的主题主体词，再进行关键词提取

- 需要改路径的有：
TF_PO.py
entity_keyword_api.py
extract_keywords.py
main.py## Acknowledgments
* Author： Yu Xia
* Contributor: [mosroot](https://github.com/mosroot)
