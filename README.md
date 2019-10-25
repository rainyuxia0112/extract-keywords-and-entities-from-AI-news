# Extract keywords and entities from AI News/Articles 

This duty is to extract keywords and entities based on AI news 

# Get Started

- Preparation before runnning

* This duty needs to be done in python3.X environment

* Needs to activate a new python enviroment

```shell
source ./bin/activate   # or use. ./bin/activate
```

- Installation

```shell
pip3 install -r requirement.txt
```
* notice: after ```import nltk ``` in python, you need to download some dictionaries below

```python
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

```

- Directory

```python
dict_dir = './dictionary'  including all dictionaries will be used
test = './models/test' # including all training and testing data
data = './models/test/aidaily_articles.csv'  # input 
stop_words_path = './dictionary/stop_words.dat'  # stop words
black_txt = './dictionary/black_txt' # all black dictionary
tech_txt = './dictionary/tech_txt' # tech
dict_txt = './dictionary/dict_txt' # jieba
topN = 5  #  the number of keywords that each acticle will keep
```

- run the script
```shell
python3 main.py #也可以直接使用python main.py
```

# Introduction to this package

### introduction to files

[models](https://github.com/rainyuxia0112/duty/tree/master/models) includes all models we need

[script](https://github.com/rainyuxia0112/duty/tree/master/script) includes all scripts we need

[test](https://github.com/rainyuxia0112/duty/tree/master/models/test) includes input file and output file

### input file requirements

input file needs to include the features below
- **title**
- **content**
- **date**
- **description** (optional)

### output

- **out_entity.csv**
- **out_keywords.csv**   
- **out_new_keywords.csv**  

### parameter selection

in python, modifying `param_grid` to finish parameter selection
```python
param_grid = {'articleType':'AIDaily', 
              'method' : 'zh_NER_TF', # method to deal with entity
              'contentMode' : [1, 1, 0],
              'useExpanded' : [1, 0, 1],
              'similarity' : 50,
              'title_weight': 0.8, 
              'cut_method': 'tfidf',
              'top_k': 5, 
              'normalize_title_content': True

        }
```

# introduction to scripts

- ```extract_keywords.py```

Based on AI news, we use tfidf to extract keywords from acticles; this script uses ```title``` and ```content``` from acticles to do analysis.

- ```TF_PO.py```

Based on AI news, we use LSTM to extract entities from acticles; this script uses ```title``` and ```content``` from acticles to do analysis.

- ```BosonNLP_PO```

this is an Api to extract entities from acticles

# Contributors
[Penghui Wei](https://github.com/Determined22/zh-NER-TF/), [Yu Xia](https://github.com/rainyuxia0112)
