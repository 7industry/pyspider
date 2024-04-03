#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:      test
# Date:      2020/4/14
__Author__ = 'chen'
#-------------------------------------------------------------------------------

import sqlite3


# 连接数据库(如果不存在则创建)
conn = sqlite3.connect('testDB.db')
print("Opened database successfully")

# 创建游标
cursor = conn.cursor()


# 创建表
sql = 'CREATE TABLE Student(id integer PRIMARY KEY autoincrement, Name  varchar(30), Age integer)'
cursor.execute(sql)


# 插入数据
sql = "INSERT INTO Student(Name, Age) VALUES(\'love\', 22)"
cursor.execute(sql)
 
# 插入数据 2
data = ('love2', 2221) # or ['love2', 2221]
sql = "INSERT INTO Student(Name, Age) VALUES(?, ?)"
cursor.execute(sql, data)


 
# 查询数据
sql = "select * from Student"
values = cursor.execute(sql)
for i in values:
    print(i)
 
# 查询数据 2
sql = "select * from Student where id=?"
values = cursor.execute(sql, (1,))
for i in values:
    print('id:', i[0])
    print('name:', i[1])
    print('age:', i[2])



# 关闭游标
cursor.close()

# 提交事物
conn.commit()

# 关闭连接
conn.close()



