#!/usr/bin/env python
# encoding: utf8

import os
import time

import pymysql

from sh import gunicorn, python

DB_DATABASE = os.environ['DB_DATABASE']
DB_USER = os.environ['DB_USER']
DB_HOST = os.environ['DB_HOST']
DB_PASSWORD = os.environ['DB_PASSWORD']


def db_connect():
    for i in range(10):
        try:
            conn = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                passwd=DB_PASSWORD,
                db=DB_DATABASE,
                charset='utf8mb4')
            with conn.cursor() as cursor:
                sql = "show variables like '%char%';"
                cursor.execute(sql)
                result = cursor.fetchall()
                for item in result:
                    print(item)
                if result:
                    return True
            conn.close()
        except Exception as e:
            print(str(e))
        time.sleep(2)
    return False


def db_init():
    try:
        if not os.path.exists('migrations'):
            if not os.path.isdir('migrations'):
                python('manage.py', 'db', 'init')

        try:
            python('manage.py', 'db', 'migrate')
        except Exception as e:
            print(e.message)
            print('migrate 错误，数据库不是新的')

            try:
                # 如果数据库中残留之前的alembic_version跟init之后的记录id不一致，会导致这步错误
                conn = pymysql.connect(
                    host=DB_HOST,
                    user=DB_USER,
                    passwd=DB_PASSWORD,
                    db=DB_DATABASE,
                    charset='utf8mb4')
                with conn.cursor() as cursor:
                    sql = "drop table if exists alembic_version;"
                    cursor.execute(sql)
                conn.close()
                python('manage.py', 'db', 'migrate')
            except Exception as e:
                print('尝试删除表后仍然出错')

        python('manage.py', 'db', 'upgrade')

    except Exception as e:
        print(e.stderr)
        exit(1)


if db_connect():
    db_init()
    gunicorn('-b', '0.0.0.0', '--reload', 'blog:app')
