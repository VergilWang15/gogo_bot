# db_utils.py
import os
import sqlite3
from sqlite3 import Error

import threading

# 线程本地数据
threadLocal = threading.local()

# 创建 SQLite 连接
def create_connection():
    if not hasattr(threadLocal, "conn"):
        try:
            db_path = './var/database.sqlite3'
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            threadLocal.conn = sqlite3.connect(db_path, check_same_thread=False)
        except Error as e:
            print(e)
    return threadLocal.conn

# 创建表
def create_table(conn):
    try:
        sql_create_table = """ CREATE TABLE IF NOT EXISTS commands (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        count integer NOT NULL
                                    ); """
        c = conn.cursor()
        c.execute(sql_create_table)
    except Error as e:
        print(e)

# 更新命令计数
def update_command_count(conn, command):
    try:
        c = conn.cursor()
        c.execute("SELECT count FROM commands WHERE name = ?", (command,))
        result = c.fetchone()
        if result is None:
            c.execute("INSERT INTO commands(name, count) VALUES(?,?)", (command, 1))
        else:
            count = result[0]
            c.execute("UPDATE commands SET count = ? WHERE name = ?", (count+1, command))
        conn.commit()
    except Error as e:
        print(e)