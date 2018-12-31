#!/usr/bin/ruby
# coding: utf-8

# files.dbに対してSELECTクエリーを実行する。
#  このプログラムはコマンドとして実行する。
require "sqlite3"

if ARGV.size == 0 then
  abort 'Usage: select_files sql'
end

path = "/home/user/data/files.db"
begin
  db = SQLite3::Database.new(path)
  sql = ARGV[0]
  db.execute(sql) do |row|
    puts row.join(', ')
  end
  db.close
  puts sql
rescue => e
  puts e.message
end
