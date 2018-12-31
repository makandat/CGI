#!/usr/bin/ruby
# coding: utf-8

# ファイル管理データのコピー
#  このプログラムはコマンドとして実行する。

require "sf2lib"

if ARGV.size == 0 then
  abort "Usage: copy_rec src_PK dest_PK"
end

path = "/home/user/data/files.db"
begin
  pksrc = Integer(ARGV[0])
  pkdest = Integer(ARGV[1])
  db = SQLite3::Database.new(path)
  copy_filedb_pk(db, pksrc, pkdest)
  db.close
  puts "Done."
rescue => e
  puts e.message
end
