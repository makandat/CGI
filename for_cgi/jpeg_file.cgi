#!C:/Apps/Python3/python.exe
# jpeg_file.cgi
import for_cgi as cgi, os, sys

# パラメータがあるか？
if cgi.qs_exists():
  params = cgi.get_params()
  path = params['path']
  # 画像として転送する。
  cgi.send_image(path)
else:
  cgi.send_status(cgi.Status.BAD_REQUEST)
