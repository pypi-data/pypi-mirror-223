
### 安装
```shell
pip install smart_vector
```
### 使用方法
```python
from smart_vector import SmartVectorDB, Text2VecEmbeddingFunction
# 定义向量转化函数
text_vector = Text2VecEmbeddingFunction()

# 数据库连接
connect_dict = {
    'host': 'xxx',
    'port': 9030,
    'user': 'xxxx',
    'password': 'xxx',
    'db': 'smartdb'
}
mydb = SmartVectorDB(db_config=connect_dict, load_host='xxx', text_vector=text_vector)

# 插入数据
mydb.add(collection='test', sr='测试', documents=['中国有一个北京', '北京在中国', '台湾是中国的'])
mydb.add(collection='test', sr='测试', documents=['中国有一个北京1', '北京在中国1'],
         categorys=['A1', 'A1'], metadatas=[{'s': 's1'}, {'s': 's2'}])

# 查询
query = """天安门\ncollection='test' and sr = '测试' and document like '%北京%'\ndocument,sr,c,get_json_string(m, 'ans') as answer\n3"""
print(mydb.get(query))

#[['document', 'sr', 'c', 'distance'], ('中国有一个北京1', '测试', 'A1', 272.8261536366944), ('中国有一个北京', '测试', '', 272.8261536366944), ('中国有一个北京', '测试', '', 272.8261536366944)]

```



### 部署

```bash
pip install -r requirements.txt

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser


#启动数据
python3 manage.py runserver 0.0.0.0:8000
```
