# 新闻/文章主题主体及关键词提取

该任务可以基于机器之心网站文章与新闻数据，分析统计出每篇文章与新闻的主题主体以及关键词。

# Get Started

- 安装前准备

* 此任务需要在python3.X环境下进行，请将默认的python版本调整至3.X

* 请在terminal中重新激活一个独立开发环境用于此任务

```shell
source ./bin/activate   # 或者使用. ./bin/activate
```

- 安装依赖

```shell
pip3 install -r requirement.txt
```
* 可能出现的问题：在 ``` import nltk ``` 后会需要download一些词库，请先使用``` python3 ```进入python交互模式,请执行以下操作：

```python
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

```

- 路径设置

```python
dict_dir = './dictionary'  # 包含所需用到的所有词典
stop_words_path = './dictionary/stop_words.dat'  # 停用词文件路径
test = './models/test' # 包含所有测试用的数据，在进行脚本时，可以将新数据放在该位置
data = './models/test/aidaily_articles.csv'  # 输入 csv 路径
topN = 5  # 每篇文章保留前5个关键词
```

- 执行下列命令，运行脚本
```shell
python3 main.py #也可以直接使用python main.py
```

# 运行说明

### 项目结构说明

[models](code) 为该项目的源代码和主要模型搭建。

[script](script) 为提取关键词和提取主题主体词脚本。

[test](test) 存放输入文件和输出文件。

### 输入文件格式要求

输入的 csv 文件应当放在 test 目录中，并包含以下字段：
- **title**
- **content**
- **date**
- **description** (optional)

### 输出文件

输出的 csv 文件在 test 目录中，并包含以下两个csv文件：
- **out_entity.csv**
- **out_keywords.csv**


### 参数选择

通过修改 `param_grid` 完成参数的选择。
```python
param_grid = {'articleType':'AIDaily', # 新闻类型
              'method' : 'zh_NER_TF', # method to deal with entity
              'contentMode' : [1, 1, 0],
              'useExpanded' : [1, 0, 1],
              'title_weight': 0.8, #标题所占比重
              'cut_method': 'tfidf',
              'top_k': 5, # 每篇新闻选择多少个关键词
              'normalize_title_content': True

        }
```

# 脚本介绍
这个文件夹包含```4```个主要脚本：

- ```extract_keywords.py```

基于```机器之心```的脚本，使用tfidf方法提取文章的关键词。脚本使用文章的```title```和```content```信息进行分析，加以不同权重，输出分数高的前几个关键词。

- ```TF_PO.py```

使用```zh-NER-TF```：脚本使用文章的```title```和```content```信息进行分析，输出信息包含：新闻标题，新闻中包含的人物，机构，人物机构关系。（该脚本的使用需要改动输入的csv，目前使用的是aidaily)。

- ```BosonNLP_PO```

使用```BosonNLP```：脚本使用文章的```title```和```content```信息进行分析，输出信息包含：新闻标题，新闻中包含的人物，机构，人物机构关系。（该脚本的使用需要改动输入的csv，目前使用的是aidaily)。

- ```main```

使用```main```：脚本使用新闻/文章的```title```和```content```信息进行分析，提取新闻/文章的主题主体以及关键词。

# 文件夹介绍
这个文件夹主要包含```4```个文件夹：

- ```models```
该文件夹中包含了主要脚本```main```运行时需要的主要脚本： ```TF_PO```， ```extract_keywords```和```BosonNLP_PO```

- ```dictionary```
该文件夹包含了所有脚本需要用到的词库（停用词典，主体机构词典， 主体人物词典，百家姓词典等）

- ```script```
该文件夹包含了```TF_PO```， ```BosonNLP_PO``` 和```extract_keywords``` 3个脚本，可以单独运行

- ```api```
该文件夹包含了```entity_keyword_api```主要用于将训练得到的主题主体词汇和关键词导出成API

# Contributors
[Mos Zhang](https://github.com/mosroot), [Yu Xia](https://github.com/rainyuxia0112)
