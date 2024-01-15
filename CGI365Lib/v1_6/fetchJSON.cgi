#!/usr/bin/env python3
#  fetchJSON.cgi
import CGI365Lib as CGI

#CGI.LOG = "D:/temp/fetchJSON.log"
request = CGI.Request()
response = CGI.Response()
if request.Method == "GET":
  amount = int(request.getParam("amount"))
  price = int(request.getParam("price"))
  product = request.getParam("product")
  payment = amount * price
  data = {"Method":"GET", "product":product, "payment":payment}
elif request.Method == "POST":
  request.parseFormBody()
  amount = int(request.getParam("amount"))
  price = int(request.getParam("price"))
  product = request.getParam("product")
  payment = amount * price
  data = {"Method":"GET", "product":product, "payment":payment}
else:
  data = "Bad REQUEST_METHOD"
response.sendJSON(data, "utf-8")
