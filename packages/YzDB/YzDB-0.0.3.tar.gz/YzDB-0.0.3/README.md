YzDB 提供一系列简单的方法来操作数据库，让用户无需掌握对应的sql语句。

- 本package基于sqlalchemy
- 目前支持: MySQL, SQLite

link: [https://bagelquant.com/](https://bagelquant.com/)

# 快速使用


```python
# mysql connection
from YzDB import create_mysql_conn
# sqlite connection
from YzDB import create_sqlite_conn

import pandas as pd

# 创建一个connection对象
conn = create_mysql_conn(
        host='localhost',
        port=3306,
        user='root',
        password='123456',
				db_name='test'  # 可选参数，默认为空
    )

# 一些基础操作

# 添加表格，只有id列，需要添加列
conn.add_table(table_name='test_table')
# 向表格中添加列
conn.add_column(table_name='test_table', 
                column_name='test_int', 
                column_type='INT',
                comment='测试列'  # 可选参数，默认为空
                )  
# 创建一个pd.DataFrame数据
test_data = pd.DataFrame({'test_int': [1, 2, 3, 4, 5]})
# 向表格中添加数据
conn.add_data(table_name='test_table',
              data=test_data)
# 查询表格中的数据
print(conn.query_data(table_name='test_table'))

# 删除表格
conn.drop_table(table_name='test_table')
```

# 常用操作


## 数据库结构方面


### 查看

1. 查看所有表名列表

### 操作

1. 添加表
2. 删除表
3. 修改表描述
4. 删除表描述

## 表内操作


### 查看 query

1. 查看表列名
2. 查看所有数据
3. 查看所选列的数据
4. 根据筛选条件筛选
5. 在某一列中搜索（基于LIKE语句）

### 添加 add

1. 添加列
2. 添加索引
3. 添加行（添加数据）

### 删除 drop

1. 删除列
2. 删除列描述
3. 删除行

### 修改 modify

1. 修改某一个位置的数据
2. 修改列名
3. 修改列描述

## 通用类


- 执行sql语句
- 执行sql文件

# 程序结构
![程序结构](structure.png)