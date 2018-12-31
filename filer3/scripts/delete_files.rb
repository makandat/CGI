#!/usr/bin/ruby
# coding: utf-8

# files.dbに対してDELETEクエリーを実行する。
#  このプログラムはコマンドとして実行する。
require "sf2lib"

if ARGV.size == 0 then
  abort 'Usage: delete_files criteria'
end

path = "/home/user/data/files.db"
begin
  db = SQLite3::Database.new(path)
  criteria = ARGV[0]
  delete_filedb(db, criteria)
  puts "deleted"
rescue => e
  puts e.message
end
