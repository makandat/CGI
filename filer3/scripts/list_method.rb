require "sf2lib"

path = settings.sqlite3
#path = '/home/user/data/files.db'
sql = %!SELECT n,path,info FROM info WHERE method <> ''!
query_files(path, sql, true)
