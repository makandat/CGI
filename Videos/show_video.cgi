#!C:\python3\python.exe
#!/usr/bin/env python3
# -*- code=utf-8 -*-
# MySQL Videos テーブル  ver1.70 2020-07-12  ビデオ表示機能追加
#                        ver1.90 ファイルチェック機能追加
#                        ver1.91 d:/temp にビデオファイルを置くように変更
#                        ver2.01 参照カウントを行わなかったバグを修正
#    (注意)  /var/www/html/temp (d:/temp と alias /temp d:/temp) が必要。
from WebPage import WebPage
import Common, FileSystem as fs
from MySQL import MySQL

class ShowVideo(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    #Common.init_logger("/home/user/log/Videos.log")
    self.__mysql = MySQL()
    self.path = self.getParam('path')
    # mp4 かどうか
    if fs.getExtension(self.path) == '.mp4' :
      if fs.exists(self.path) :
        self.setPlaceHolder('display0', 'block');
        self.setPlaceHolder('message', self.path)
        # self.copyFile(self.path)
        WebPage.sendMP4(self.path)
        self.countUp(self.path)
      else :
        self.setPlaceHolder('display0', 'none');
        self.setPlaceHolder('message', '<b>動画のパスが不正です。</b><br />' + self.path)
    else :
      self.setPlaceHolder('display0', 'none');
      self.setPlaceHolder('message', '<b>.mp4 形式以外の動画は表示できません。</b><br />' + self.path)
    self.setPlaceHolder('title', fs.getFileName(self.path))
    return

  # ビデオファイルを一時フォルダへ転送
  def copyFile(self, path) :
   if Common.is_windows() :
     videoPath = "d:/temp/video.mp4"
   else :
     videoPath = "/var/www/html/temp/video.mp4"
   fs.copy(path, videoPath)
   self.setPlaceHolder('path', "/temp/video.mp4")
   return

  # 参照カウントアップ
  def countUp(self, path) :
    id = self.__mysql.getValue(f"SELECT id FROM Videos WHERE path='{path}'")
    self.__mysql.execute(f"CALL IncreaseVideoCount({id})")
    return


# 開始位置
wp = ShowVideo('templates/show_video.html')
wp.echo()
