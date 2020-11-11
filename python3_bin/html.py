#!/usr/bin/python3

#  HTML ファイルのひな型を作成する。 v1.1
from Py365Lib import Common, FileSystem as fs

HTML_Simple = '''<!DOCTYPE html>
<html>
<head>
 <meta charset="utf-8" />
 <title>(*title*)</title>
 <link rel="stylesheet" href="/css/style.css" />
 <style></style>
 </head>

<body>
 <!-- ヘッダー -->
 <header>
  <h1>title</h1>
  <div class="menubar"><a href="/">HOME</a>&nbsp;/&nbsp;<a href="javascript:window.close()">閉じる</a></div>
 </header>
 
 <!-- 本文 -->
 <article>
   <section>

   </section>
 </article>

 <!-- フッター -->
 <footer>
  <p>&nbsp;</p>
  <p style="text-align:center;"><a href="#top">TOP</a></p>
  <p>&nbsp;</p>
  <p>&nbsp;</p>
 </footer>
</body>
</html>
'''

HTML_Highlight = '''<!DOCTYPE html>
<html>
<head>
 <meta charset="utf-8" />
 <title>(*title*)</title>
 <link rel="stylesheet" href="/css/style.css" />
 <script src="/js/jquery.min.js"></script>
 <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.0.0/styles/vs.min.css">
 <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.0.0/highlight.min.js"></script>
 <script>hljs.initHighlightingOnLoad();</script>
 <style></style>
 <script>
   $(() => {

   });
 </script>
</head>

<body>
 <!-- ヘッダー -->
 <header>
  <h1>(*title*)</h1>
  <div class="menubar"><a href="/">HOME</a>&nbsp;/&nbsp;<a href="javascript:window.close()">閉じる</a></div>
 </header>
 
 <!-- 本文 -->
 <article>
   <section>

   </section>
 </article>

 <!-- フッター -->
 <p>&nbsp;</p>
 <p style="text-align:center;"><a href="#top">TOP</a></p>
 <p>&nbsp;</p>
 <p>&nbsp;</p>
</body>
</html>
'''

HTML_Bootstrap4 = '''<!DOCTYPE html>
<html>
<head>
 <meta charset="utf-8" />
 <meta http-equiv="X-UA-Compatible" content="IE=edge">
 <meta name="viewport" content="width=device-width, initial-scale=1">
 <title>(*title*)</title>
 <link rel="stylesheet" href="/css/style2.css" />
 <!-- BootstrapのCSS読み込み -->
 <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
 <link rel="stylesheet" href="/css/style2.css">
 <style></style>
 <script>
   $(() => {

   });
 </script>
</head>

<body>
  <!-- ヘッダー -->
  <header class="container" style="padding:24px;">
   <h1 id="header">(*title*)</h1>
   <h5>Updated on (*date*)</h5>
   <hr />
  </header>

  <!-- Bootstrap コンテナ -->
  <div class="container">
    <div class="row">
      <div class="col-sm"></div>
      <div class="col-sm"></div>
    </div>
  </div>

  <!-- コンテナの終わり -->
  </div>

  <!-- フッター -->
  <footer>
   <p>&nbsp;</p>
   <p style="text-align:center;"><a href="#top">TOP</a></p>
   <p>&nbsp;</p>
   <p>&nbsp;</p>
  </footer>

  <!-- BootstrapのJS読み込み -->
  <script src="https://code.jquery.com/jquery-3.5.0.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
</body>
</html>
'''

HTML_Bootstrap4H = '''<!DOCTYPE html>
<html>
<head>
 <meta charset="utf-8" />
 <meta http-equiv="X-UA-Compatible" content="IE=edge">
 <meta name="viewport" content="width=device-width, initial-scale=1">
 <title>(*title*)</title>
 <link rel="stylesheet" href="/css/style2.css" />
 <!-- Bootstrapの CSS 読み込み -->
 <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
 <link rel="stylesheet" href="/css/style2.css">
 <!-- highlight.js -->
 <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.0.0/styles/vs.min.css">
 <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.0.0/highlight.min.js"></script>
 <script>hljs.initHighlightingOnLoad();</script>
 <style></style>
 <script>
   $(() => {

   });
 </script>
</head>

<body>
  <!-- ヘッダー -->
  <header class="container" style="padding:24px;">
   <h1 id="header">(*title*)</h1>
   <h5>Updated on (*date*)</h5>
   <hr />
  </header>

  <!-- Bootstrap コンテナ -->
  <div class="container">

    <!-- 行 -->
    <div class="row">
      <div class="col-sm"></div>
      <div class="col-sm"></div>
    </div>
  </div>

  <!-- コンテナの終わり -->
  </div>

  <!-- フッター -->
  <footer>
   <p>&nbsp;</p>
   <p style="text-align:center;"><a href="#top">TOP</a></p>
   <p>&nbsp;</p>
   <p>&nbsp;</p>
  </footer>

  <!-- BootstrapのJS読み込み -->
  <script src="https://code.jquery.com/jquery-3.5.0.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
</body>
</html>
'''


HTML_Vue = '''
<!DOCTYPE html>
<html>
<head>
 <meta charset="utf-8" />
 <title>(*title*)</title>
 <link rel="stylesheet" href="/css/style.css" />
 <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
 <script src="/js/jquery.min.js"></script>
 <style>
 </style>
</head>

<body>
 <h1>(*title*)</h1>
 <div class="menubar"><a href="/">ホーム</a> / <a href="javascript:window.close()">閉じる</a></div>
 <br />
 <div id="app" class="app">
  <div class="form_row"><label>PARAM<input type="text" v-model="value" /></label> </div>
  <div class="form_row"><input type="button" v-on:click="submit_click" value="送信" /></div>
  <div class="message" v-text="message"></div>
 </div>

 <script>
  const URL = "http://localhost/cgi-bin/API/testApi.cgi"
  var app = new Vue({
    el: "#app",
    data: {
        value: "",
        message: "" 
      },
    methods: {
      submit_click: () => {
        $.getJSON(URL, {"value":app.value}, (data) => {
          app.message = data;
        });
      }
    }
  });
</script>
<p>&nbsp;</p>
<p>&nbsp;</p>
</body>
</html>
'''

if Common.count_args() == 0 :
  filePath = Common.readline('HTMLファイルのパス名を入力してください。')
else :
  filePath = Common.args(0)

if Common.count_args() < 2 :
  print("1: HTML5 のシンプルなページ")
  print("2: HTML5 のシンプルなページ + jQuery + Highlight.js")
  print("3: Bootstrap4 のページ")
  print("4: Bootstrap4 のページ + Highlight.js ")
  print("5: Vue.js のページ")
  pagen = int(Common.readline("番号入力 > "))
else :
  pagen = int(Common.args(1))

if pagen < 1 or pagen > 4 :
  Common.stop(9, "番号が不正です。")

# "~" をホームディレクトリに変換する。
filePath = fs.tilder(filePath)
  
if fs.exists(filePath) :
  Common.stop(1, filePath + " はすでに存在します。")

with open(filePath, "w", encoding="utf-8") as f :
  if pagen == 1 :
    f.write(HTML_Simple)
  elif pagen == 2 :
    f.write(HTML_Highlight)
  elif pagen == 3 :
    f.write(HTML_Bootstrap4)
  elif pagen == 4 :
    f.write(HTML_Bootstrap4H)
  else :
    f.write(HTML_Vue)

print("HTML ファイルが作成されました。")

