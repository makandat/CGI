#!/usr/bin/python3
#  showText.cgi テキストを表示する。
from WebPage import WebPage
import FileSystem as fs
import Text

# テキスト表示 showText.cgi
class TextView(WebPage) :
  # コンストラクタ
  def __init__(self, template="") :
    super().__init__(template)
    if self.isParam('path') :
      self.path = self.getParam('path')
      filename = fs.getFileName(self.path)
      self.setPlaceHolder('title', filename)
      # 対応するファイルの拡張子リスト
      self.texts = self.conf['text'].split(':')
      self.showText(self.path)
    else :
      self.setPlaceHolder('message', "エラー：パスの指定がありません。")
      self.setPlaceHolder('content', "")
      self.setPlaceHolder('title', "Fatal Error")
    return

  # ファイル内容を表示する。
  def showText(self, path) :
    ext = fs.getExtension(path)
    ext = Text.substring(ext, 1)
    if ext in self.texts :
      try :
        text = WebPage.escape(fs.readAllText(path))
        self.setPlaceHolder('content', text)
        self.setPlaceHolder('message', path)
      except Exception as e :
        self.setPlaceHolder('message', path + "<br />を表示できません。コードが UTF-8 か確認してください。")
        self.setPlaceHolder('content', '')               
    else :
      self.setPlaceHolder('content', '')
      self.setPlaceHolder('message', 'エラー：この形式のファイルは表示できません。AppConf.ini に拡張子を登録してください。')     
    return

# スタート
wp = TextView('templates/showText.html')
wp.echo()

  
