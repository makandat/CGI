#!D:/python312/python.exe
import CGI365Lib as CGI
import os

HTML = '''<!doctype html>
<html lang="ja">
<head>
 <meta charset="utf-8" />
 <meta name="viewport" content="width=device-width,initial-scale=1" />
 <title>Show Thumbnailes</title>
 <!-- BootstrapのCSS読み込み -->
 <link href="https://cdn.jsdelivr.net/npm/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
</head>

<body>
 <!-- ヘッダー -->
 <header class="container">
  <h1 class="header-1 text-center p-5 bg-light border rounded border-warning">Show Thumbnailes</h1>
  <p class="text-center"><a href="/cgi-bin/CGI365Lib/v1_7/index.cgi">HOME</a></p>
 </header>

 <!-- 本文 -->
 <article class="container">
  <div class="row mt-5 justify-content-start">
    {{ content }}
  </div>
 </article>
 <!-- フッター -->
 <footer class="container">
  <p class="text-center mt-4"><a href="#top">TOP</a></p>
  <p>&nbsp;</p>
 </footer>
 <!-- BootstrapのJS読み込み -->
 <script src="https://cdn.jsdelivr.net/npm/bootstrap/dist/js/bootstrap.bundle.min.js"></script>
<body>
</html>
'''

# 指定したディレクトリ内の JPEG / PNG 画像一覧を文字列として返す。
def getContents(dirpath):
  SHOW_PICTURE = "/cgi-bin/CGI365Lib/v1_7/show_picture.cgi"
  GET_IMAGE = "/cgi-bin/CGI365Lib/v1_7/get_image.cgi"
  s = ""
  for item in os.scandir(dirpath):
    parts = os.path.splitext(item.path)
    ext = ""
    if len(parts) == 2:
      ext = parts[1].lower()
    if item.is_file() and (ext == ".jpg" or ext == ".png"):
      s += f"<figure class=\"col\"><a href=\"{SHOW_PICTURE}?path={item.path}\" target=\"_blank\"><img src=\"{GET_IMAGE}?path={item.path}\" style=\"padding:2px;\" width=\"240px\" /></a></figure>\n"
  return s

# Start
req, res = (CGI.Request(), CGI.Response())

dirpath = req.getParam("path")
if dirpath == "":
  res.sendString(HTML, embed={"content":""})
else:
  res.sendString(HTML, embed={"content":getContents(dirpath)})
 
  

