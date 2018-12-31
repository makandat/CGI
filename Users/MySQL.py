# -*- code=utf-8 -*-
# Version 0.50  2018-09-12
# Version 1.00  2018-10-03
#  sudo pip3 install mysql-connector-python
import mysql.connector

class MySQL :
    APPCONF = "AppConf.ini"

    # コンストラクタ
    def __init__(self, uid="", pwd="", db="", host="localhost") :
        self.__config = {"user":uid, "password":pwd, "host":host, "database":db}
        self.__rows = {}
        # パラメータが無効の場合は、AppConf.ini から取得する。
        if uid == "" :
            self.readAppConf()
        else :
            pass
        # 接続する。
        self.__client = mysql.connector.connect(**self.__config)
        # カーソルを取得する。
        self.__cursor = self.__client.cursor()

    # AppConf.ini を読んで接続情報を得る。
    def readAppConf(self) : 
        uid = ""
        pwd = ""
        db = ""
        host = "localhost"
        with open(MySQL.APPCONF) as f :
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

    # カーソル
    def cursor(self, sql) :
        self.__cursor.execute(sql)
        return self.__cursor
        
    # クエリーを行う。
    def query(self, sql) :
        self.__cursor.execute(sql)
        self.__rows = self.__cursor.fetchall()
        return self.__rows

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
            
    # カーソルを閉じる。
    def cursorClose(self) :
        self.__cursor.close()

    # 接続情報
    @property
    def connectInfo(self) :
        return (self.__config)
    
    
    
