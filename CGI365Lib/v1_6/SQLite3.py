# -*- coding: utf-8 -*-
# SQLite3.py
#   ver 1.0  2023-03-26
import sqlite3

# クエリーを実行する。
def query(db, sql):
  con = sqlite3.connect(db)
  cur = con.cursor()
  cur.execute(sql)
  result = cur.fetchall()
  con.close()
  return result

# 値を１つだけ返すクエリーを実行する。
def getValue(db, sql):
  con = sqlite3.connect(db)
  cur = con.cursor()
  cur.execute(sql)
  row = cur.fetchone()
  con.close()
  return row[0]

# 1 行だけを返すクエリーを実行する。
def getRow(db, sql):
  con = sqlite3.connect(db)
  cur = con.cursor()
  cur.execute(sql)
  row = cur.fetchone()
  con.close()
  return row

# コマンドを実行する。
def execute(db, sql):
  con = sqlite3.connect(db)
  con.execute(sql)
  con.commit()
  con.close()
  return
