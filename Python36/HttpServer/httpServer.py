import http.server

server_address = ("", 5411)
handler_class = http.server.SimpleHTTPRequestHandler #ハンドラを設定
simple_server = http.server.HTTPServer(server_address, handler_class)
simple_server.serve_forever()
