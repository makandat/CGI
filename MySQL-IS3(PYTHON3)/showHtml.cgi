#!/usr/bin/python3
# -*- code=utf-8 -*-
#   MySQL-IS showHtml.cgi  Version 2.00
import WebPage as web
import FileSystem as fs

# CGI WebPage クラス
class MainPage(web.WebPage) :

  # コンストラクタ
  def __init__(self, template="") :
    super().__init__(template)
    htmlfile = self.getParam('html')
    self.html = fs.readAllText(htmlfile)
    if self.isParam('anchor') :
      anchor = self.getParam('anchor')
      javascript = "<script src=\"/js/jquery.min.js\"></script>\n"
      javascript += "<script>\n"
      javascript += "$(function() {\n"
      javascript += f"  document.location.href = \"#{anchor}\";\n"
      javascript += "});\n"
      javascript += "</script>\n";
    else :
      javascript = ""
    self.setPlaceHolder('javascript', javascript)
    return

# メイン開始位置
wp = MainPage()
wp.echo()
