#!C:/python3/python.exe
#!/usr/bin/python3

from MySQL import MySQL
from WebPage import WebPage

class SendFile(WebPage) :
    def __init__(self, template="") :
        super().__init__(template)
        mysql = MySQL()
        id = self.getParam('id')
        path = mysql.getValue("SELECT `path` FROM Music WHERE id=" + id)
        WebPage.sendAudio(path)
        return

wp = SendFile()
