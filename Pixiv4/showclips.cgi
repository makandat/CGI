#!/usr/bin/env python3
#  Pixiv Clip by Python3 v4.0  2019-04-17
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
    if self.isParam('creator') :
      creator = self.getParam('creator')
      self.setPlaceHolder('title', creator + 'さん作品')
      self.showClips(creator)
    else :
      self.setPlaceHolder('message', 'エラー：作者の指定がありません。')
      self.setPlaceHolder('title', '作品の表示')
      self.setPlaceHolder('clips', '')
    return

  # 作品一覧を表示
  def showClips(self, creator) :
    creator = creator.replace("'", "''")
    sql = f"SELECT id,title,creator,illust_id,original,tags,bindata FROM Pixiv3 WHERE creator='{creator}'"
    rows = self.__mysql.query(sql)
    if len(rows) == 0 :
      self.setPlaceHolder('message', creator + " の作品が登録されていません。")
      self.setPlaceHolder('clips', '')
    else :
      buff = ""
      for row in rows :
        id = row[0]
        title = row[1]
        illust_id = row[3]
        original = Pixiv4.NoneToSpace(row[4])
        tags = Pixiv4.NoneToSpace(row[5])
        bindata = Pixiv4.NoneToSpace(row[6])
        buff += "<tr>"
        buff += WebPage.tag("td", id)
        tlink = f"<a href=\"https://www.pixiv.net/member_illust.php?mode=medium&illust_id={illust_id}\" target=\"_blank\">{title}</a>"
        buff += WebPage.tag("td", tlink)
        buff += WebPage.tag("td", creator)
        buff += WebPage.tag("td", illust_id)
        buff += WebPage.tag("td", original)
        buff += WebPage.tag("td", tags)
        blink = f"<img src=\"extract.cgi?id={bindata}\" alt=\"{bindata}\" />" if not (bindata == 0 or bindata == "") else ""
        buff += WebPage.tag("td", blink)
        buff += "</tr>\n"
      self.setPlaceHolder('clips', buff)
    return

  # None を空文字に変換する。
  @staticmethod
  def NoneToSpace(s) :
    if s == None :
      return ""
    else :
      return str(s)


# ページを表示する。
wp = Pixiv4('templates/showclips.html')
wp.echo()
