#!/usr/bin/env python3
#  postJSON.cgi
import CGI365Lib as CGI

request = CGI.Request()
response = CGI.Response()
CGI.info("postJSON.cgi " + request.Method)
if request.Method == "POST":
  data = request.parseJSON()
  product = data['product']
  amount = int(data['amount'])
  price = int(data['price'])
  payment = amount * price
  result  = {"product":product, "payment":payment}
  response.sendJSON(result, "utf-8")
else:
  response.sendJSON("Bad REQUEST_METHOD")
