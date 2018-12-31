#!/usr/bin/ruby
# coding: utf-8

# ディレクトリをスキャンしてレコードをファイル管理データに追加。
#  このプログラムはコマンドとして実行する。
require "sf2lib"

def addNew(db, path)
  r = query_path(db, path)
  if r.nil? then
    data = [path, '', '', '', 0, 0, '']
    insert_filedb(db, data)
  end
end

if ARGV.size == 0 then
  abort 'Usage: scan_add wildcard'
end

path = "/home/user/data/files.db"
begin
  db = SQLite3::Database.new(path)
  wc = ARGV[0]
  Dir.glob(wc) do |path|
    addNew(db, path)
  end
  db.close
  puts "Done."
rescue => e
  puts e.message
end
