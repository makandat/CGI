#!C:/Apps/Python3/python.exe
#  cookie.cgi
import for_cgi as cgi

HTML_BODY = '''
<h1>cookie.cgi</h1>
<br />
<p style="margin-left:35%"><a href="/cgi-bin/test/index.cgi">index.cgi へもどる</a> | <a href="javascript:location.reload()">Reload</a></p>
<p style="text-align:center;font-size:2em;color:indigo;">count = {0}</p>
'''

# クッキー一覧を取得。
cookies = cgi.get_cookies()

count = 0
# クッキーに 'count' というキーがある場合は、その値を取得して＋１する。
if 'count' in cookies.keys():
  count = int(cookies['count'])
  count += 1
# count を HTML_BODY に埋め込む。
html_body = HTML_BODY.format(count)

# HTML とクッキーを出力する。
cgi.send_html(cgi.HTML_HEAD.format('cookie.cgi') + html_body + cgi.HTML_TAIL, {'count':count})
