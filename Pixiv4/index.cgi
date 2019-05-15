#!/usr/bin/env python3
#!C:\Program Files (x86)\Python37\python.exe
#  Pixiv Clip by Python3 v4.10  2019-05-16
#    Pixiv のイラストを管理するアプリ。
from WebPage import WebPage
from MySQL import MySQL

# HTML ページの定義
class Pixiv4(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL()
    self.setPlaceHolder('message', '')
    self.setPlaceHolder('view', 'detail')
    if self.isCookie('view') :
      self.view = self.getCookie('view')
      self.setPlaceHolder('view', 'icons' if self.view == 'detail' else 'detail')
    else :
      self.view = 'detail'
      self.setCookie('view', 'detail')
    # ポストバックか？
    if self.isParam('submit') :
      # 作者検索
      if self.isParam('creator') :
        creator = "%" + self.getParam('creator') + "%"
        # 作者一覧を表示する。
        self.showCreators(creator)
      else :
        # 作者一覧を表示する。
        self.showCreators()
    elif self.isParam('view') :
      view = self.getParam('view')
      if view == 'icons' :
        self.setCookie('view', 'icons')
        self.view = 'icons'
        self.setPlaceHolder('view', 'detail')
        # 作者一覧をアイコン表示する。
        self.showIcons()
      else :
        self.setCookie('view', 'detail')
        self.view = 'detail'
        self.setPlaceHolder('view', 'icons')       
        # 作者一覧を詳細表示する。
        self.showCreators()
    else :
      # 作者一覧を詳細表示する。
      self.showCreators()
    return

  # 作者一覧を表示する。
  def showCreators(self, creator="") :
    # 作者と登録数を得る。
    if creator == "" :
      sql = "SELECT creator, count(creator) AS count FROM Pixiv3 GROUP BY creator ORDER By creator"
    else :
      sql = f"SELECT creator, count(creator) AS count FROM Pixiv3 WHERE creator LIKE '{creator}' GROUP BY creator ORDER By creator"
    rows = self.__mysql.query(sql)
    if len(rows) == 0 :
      self.setPlaceHolder('message', '作品が登録されていません。')
      self.setPlaceHolder('creators', '')
      return
    buff = "<tr><th>作者</th><th>登録数</th><th>タグ</th><th>登録イメージ</th></tr>"
    for row in rows :
      creator = row[0]
      count = row[1]
      # もしあれば、作者の最新のカテゴリータグを得る。
      sql = "SELECT tags FROM Pixiv3 WHERE creator='{0}' AND tags <> ''".format(creator)
      tagrows = self.__mysql.query(sql)
      n = len(tagrows) - 1
      if n >= 0 :
        tags = tagrows[n][0]
      else :
        tags = ""
      # もしあれば、作者の最新のイメージを得る。
      sql = "SELECT bindata FROM Pixiv3 WHERE creator='{0}' AND bindata > 0".format(creator)
      bdrows = self.__mysql.query(sql)
      n = len(bdrows) - 1
      if n >= 0 :
        bdid = bdrows[n][0]
        bindata = f"<img src=\"extract.cgi?id={bdid}\" alt=\"{bdid}\" />"
      else :
        bindata = ""
      buff += "<tr>"
      clink = f"<a href=\"showclips.cgi?creator={creator}\" target=\"_blank\">{creator}</a>"
      buff += WebPage.tag("td", clink)
      buff += WebPage.tag("td", str(count))
      buff += WebPage.tag("td", tags)
      buff += WebPage.tag("td", bindata)
      buff += "</tr>\n"
    self.setPlaceHolder('creators', buff)
    return

  # 作者一覧をアイコン表示する。
  def showIcons(self, creator="") :
    # 作者と登録数を得る。
    if creator == "" :
      sql = "SELECT creator, count(creator) AS count FROM Pixiv3 GROUP BY creator ORDER By count DESC"
    else :
      sql = f"SELECT creator, count(creator) AS count FROM Pixiv3 WHERE creator LIKE '{creator}' GROUP BY creator ORDER By creator"
    rows = self.__mysql.query(sql)
    if len(rows) == 0 :
      self.setPlaceHolder('message', '作品が登録されていません。')
      self.setPlaceHolder('creators', '')
      return
    buff = "<div>"
    for row in rows :
      creator = row[0]
      count = row[1]
      # もしあれば、作者の最新のイメージを得る。
      sql = "SELECT bindata FROM Pixiv3 WHERE creator='{0}' AND bindata > 0".format(creator)
      bdrows = self.__mysql.query(sql)
      n = len(bdrows) - 1
      if n >= 0 :
        bdid = bdrows[n][0]
        bindata = f"<img src=\"extract.cgi?id={bdid}\" alt=\"{bdid}\" />"
      else :
        bindata = f"<img src=\"/img/NoImage.jpg\" />"
      binlink = f"<a href=\"showclips.cgi?creator={creator}\" target=\"_blank\">{bindata}</a>"
      buff += f"<div style=\"display:inline-block;padding:6px;\"><div>{binlink}</div><div style=\"font-size:10pt;\">{creator} ({count})</div></div>"
    buff += "</div>\n"
    self.setPlaceHolder('creators', buff)
    return

# プログラム開始
wp = Pixiv4('templates/index.html')
wp.echo()
