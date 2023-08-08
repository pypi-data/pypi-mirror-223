# DocsBot 使用说明

DocsBot 是一个命令行工具，提供了方便的方式来管理和查询你的资料库。

## 快速开始 Quick Start

```shell
$ pip install docsbot


$ docsbot
Please enter your OpenAI Key: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
usage: chatbase [-h] {addbase,listbase,deletebase,query} ...

positional arguments:
  {addbase,listbase,deletebase,query}

options:
  -h, --help            show this help message and exit
  
  
$ docsbot addbase /Users/jeffrey/Downloads/laws

Using vector store:  Qdrant
loading from dir: /Users/jeffrey/Downloads/laws
Added 4 document(s) to base base000x7uvrvegk9vv
Added /Users/jeffrey/Downloads/laws with ID base000x7uvrvegk9vv

$ docsbot listbase
+---------------------+-------------------------------+---------+
|          ID         |            Location           |  Count  |
+---------------------+-------------------------------+---------+
| base000x7uvrvegk9vv | /Users/jeffrey/Downloads/laws | 4 files |
+---------------------+-------------------------------+---------+

$ docsbot query base000x7uvrvegk9vv 什么是技术开发合同
Using vector store:  Qdrant
查询: 什么是技术开发合同
结果:  技术开发合同是当事人之间就新技术、新产品、新工艺、新品种或者新材料及其系统的研究开发所订立的合同。它包括委托开发合同和合作开发合同，并且应当采用书面形式。
来源文件：
1. 来源：/Users/jeffrey/Downloads/laws/中华人民共和国民法典.docx
   内容1.：第八百五十一条  技术开发合同是当事人之间就新技术、新产品、新工艺、新品种或者新材料及其系统的研究开发所订立的合同。  技术开发合同包括委托开发合同和合作开发合同。  技术开发合同应当采用书面形式。  当事人之间就具有实用价值的科技成果实施转化订立的合同，参照适用技术开发合同的有关规定。
   内容2.：第八百五十一条  技术开发合同是当事人之间就新技术、新产品、新工艺、新品种或者新材料及其系统的研究开发所订立的合同。  技术开发合同包括委托开发合同和合作开发合同。  技术开发合同应当采用书面形式。  当事人之间就具有实用价值的科技成果实施转化订立的合同，参照适用技术开发合同的有关规定。
   内容3.：第八百四十三条  技术合同是当事人就技术开发、转让、许可、咨询或者服务订立的确立相互之间权利和义务的合同。  第八百四十四条  订立技术合同，应当有利于知识产权的保护和科学技术的进步，促进科学技术成果的研发、转化、应用和推广。
   内容4.：第八百四十三条  技术合同是当事人就技术开发、转让、许可、咨询或者服务订立的确立相互之间权利和义务的合同。  第八百四十四条  订立技术合同，应当有利于知识产权的保护和科学技术的进步，促进科学技术成果的研发、转化、应用和推广。
Queried base with ID base000x7uvrvegk9vv with query 什么是技术开发合同




```


## 命令和参数

以下是 DocsBot 支持的命令及其参数：

```bash
$ docsbot addbase <dir>          # 用于添加一个新的资料库。 `<dir>`: 要添加的资料库的目录路径。
$ docsbot listbase               # 用于列出所有已添加的资料库。
$ docsbot deletebase <baseid>    # 用于删除一个已添加的资料库。 `<baseid>`: 要删除的资料库的ID。
$ docsbot query <baseid> <query> # 用于查询一个资料库。 `<baseid>`: 要查询的资料库的ID。 `<query>`: 查询字符串。
```



## 配置项

### Home目录
`docsbot` 默认使用目录 `$HOME/.docsbot`来存储自己的配置信息、资料库的元信息与索引数据等。
```python
# 该目录中的文件和文件夹
docsbot.env  -- 配置文件
base_data.json -- 资料库的元信息，比如ID、目录、文件数
vectors -- 对资料库Embedding后的向量索引数据的存储目录

```

### 配置文件
第一次运行时，请根据提示设置OpenAI的Key，`docsbot`自动保存到配置文件 
`$HOME/.docsbot/docsbot.env`中。

所有的配置项如下：
```env
OpenAI_KEY=xxxxxxxxx
VECTOR_STORE_TYPE="Chroma"  # 索引类型，目前支持Chroma、Qdrant
QDRANT_SERVER_URL="http://192.168.1.22:6333"
```


## FAQ

### Q：如何更换向量数据库为Qdrant？

修改配置文件，添加如下内容（修改为真实的Qdrant地址）：
```env
VECTOR_STORE_TYPE="Qdrant"
QDRANT_SERVER_URL="http://192.168.1.22:6333"
```




