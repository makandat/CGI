#!/usr/bin/env python3
# requestPostForm.cgi
import CGI365Lib as CGI

request = CGI.Request()
response = CGI.Response()

HTML = '''<!doctype html>
<html>
<head>
 <meta charset="utf-8">
 <title>requestPostForm.cgi</title>
 <link href="https://cdn.jsdelivr.net/npm/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
 <style>
   form {
     margin: 6px;
     padding: 4px;
     border: solid thin silver;
     border-radius: 6px;
     background-color: whitesmoke;
   }
   .result {
     color:fuchsia;
     padding:4px;
     font-size;12pt;
   }
   .form-row {
     margin-left:2%;
     margin-top: 5px;
   }
   .message {
     font-size; 10pt;
     color:fuchsia;
     margin-top, margin-bottom:10px;
     margin-left:2%;
    }
 </style>
 <script>
  function clearAll() {
    const inputs = document.getElementsByTagName("input");
    inputs[0].value = "";
    inputs[1].value = "";
    location.href = "/cgi-bin/CGI365Lib/Proj/requestPostForm.cgi";
  }
 </script>
</head>

<body class="container">
 <section class="row">
  <h1 class="h1 text-primary text-center p-3">requestPostForm.cgi</h1>
  <p class="text-center p-3">フォームを submit POST し、結果を表示する。</p>
  <form method="POST" action="/cgi-bin/CGI365Lib/Proj/requestPostForm.cgi">
    <div class="form-row">
      <label class="form-label">A
       <input type="text" name="A" value="{{ A }}" class="form-control">
      </label>
    </div>
    <div class="form-row">
      <label class="form-label">B
       <input type="text" name="B" value="{{ B }}" class="form-control">
      </label>
    </div>
    <div class="form-row mb-4">
      <button type="submit" class="btn btn-primary">送信する</button>
      <button type="button" class="btn btn-primary" onclick="javascript:clearAll()">クリア</button>
    </div>
    <p id="message" class="message">{{ message }}</p>
  </form>
 </section>
 <script src="https://cdn.jsdelivr.net/npm/bootstrap/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>'''

if request.Method == "GET":
  response.sendString(HTML, mime="text/html; charset=\"utf-8\"", cookie=False, headers=False, embed={"A":"", "B":"", "message":""})
elif request.Method == "POST":
  request.parseFormBody()
  a = request.getParam("A")
  b = request.getParam("B")
  response.sendString(HTML, mime="text/html; charset=\"utf-8\"", cookie=False, headers=False, embed={"A":a, "B":b, "message":"POST OK"})
else:
  response.status("403 Forbidden")
