#!/usr/bin/env python3
#  CGI インタプリタ設定
from Py365Lib import Common, FileSystem as fs, Text

INTERPRETERS = '''1: /usr/bin/env python3
2: C:/Program Files/Python3/python.exe
3: C:/Program Files (x86)/Python37/python.exe
4: /usr/bin/env perl
5: C:/Perl64/bin/perl.exe
6: C:/Apps/Strawberry/perl/bin/perl.exe
7: /usr/bin/env ruby
8: C:/Program Files/Ruby27-x64/bin/ruby.exe
9: /usr/bin/env node
10: C:/Program Files/nodejs/node.exe
'''

# ファイルにインタプリタを適用する。
def apply(fileName, interpreter) :
    lines = fs.readLines(fileName)
    if lines[0].startswith('#!') :
        lines[0] = "#!" + interpreter + "\n"
        fs.writeLines(fileName, lines)
    else :
        print("Skiped: 行の先頭にインタプリタ指定が見当たりません。" + fileName)
    return

# 条件入力
fileName = ""
interpreterNo = 1
if Common.count_args() < 2 :
    fileName = Common.readline("対象のファイル・フォルダを指定してください。> ")
    print(INTERPRETERS)
    interpreterNo = int(Common.readline("番号を選択してください。> "))
else :
    fileName = Common.args(0)
    interpreterNo = int(Common.args(1))


interpreterLines = INTERPRETERS.split('\n')
interpreter = Text.substring(interpreterLines[interpreterNo - 1], 3)
print(interpreter + " が " + fileName + " に適用されます。")
a = Common.readline("実行しますか？ (y/n)")
if a != 'y' :
    Common.stop(9, "実行が取り消されました。")

# インタプリタ適用
if fs.isFile(fileName) :
    apply(fileName, interpreter)
else :
    files = fs.listFiles2(fileName)
    for f in files :
        print(f)
        ext = fs.getExtension(f)
        if ext == ".cgi" :
            apply(f, interpreter)
        else :
            print("Skipped")
        # end if
    # end for

print("正常終了。")
