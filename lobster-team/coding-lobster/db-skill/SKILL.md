# 数据库操作Skill

> 适用场景：MySQL/MongoDB/CSV/JSON数据增删改查
> 编程龙虾专用

---

## 数据库类型与连接

### SQLite（轻量，已有MCP支持）
- 文件型数据库，后缀 .db/.sqlite3
- 不需要安装服务器

### MySQL（需安装）
- 安装：pip install mysql-connector-python
- 连接：host/localhost，用户名/密码/数据库名

### MongoDB（需安装）
- 安装：pip install pymongo
- 连接：mongodb://host:port/

### CSV/JSON（最简单，已有）
- pandas.read_csv()
- pandas.read_json()

---

## SQLite标准模板

import sqlite3
import pandas as pd

def query_db(db_path, sql):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

def execute_db(db_path, sql, params=None):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    if params:
        cursor.execute(sql, params)
    else:
        cursor.execute(sql)
    conn.commit()
    result = cursor.fetchall()
    conn.close()
    return result

# 查询示例
df = query_db('data.db', 'SELECT * FROM users LIMIT 10')

# 插入示例
execute_db('data.db', 'INSERT INTO users (name, age) VALUES (?, ?)', ('test', 25))

---

## MySQL标准模板

import mysql.connector

def connect_mysql(host, user, password, database):
    return mysql.connector.connect(host=host, user=user, password=password, database=database)

def query_mysql(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

# 使用
conn = connect_mysql('localhost', 'root', 'password', 'mydb')
results = query_mysql(conn, 'SELECT * FROM users LIMIT 10')
conn.close()

---

## MongoDB标准模板

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
collection = db['users']

# 查询
for doc in collection.find({'age': {'': 20}}).limit(10):
    print(doc)

# 插入
collection.insert_one({'name': 'test', 'age': 25})

---

## 编程龙虾输出规范

1. 连接的数据库类型和路径
2. 执行的SQL/查询
3. 返回结果数量
4. 结果摘要（前5条）
