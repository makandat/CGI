#!/usr/bin/env python3
#  ユーザ管理クラス  ver 1.21  2019-09-16
from MySQL import MySQL
from DateTime import DateTime
import hashlib
import Common

class Users(MySQL) :
  # コンストラクタ
  def __init__(self) :
    super().__init__(uid="")
    Common.init_logger("/home/user/log/WebPage.log")

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
    Common.log("authorize")
    b = False
    try :
      passwd = str(self.getValue(f"SELECT password FROM Users WHERE userid='{userid}'"))
      Common.log(password)
      # パスワードの確認
      Common.log(Users.get_sha256(password))
      if passwd == str(Users.get_sha256(password)):
        Common.log("パスワードの確認 OK")
        b = True
        if b :
          # 期限切れの確認
          expired = self.getValue(f"SELECT expired FROM Users WHERE userid='{userid}'")
          Common.log("期限切れの確認 " + str(expired))
          b = int(expired) == 0
    except :
      Common.log("pass")
      pass 
    return b

  # ユーザの特権レベルを得る。
  def getPriv(self, userid:str) -> int :
    priv = -1
    try :
      priv = int(self.getValue(f"SELECT priv FROM Users WHERE userid='{userid}'"))
    except :
      pass 
    return priv

  # 生パスワードの sha256 を得る。
  @staticmethod
  def get_sha256(password: str) -> str:
    s = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return s
    
  # ユーザが登録済みかどうか (登録済みなら True を返す。)
  def exists(self, userid) :
    n = int(self.getValue(f"SELECT count(*) FROM Users WHERE userid='{userid}'"))
    return n > 0
    
  # ログインユーザが有効かどうかを返す。
  #   userp: user id from Param
  #   userc: user id from Cookie
  #   operation:
  #     1: change password
  #     2: change info
  #     3: add new user 
  #     4: expire user
  def isValidUser(self, userp:str, userc:str, operation:int) -> bool :
    # ログインしていない場合は無効
    if userc == '' :
      return False 
    # operation
    if operation == 1 : # パスワードの変更 (当人と管理者のみ可能)
      if userp == userc :
        return True
      elif self.getPriv(userc) == 2 :
        return True
      else :
        return False
    elif operation == 2 : # ユーザ情報変更 (管理者のみ可能)
      if self.getPriv(userc) == 2 :
        return True
      else :
        return False
    elif operation == 3 : # 新規ユーザ追加 (管理者のみ可能）
      if self.getPriv(userc) == 2 :
        return True
      else :
        return False
    elif operation == 4 : # ユーザ有効期限終了 (管理者のみ可能）
      if self.getPriv(userc) == 2 and userp != userc :
        return True
      else :
        return False
    else :
      return False
    return True

