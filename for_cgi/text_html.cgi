#!C:/Apps/Python3/python.exe
#  text_html.cgi
import for_cgi as cgi

HTML = '''<!DOCTYPE html>
<html>
 <head>
  <!-- <meta charset="utf-8"> -->
  <title>text_html.cgi</title>
  <link rel="stylesheet" href="/css/style.css">
 </head>
 <body>
  <h1>HTML 出力のテスト</h1>
 </body>
</html>
'''
cgi.send_html(HTML)
