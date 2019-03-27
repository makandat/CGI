#!/usr/bin/env python3
#  画像を返す。
import WebPage as page

class Page(page.WebPage) :
  # コンストラクタ
  def __init__(self) :
    super().__init__(self)
    if 'path' in self.params :
      path = self.params['path'].value.encode('utf8')
      Page.sendImage(path)
    else :
      Page.sendImage('/var/www/html/img/error.png')

Page()
