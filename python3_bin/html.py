#!/usr/bin/python3

#  HTML ファイルのひな型を作成する。
from Py365Lib import Common, FileSystem as fs

HTML = '''<!doctype html>
<html>
<head>
 <meta chaset="utf-8" />
 <title>title</title>
 <link rel="stylesheet" href="http://www7b.biglobe.ne.jp/~makandat/css/default.css" />
 <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
 <script src="https://cdn.jsdelivr.net/npm/vue"></script>
 <script src="https://cdn.jsdelivr.net/npm/chart.js@2.8.0"></script>
 <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.5/styles/vs.min.css">
 <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.5/highlight.min.js"></script>
 <script>hljs.initHighlightingOnLoad();</script>
 <style></style>
 <script></script>
</head>

<body>
 <h1>title</h1>
 <div class="menubar"><a href="/">HOME</a></div>
 <div class="section">

 </div>
 <p>&nbsp;</p>
 <p style="text-align:center;"><a href="#top">TOP</a></p>
 <p>&nbsp;</p>
 <p>&nbsp;</p>
</body>
</html>
'''

if Common.count_args() == 0 :
  filePath = Common.readline('HTMLファイルのパス名を入力してください。')
else :
  filePath = Common.args(0)


# "~" をホームディレクトリに変換する。
filePath = fs.tilder(filePath)
  
if fs.exists(filePath) :
  Common.stop(1, filePath + " はすでに存在します。")

with open(filePath, "w", encoding="utf-8") as f :
  f.write(HTML)

print("Done.")

