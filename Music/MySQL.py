# -*- coding: utf-8 -*-
# Version 0.50  2018-09-12
# Version 1.00  2018-10-03
# Version 1.10  2018-12-01
# Version 1.20  2019-04-09
# Version 1.30  2019-07-20
# Version 2.00  2021-09-11
# Version 2.10  2021-09-15
#    To install mysql connector
#  sudo pip3 install mysql-connector-python
import json, os
import mysql.connector
import Common

class MySQL :
    APPCONF = "AppConf.ini"

    # コンストラクタ
    def __init__(self, uid="", pwd="", db="", host="localhost") :
        self.__config = {"user":uid, "password":pwd, "host":host, "database":db}
        self.__rows = {}
        # パラメータが無効の場合は、AppConf.ini から取得する。
        if uid == "" :
            # APPCONF を使う。
            self.readAppConf()
        elif pwd == "" and db == "" :
            # uid をコンフィグファイルとして使う
            self.readAppConf(uid)
        else :
            raise "No connection info."
        # 接続する。
        self.__client = mysql.connector.connect(**self.__config)
        # カーソルを取得する。
        self.__cursor = self.__client.cursor()

    # AppConf.ini を読んで接続情報を得る。
    def readAppConf(self, conf=None) :
        uid = ""
        pwd = ""
        db = ""
        host = "localhost"
        if conf == None :
            conf = MySQL.APPCONF
        #Common.log(conf)
        root, ext = os.path.splitext(conf)
        if ext == '.ini' :
            with open(conf) as f :
                for line in f :
                    pair = line.strip().split('=')
                    if (pair[0] == 'uid') :
                        uid = pair[1]
                    elif (pair[0] == 'pwd') :
                        pwd = pair[1]
                    elif pair[0] == 'db' :
                        db = pair[1]
                    elif pair[0] == 'host' :
                        host = pair[1]
                    else :
                        pass
            self.__config = {"user":uid, "password":pwd, "host":host, "database":db}
        elif ext == ".json" :
            with open(conf) as f :
                str = f.read()
                #Common.log("MySQL.readAppConf : " + str)
                self.__config = json.loads(str)
        else :
            raise "No MySQL config file."

    # カーソル
    def cursor(self, sql) :
        self.__cursor.execute(sql)
        return self.__cursor

    # クエリーを行う。
    def query(self, sql) :
        self.__cursor.execute(sql)
        self.__rows = self.__cursor.fetchall()
        return self.__rows

    # 結果が1行のクエリーを行う。
    def getRow(self, sql) :
        self.__cursor.execute(sql)
        self.__rows = self.__cursor.fetchall()
        if self.__rows :
          return self.__rows[0]
        else :
          return None

    # クエリー結果行数を取得する。
    @property
    def rows(self) :
        return len(self.__rows)

    # コマンドを実行する。
    def execute(self, sql) :
        n = 0
        try :
            n = self.__cursor.execute(sql)
            self.__client.commit()
        except :
            self.__client.rollback()
            raise
        return n

    # 値を1つだけ返すクエリーを実行し、その値を得る。
    def getValue(self, sql) :
        result = None
        self.__cursor.execute(sql)
        self.__rows = self.__cursor.fetchall()
        if len(self.__rows) >= 1 :
            row = self.__rows[0]
            result = row[0]
        return result

    # カーソルを閉じる。
    def cursorClose(self) :
        self.__cursor.close()

    # カラム名を得る。
    def getFieldNames(self, table="") :
      if table != "" :
        self.cursor("SELECT * FROM " + table + " LIMIT 1")
      num_fields = len(self.__cursor.description)
      field_names = [i[0] for i in self.__cursor.description]
      return field_names

    # 接続情報
    @property
    def connectInfo(self) :
        return (self.__config)



