#!C:/Apps/Python3/python.exe
# server_error.cgi
import for_cgi as cgi

cgi.send_status(cgi.Status.INTERNAL_SERVER_ERROR, "Fatal error occured.")
