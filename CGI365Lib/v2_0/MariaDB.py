# MariaDB.py v1.2 2024-01-03
import mariadb, json

# MariaDB class
class MariaDB:
  # constructor. config file = 'MariaDB.json'
  def __init__(self, user="", password="", database="", host="localhost"):
    self._conf = {"user":user, "password":password, "database":database, "host":host}
    if user == "":
      with open("MariaDB.json", "r") as f:
        self._conf = json.load(f)
        self._conn = mariadb.connect(user=self._conf["user"], password=self._conf["password"], host=self._conf["host"], database=self._conf["database"])
    else:
      self._conn = mariadb.connect(user=user, password=password, host=host, database=database)
    self._cur = self._conn.cursor()
    return

  # execute select query. data is tuple, result is array of tuple.
  def query(self, sql, data=None):
    if data is None:
      self._cur.execute(sql)
    else:
      self._cur.execute(sql, data)
    return self._cur.fetchall()

  # get scalar.
  def getValue(self, sql):
    self._cur.execute(sql)
    row = self._cur.fetchone()
    return row[0]

  # get one row.. row is tuple.
  def getRow(self, sql):
    self._cur.execute(sql)
    row = self._cur.fetchone()
    return row

  # execute non query sql. data is tuple.
  def execute(self, sql, data=None, commit=True):
    if data is None:
      self._cur.execute(sql)
    else:
      self._cur.execute(sql, data)
    if commit:
      self._cur.execute("COMMIT")

  # use database command
  def useDatabase(self, database, user=None):
    self._conf["database"] = database
    self._conn.close()
    if not (user is None):
      self._conf["user"] = user
    self._conn = mariadb.connect(user=self._conf["user"], password=self._conf["password"], host=self._conf["host"], database=self._conf["database"])
    return

  # 現在のデータベース
  @property
  def currentDB(self):
    return self._conf["database"]

  # 接続情報
  @property
  def conf(self):
    return self._conf
  
  # カーソル
  @property
  def cursor(self):
    return self._cur
  
  # 接続オブジェクト
  @property
  def conn(self):
    return self._conn
