#!/usr/bin/python3
#!C:\Program Files (x86)\Python37\python.exe
# -*- coding: utf-8 -*-
# slideview.cgi フォルダ内画像のスライド表示
#   MySQL を利用
from WebPage import WebPage
import FileSystem as fs
from MySQL import MySQL
import Text
import Common
import sys, os
#from syslog import syslog

## ページクラス
class MainPage(WebPage) :

  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL()
    self.adjust = '0'
    self.current_image = 0
    if self.isCookie('current_image') :
      self.current_image = int(self.getCookie('current_image'))
    if self.isParam('album') :
      # Postback のとき
      album = self.getParam('album')
      slide = self.getParam('slide')
      if Text.re_contain('^\\d+$', slide) :
        self.setCookie('current_image', int(slide) - 1)
        self.current_image = int(slide) - 1
      if self.isParam('width') :
        # 画像幅調整あり
        if self.isCookie('adjust_width') :
          self.adjust = self.getCookie('adjust_width')
          if self.adjust == '1' :
            # 反転させる。
            self.adjust = '0'
          else :
            self.adjust = '1'
        else :
          self.adjust = '0'
        self.setCookie('adjust_width', self.adjust)
      else :
        # 画像調整指定なし(width=なし)
        self.adjust = self.getCookie('adjust_width')
      self.showPicture(album, slide)
      albumName = self.getAlbumName(album)
      self.setPlaceHolder('title', albumName)
      self.setPlaceHolder('slide', "slide #" + slide)
    else :
      # Postback でない
      self.setPlaceHolder('album', '')
      self.setPlaceHolder('message', '')
      self.setPlaceHolder('title', 'スライド表示')
      self.setPlaceHolder('slide', '')
      self.setCookie('adjust_width', '0')
    return


  # アルバム番号から名称を得る。
  def getAlbumName(self, id) :
    sql = f"SELECT name FROM Album WHERE id={id}"
    name = self.__mysql.getValue(sql)
    return name


  # 画像を表示する。
  def showPicture(self, album, slide) :
    # アルバム内の画像一覧を取得
    sql = f"SELECT id, title, path FROM PictureAlbum WHERE album = {album} ORDER BY id"
    rows = self.__mysql.query(sql)
    m = len(rows)
    current = self.current_image
    if slide == "first" :
      # 最初
      current = 0
      self.setPlaceHolder('message', "最初の画像です。No.1")
    elif slide == "prev" :
      # 前
      current = (current - 1) if current > 0 else 0
      current1 = current + 1
      if current == 0 :
        self.setPlaceHolder('message', '最初の画像です。No.1')
      else :
        self.setPlaceHolder('message', f"No.{current1} / {m}の画像です。")
    elif slide == "next" :
      # 次
      current = (current + 1) if current < (m - 1) else (m - 1)
      current1 = current + 1
      if current == m - 1 :
        self.setPlaceHolder('message', f"最後の画像です。No.{current1}")
      else :
        self.setPlaceHolder('message', f"No.{current1} / {m} の画像です。")
    elif slide == "last" :
      # 最後
      current = m - 1
      current1 = current + 1
      self.setPlaceHolder('message', f"最後の画像です。No.{current1}")
    elif slide == 'current' :
      # 移動しない
      current1 = current + 1
      self.setPlaceHolder('message', f"No.{current1} / {m}の画像です。")
    else :
      # CURRENT
      current = int(slide) - 1
      self.setPlaceHolder('message', f"No.{slide} / {m} の画像です。")
    row = rows[current]
    path = row[2]
    self.setCookie('current_image', str(current))
    if self.adjust == '1' :
      self.setPlaceHolder('picture', f"<img src=\"getImage.cgi?path={path}\" style=\"padding:10px;\" />")
    else :
      self.setPlaceHolder('picture', f"<img src=\"getImage.cgi?path={path}\" style=\"padding:10px;width:100%;\" />")
    self.setPlaceHolder('path', path)
    self.setPlaceHolder('album', album)
    self.setCookie('current_image', current)
    return

  # 画像ファイルなら True を返す。
  @staticmethod
  def isPicture(path) :
    ext = Text.tolower(fs.getExtension(path))
    return (ext == '.jpg' or ext == '.png' or ext == '.gif')



# メイン開始位置
wp = MainPage('templates/slideview.html')
wp.echo()
