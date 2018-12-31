# coding: utf-8
# =====================================================
#   ファイル管理 DB
# =====================================================
require 'sqlite3'

class FilesDb
  TableName = "info"

  # コンストラクタ
  def initialize(path)
    @db = SQLite3::Database.new(path)
  end

  # テーブルのレコード数
  def count()
    n = 0
    @db.execute('SELECT count(n) FROM ' + TableName) do |row|
      n = row[0]
      break
    end
    return n.to_i
  end

  # 最大のレコード番号（キー）
  def get_max()
    n = -1
    @db.execute('SELECT max(n) FROM ' + TableName) do |row|
      n = row[0]
      break
    end
    return n.to_i
  end

  # 最少のレコード番号（キー）
  def get_min()
    n = -1
    @db.execute('SELECT min(n) FROM ' + TableName) do |row|
      n = row[0]
      break
    end
    return n.to_i
  end

  # 結果を返すクエリをinfoテーブルに対して実行する。
  #   criteria  WHERE句
  #   columns: 最初の行に列名を入れる。
  #   戻り値  ２次元配列
  def query(criteria=nil, columns=false)
    rows = Array.new
    if criteria.nil? then
      sql = "SELECT n,path,info,method,icon,dir,bin,`group`,tstamp FROM " + TableName
    else
      sql = "SELECT n,path,info,method,icon,dir,bin,`group`,tstamp FROM " + TableName + " WHERE " + criteria
    end
    if columns then
      @db.execute2(sql) do |row|
        rows.push(row)
      end
    else
      @db.execute(sql) do |row|
        rows.push(row)
      end
    end
    return rows
  end

  # 同じパス名のレコードのうち新しいほうを返す。
  #   path: パス名
  def query_path(path)
    result = nil
    sql = "SELECT n,path,info,method,icon,dir,bin,`group`,tstamp FROM info WHERE path='" + path + "'"
    @db.execute(sql) do |row|
      if result.nil? then
        result = row
      elsif row[0] > result[0] then
        result = row
      end
    end
    return result
  end

  # データをinfoに挿入する。
  #   data: 値の配列 [path,info,method,icon,dir,bin,group]
  def insert(data)
    sql = "INSERT INTO " + TableName + " (path, info, method, icon, dir, bin, `group`, tstamp) VALUES(:path, :info, :method, :icon, :dir, :bin, :group, :tstamp)"
    tstamp = DateTime.now.to_s
    items = {:path=>data[0], :info=>data[1], :method=>data[2], :icon=>data[3], :dir=>data[4], :bin=>data[5], :group=>data[6], :tstamp=>tstamp}
    @db.execute(sql, items)
  end

  # データをinfoから削除する。
  #   criteria: WHERE 句
  def delete(criteria)
    sql = "DELETE FROM " + TableName + " WHERE " + criteria
    @db.execute(sql)
  end

  # キー n のデータを更新する。
  #   data: フィールド名:値の連想配列 [path,info,method,icon,dir,bin,group] (変更する項目のみ含む)
  #   criteria: WHERE 句
  def update(data, criteria)
    sql = "UPDATE " + TableName + " SET "
    data.each_pair do |key, value|
      next if key.to_s == "n"
      if value.class == String then
        name = key.to_s
        name = "`group`" if name == 'group'
        sql += format("%s='%s',", name, value.gsub("'", "''"))
      else
        sql += format("%s=%d,", key.to_s, value)
      end
    end
    sql.chop!
    sql += " WHERE "
    sql += criteria
    @db.execute(sql)
  end

  # クエリー結果をHTMLまたはテキストとして返す。
  def get_result(criteria=nil, html=false, columns=false)
    rows = query(criteria, columns)
    if rows.size == 0 then
      return ""
    end

    if html then
      str = %!<table style="margin-left:10px;margin-bottom:15px;">\n!
      str += "<tr><th>n</td><th>path</th><th>info</th><th>method</th><th>icon</th><th>dir</th><th>bin</th><th>group</th><th>time stamp</th></tr>\n"
    else
      str = ""
    end
    rows.each do |row|
      if html then
        str += "<tr>"
        row.each_with_index do |col, i|
          if col.class == String and i != 1 then
            col = col.size > 50 ? col[0..49] + " .. " : col
            if i == 3 then  # method
              col = col.gsub('&', '&amp;').gsub('<', '&lt;').gsub('>', '&gt;')
            end
          else
            col = col.to_s
          end
          str << "<td>" << col << "</td>"
        end
        str += "</tr>\n"
      else
        row.each_with_index do |col, i|
          if col.class == String and i != 1 then
            col = col.size > 30 ? col[0..29] + " .. " : col
          else
            col = col.to_s
          end
          str += col
          str += "\t"
        end
        str += "\n"
      end
    end
    str += "</table>\n" if html
    return str
  end


  # パスがsrcのレコードをdestにコピーする。destが未登録の場合は追加する。
  def copy(src, dest)
    r1 = @db.query_path(src)
    return if data.nil?
    r2 = @db.query_path(dest)
    if r2.nil? then
      data = [dest, '', r1[3], r1[4], r1[5], r1[6], r1[7]]
      self.insert(data)
    else
      hash = {:method=>r1[3], :icon=>r1[4], :dir=>r1[5], :bin=>r1[6], :group=>r1[7]}
      self.update(hash, "path='#{dest}'")
    end
  end
end  # FilesDb
