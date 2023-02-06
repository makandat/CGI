#!/usr/bin/python3

#  HTML ファイルのひな型を作成する。 v1.2
from Py365Lib import Common, FileSystem as fs

HTML_Simple = '''<!DOCTYPE html>
<html lang="ja">
<head>
 <meta charset="utf-8" />
 <meta name="viewport" content="width=device-width,initial-scale=1" />
 <title>HTML_Simple</title>
 <link rel="stylesheet" href="/css/style.css" />
 <style>
   h1 {
     text-align: center;
     color: crimson;
     padding: 10px;
   }
   a:link, a:visited {
     text-decoration: none;
     color: firebrick;
   }
 </style>
</head>

<body>
 <!-- ヘッダー -->
 <header>
  <h1>HTML_Simple</h1>
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

HTML_Bootstrap5 = '''<!DOCTYPE html>
<html lang="ja">
<head>
 <meta charset="utf-8" />
 <meta name="viewport" content="width=device-width,initial-scale=1" />
 <title>HTML_Bootstrap5</title>
 <!-- BootstrapのCSS読み込み -->
 <link href="https://cdn.jsdelivr.net/npm/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
 <style>
 </style>
</head>

<body>
 <!-- ヘッダー -->
 <header class="container">
  <h1 class="header-1 text-primary text-center p-5">HTML_Bootstrap5</h1>
 </header>

 <!-- 本文 -->
 <article class="container">
   <section class="row">
    <div class="col p-2">
      <p class="text-success fs-3">row1 col1</div>
    </div>
    <div class="col p-2">
      <p class="text-warning fs-3 fw-bold">row1 col2</div>
    </div>
   </section>
 </article>
 
 <!-- フッター -->
 <footer class="container">
  <p class="text-center mt-4"><a href="#top">TOP</a></p>
  <p>&nbsp;</p>
 </footer>
 <!-- BootstrapのJS読み込み -->
 <script src="https://cdn.jsdelivr.net/npm/bootstrap/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

HTML_Vue3 = '''<!DOCTYPE html>
<html lang="ja">
<head>
 <meta charset="utf-8" />
 <meta name="viewport" content="width=device-width,initial-scale=1" />
 <title>HTML_Vue3</title>
 <!-- BootstrapのCSS読み込み -->
 <link href="https://cdn.jsdelivr.net/npm/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
 <!-- Vue.js の読み込み -->
 <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
 <style>
 </style>
</head>

<body>
  <!-- ヘッダー -->
  <header class="container">
   <h1 class="header-1 text-primary p-5 text-center">HTML_Vue3</h1>
  </header>

  <div id="App" class="container">
    <div class="row p-5">
     <div class="col">
       <button type="button" @click="countUp" class="btn btn-primary">Count Up</button>
     </div>
    </div>
    <div class="row p-5 display-6 text-danger">
     <div class="col">
       count = {{ count }}
     </div>
    </div>
  </div>
  
  <!-- フッター -->
  <footer class="container">
   <p class="text-center mt-4"><a href="#top">TOP</a></p>
   <p>&nbsp;</p>
  </footer>
  <!-- BootstrapのJS読み込み -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap/dist/js/bootstrap.bundle.min.js"></script>
  <!-- Vue3 App -->
   <script>
    const { createApp } = Vue
    createApp({
      data() {
        return { count: 0 }
      },
      methods: {
        countUp() {
          this.count++;
        }
      }
    }).mount('#App');
  </script>
</body>
</html>
'''

if Common.count_args() == 0 :
  filePath = Common.readline('HTMLファイルのパス名を入力してください。')
else :
  filePath = Common.args(0)

if Common.count_args() < 2 :
  print("1: HTML5 のシンプルなページ")
  print("2: Bootstrap5 のページ")
  print("3: Vue3 + Bootstrap5 のページ")
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
    f.write(HTML_Bootstrap5)
  elif pagen == 3 :
    f.write(HTML_Vue3)
  else :
    Common.stop(2, "番号が間違っています。")

print("HTML ファイルが作成されました。必要なら下記の文を追加して下さい。")
print(''' jQuery の追加：
      https://code.jquery.com/jquery-3.6.3.slim.min.js
      <script>
        $(() => { });
      </script>''')
print(''' Highlight.js の追加：
       https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/vs.min.css
       https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js
       hljs.initHighlightingOnLoad();''')

