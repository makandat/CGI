#!C:/Apps/Python3/python.exe
# get_form.cgi
import for_cgi as cgi, os

HTML_BODY = '''<h1>get_form.cgi</h1>
<hr>
<p style="padding:10px;"><a href="/cgi-bin/for_cgi/index.cgi">index.cgi へもどる</a></p>
<form styl="margin-left:10%; margin-top:20px;" method="GET">
 <fieldset style="margin-top:20px; padding:8px;">
  <legend>名前と年齢を入力</legend>
  <div style="margin-top:10px">
    <label>名前 <input type="text" name="name" id="name" value="{0}" /></label>
  </div>
  <div style="margin-top:10px; margin-bottom:20px;">
    <label>年齢 <input type="number" name="age" id="age" value="{1}" /></label>
  </div>
 </fieldset>
 <div style="margin-top:20px;"><button type="submit">送信する</button></div>
</form>
<p id="message" class="message">{2}</p>
'''

# QUERY_STRING があるか？
if cgi.qs_exists():
  # パラメータを取得してメッセージを埋め込む。
  params = cgi.get_params()
  cgi.info(params)
  name = params['name']
  age = params['age']
  message = f'{name}さんは{age}歳です。'
  body = HTML_BODY.format(name, age, message) 
else:
  # フォームのみを表示。
  body = HTML_BODY.format('', '', '')
# レスポンスを返す。
cgi.send_html(cgi.HTML_HEAD.format('get_form') + body + cgi.HTML_TAIL)
