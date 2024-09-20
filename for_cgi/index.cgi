#!C:/Apps/Python3/python.exe
#  index.cgi
import for_cgi as cgi

HTML_BODY = '''
<article style="margin-top:20px;margin-left:8%; margin-right:8%;">
<h1>for_cgi.py テストメニュー</h1>
 <ul style="margin:30%;margin-top:20px;">
   <li><a href="/cgi-bin/for_cgi/hello.cgi">hello</a></li>
   <li><a href="/cgi-bin/for_cgi/text_plain.cgi">text_plain.cgi</a></li>
   <li><a href="/cgi-bin/for_cgi/text_html.cgi">text_html.cgi</a></li>
   <li><a href="/cgi-bin/for_cgi/bad_request.cgi">Bad Request</a></li>
   <li><a href="/cgi-bin/for_cgi/server_error.cgi">Internal Server Error</a></li>
   <li><a href="/cgi-bin/for_cgi/jpeg_file.cgi?path=D:/HD-LLU3/Pictures/Pixiv/DOE/117247555_p00.jpg">jpeg file</a></li>
   <li><a href="/cgi-bin/for_cgi/get_form.cgi">get_form.cgi</a></li>
   <li><a href="/cgi-bin/for_cgi/post_form.cgi">post_form.cgi</a></li>
   <li><a href="/cgi-bin/for_cgi/fetch_json.cgi">fetch_json.cgi</a></li>
 </ul>
</article>
'''

cgi.content_type()
print(cgi.HTML_HEAD.format('index') + HTML_BODY + cgi.HTML_TAIL)
