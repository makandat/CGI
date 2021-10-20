#!C:\python3\python.exe
# -*- code=utf-8 -*-
#  like.cgi
import WebPage as page
import MySQL
import Common


class MainPage(page.WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    # Common.init_logger("C:/temp/PyLogger.log")
    # fav を取得する。
    self.__mysql = MySQL.MySQL()
    id = self.getParam('id')
    fav = self.__mysql.getValue(f"SELECT fav FROM Pictures WHERE id={id}")
    fav = int(fav) + 1
    self.__mysql.execute(f"UPDATE Pictures SET fav={fav} WHERE id={id}")
    self.setPlaceHolder("message", f"お気に入り度数が {fav} になりました。index.cgi をリロードしてください。")
    return


# メイン開始位置
wp = MainPage('templates/like.html')
wp.echo()
