#!/usr/bin/env python3
# -*- code=utf-8 -*-
# MySQL Videos テーブル  ver1.70 2020-07-12  ビデオ表示機能追加
#    (注意)  /var/www/html/temp (c:Apache24/htdocs/temp) が必要。
from WebPage import WebPage
import Common, FileSystem as fs
from MySQL import MySQL

class ShowVideo(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    #Common.init_logger("/home/user/log/Videos.log")
    self.path = self.getParam('path')
    # gif かどうか
    if fs.getExtension(self.path) == '.gif' :
      self.setPlaceHolder('display0', 'none');
      self.setPlaceHolder('display1', 'block');
    else :
      self.setPlaceHolder('display0', 'block');
      self.setPlaceHolder('display1', 'none');
    self.setPlaceHolder('title', fs.getFileName(self.path))
    self.setPlaceHolder('message', self.path)
    self.copyFile(self.path)
    return

  # ビデオファイルを一時フォルダへ転送
  def copyFile(self, path) :
   dataFolder = "/var/www/html/temp"
   if Common.is_windows() :
     dataFolder ="C:/Apache24/htdocs/temp"
   fileName = "video" + fs.getExtension(path)
   videoPath = dataFolder + "/" + fileName
   fs.copy(path, videoPath)
   self.setPlaceHolder('path', "/temp/" + fileName)
   return


# 開始位置
wp = ShowVideo('templates/show_video.html')
wp.echo()
