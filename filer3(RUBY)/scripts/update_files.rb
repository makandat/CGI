#!/usr/bin/ruby
# coding: utf-8

# files.dbに対してDELETEクエリーを実行する。
#  このプログラムはコマンドとして実行する。
require "sf2lib"
require "json/pure"

if ARGV.size == 0 then
  abort 'Usage: update_files json criteria'
end

path = "/home/user/data/files.db"
begin
  criteria = ARGV[1]
  data = JSON.parse(ARGV[0])
  db = SQLite3::Database.new(path)
  update_filedb(db, data, criteria)
  puts "updated"
rescue => e
  puts e.message
end
