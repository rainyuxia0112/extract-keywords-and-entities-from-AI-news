# 基于机器之心网站文章与新闻数据API搭建

该任务可以基于机器之心网站文章与新闻数据，分析统计出每篇文章与新闻的主题主体以及关键词并以此搭建简单API。

# Get Started

- 安装前准备

* 此任务需要在python3.X环境下进行，请将默认的python版本调整至3.X

* 请在terminal中重新激活一个独立开发环境用于此任务

```shell
source ./bin/activate   # 或者使用. ./bin/activate
```

- 安装依赖

```shell
pip3 install -r requirement.txt # 该任务的requirement在api文件夹中
```
* Note：安装Flask时注意安装官网要求进行测试与安装：[flask](http://flask.pocoo.org/)

- 执行下列命令，运行脚本
```shell
FLASK_APP=entity_keyword_api.py flask run #也可以直接使用python3 entity_keyword_api.py
* Serving Flask app "entity_keyword_api"
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

# 运行说明

* 该项目为针对新闻文章提取出的主题主体与关键词搭建的一个简单API示例

### 输入文件格式要求

输入的 csv 文件应当放在 test 目录中，并包含以下字段：
- **title**
- **content**
- **date**
- **description** (optional)

### API接口

通过修改 link： ```http://127.0.0.1:5000/```  完成参数的选择。
输入网址：```http://127.0.0.1:5000/```进入主页；```http://127.0.0.1:5000/api/resources/keywords```进入关键词Api网页；```http://127.0.0.1:5000/api/resources/entity```进入主题主体Api网页；



|URL|Method|Return
|----|--------|----
|*http://127.0.0.1:5000/*|GET|
|*http://127.0.0.1:5000/api/resources/keywords*|GET|json格式的分析结果
|*http://127.0.0.1:5000/api/resources/entity*|GET|json格式的分析结果


    斜体、粗体、删除线可混合使用




# Contributors
[Mos Zhang](https://github.com/mosroot), [Yu Xia](https://github.com/rainyuxia0112)
