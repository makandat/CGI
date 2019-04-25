#!/usr/bin/env python3
#  pathmemo.cgi
from WebPage import WebPage


class PathMemo(WebPage) :
  # コンストラクタ
  def __init__(self, template="") :
    super().__init__(template)
    return

wp = PathMemo('templates/pathmemo.html')
wp.echo()
