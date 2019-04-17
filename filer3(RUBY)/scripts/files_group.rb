require "sf2lib"

path = settings.sqlite3
#path = '/home/user/data/files.db'
sql = 'SELECT `group`, count(n) FROM info GROUP BY `group`'
query_files(path, sql, true)
