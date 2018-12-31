#!/usr/bin/env python3
#  ユーザ管理クラス  ver 1.10  2018-10-10
from MySQL import MySQL
from DateTime import DateTime
import hashlib

class Users(MySQL) :
  # コンストラクタ
  def __init__(self) :
    super().__init__(uid="")

  # 新規ユーザを登録する。
  def add_new(self, userid: str, password: str, info="") :
    date = DateTime()
    today = date.toDateString()
    enc_password = Users.get_sha256(password)
    sql = f"INSERT INTO `Users`(userid, password, info, registered) VALUES('{userid}', '{enc_password}', '{info}', '{today}')"
    self.execute(sql)

  # ユーザ情報を変更する。
  def modify_info(self, userid: str, info: str) :
    sql = f"UPDATE `Users` SET info='{info}' WHERE userid='{userid}'"
    self.execute(sql)

  # パスワードを更新する。
  def update_password(self, userid: str, password: str) :
    enc_password = Users.get_sha256(password)
    sql = f"UPDATE Users SET password = '{enc_password}' WHERE userid='{userid}'"
    self.execute(sql)
  
  # 暗号化されてないパスワードを暗号化する。(手動でユーザを追加したときに使う)
  def encrypt_passwords(self) :
    sql = "SELECT userid, password FROM `Users` WHERE expired = 0"
    rows = self.query(sql)
    for row in rows :
      userid = row[0]
      password = row[1]
      if len(password) <= 12 :
        enc_password = Users.get_sha256(password)
        sql = f"UPDATE `Users` SET `password`='{enc_password}' WHERE `userid` = '{userid}'"
        print(sql)
        self.execute(sql)

  # 指定したユーザIDを無効にする。
  def set_expired(self, userid: str) :
    sql = f"UPDATE Users SET expired = 1 WHERE userid='{userid}'"
    self.execute(sql)

  # ユーザ一覧を HTML テーブルまたはCSVとして返す。
  def userlist(self, all=False, csv=False) -> str:
    sql = "SELECT * FROM `Users`"
    if all == False :
      sql += " WHERE expired = 0"
    cur = self.cursor(sql)
    if csv :
      buff = "id,userid,password,priv,info,registered,expired\n"
    else :
      buff = "<table>\n"
      buff += "<tr><th>id</th><th>userid</th><th>password</th><th>priv</th><th>info</th><th>registered</th><th>expired</th></tr>\n"
    for (id, userid, password, priv, info, registered, expired) in cur :
      if csv :
        buff += f"{id},{userid},{password},{priv},{info},{registered},{expired}\n"
      else :
        buff += "<tr>"
        buff += f"<td>{id}</td>"
        buff += f"<td>{userid}</td>"
        buff += f"<td>{password}</td>"
        buff += f"<td>{priv}</td>"
        buff += f"<td>{info}</td>"
        buff += f"<td>{registered}</td>"
        buff += f"<td>{expired}</td>"
        buff += "</tr>\n"
    if not csv :
      buff += "</table>\n"
    return buff

  # ユーザ userid のパスワードを照合する。
  def authorize(self, userid: str, password: str) -> bool :
    rows = self.query(f"SELECT password FROM Users WHERE userid='{userid}'")
    b = False
    if len(rows) == 1 :
      row = rows[0]
      b = row[0] == Users.get_sha256(password)
    return b

  # ユーザの特権レベルを得る。
  def getPriv(userid:str) -> int :
    priv = -1
    rows = self.query(f"SELECT priv FROM Users WHERE userid='{userid}'")
    if len(rows) == 1 :
      row = rows[0]
      priv = int(row[0])
    return priv

  # 生パスワードの sha256 を得る。
  @staticmethod
  def get_sha256(password: str) -> str:
    s = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return s

