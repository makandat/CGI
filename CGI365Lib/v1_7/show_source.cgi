#!D:/python312/python.exe
import CGI365Lib as CGI
import os, html

HTML = '''<!doctype html>
<html lang="ja">
<head>
 <meta charset="utf-8" />
 <meta name="viewport" content="width=device-width,initial-scale=1" />
 <title>Show Source</title>
 <!-- BootstrapのCSS読み込み -->
 <link href="https://cdn.jsdelivr.net/npm/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
 <!-- highlight.js -->
 <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/vs.min.css">
 <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
 <script>hljs.initHighlightingOnLoad();</script>
</head>

<body>
 <!-- ヘッダー -->
 <header class="container">
  <h1 class="header-1 text-center p-5 bg-light border rounded border-warning">Show Source</h1>
  <p class="text-center"><a href="/cgi-bin/CGI365Lib/v1_7/index.cgi">HOME</a></p>
 </header>

 <!-- 本文 -->
 <article class="container">
  <div class="row mt-5">
    <h5 class="fs-5 mb-3 text-primary">{{ path }}</h5>
    <pre class="border rounded p-1" style="font-size:small;"><code>{{ code }}</code></pre>
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

# show_source.html
req, res = (CGI.Request(), CGI.Response())

path = req.getParam("path")
if not os.path.isfile(path):
  res.status(403, CGI.FORBIDDEN)
else:
  code = ""
  with open(path, encoding="utf-8") as f:
    s = f.read()
    code = html.escape(s)
  res.sendString(HTML, embed={"path":path, "code":code})
