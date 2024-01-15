#!D:/python312/python.exe
import CGI365Lib as CGI

HTML = '''<!doctype html>
<html lang="ja">
<head>
 <meta charset="utf-8" />
 <meta name="viewport" content="width=device-width,initial-scale=1" />
 <title>Show Picture</title>
 <!-- BootstrapのCSS読み込み -->
 <link href="https://cdn.jsdelivr.net/npm/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
</head>

<body>
 <!-- ヘッダー -->
 <header class="container">
  <h1 class="header-1 text-center p-5 bg-light border rounded border-warning">Show Picture</h1>
  <p class="text-center"><a href="/cgi-bin/CGI365Lib/v1_7/index.cgi">HOME</a></p>
 </header>

 <!-- 本文 -->
 <article class="container">
  <div class="row mt-5">
    <h5 class="fs-5 text-primary">{{ path }}</h5>
    <figure classs="border"><img class="p-1" src="{{ get_image }}" /></figure>
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

# get_image.cgi
req, res = (CGI.Request(), CGI.Response())

GET_IMAGE = "/cgi-bin/CGI365Lib/v1_7/get_image.cgi"
path = req.getParam("path")
get_image = f"{GET_IMAGE}?path={path}"
res.sendString(HTML, embed={"path":path, "get_image":get_image})
