#!/usr/bin/env python3
#  fetchText.cgi
import CGI365Lib as CGI

request = CGI.Request()
response = CGI.Response()
if request.Method == "GET":
  amount = int(request.getParam("amount"))
  price = int(request.getParam("price"))
  product = request.getParam("product")
  payment = amount * price
  message = "GET " + product + " = " + str(payment)
elif request.Method == "POST":
  request.parseFormBody()
  amount = int(request.getParam("amount"))
  price = int(request.getParam("price"))
  product = request.getParam("product")
  payment = amount * price
  message = "POST " + product + " = " + str(payment)
else:
  message = "Bad REQUEST_METHOD"
response.sendSimple(message, "utf-8")
