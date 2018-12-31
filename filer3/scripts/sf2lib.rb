# coding: utf-8
require "image_size"
require "sqlite3"
require "mylogger"


# 画像のプロパティと画像の縮小表示
def image_view(path)
  html = ""
  thumb_size = 240
  begin
    File.open(path) do |f|
      img = ImageSize.new(f)
      w = img.width
      h = img.height
      if w > thumb_size or h > thumb_size then
        if w >= h then
          hw = Float(h) / Float(w)
          w = thumb_size
          h = Integer(Float(w) * hw)
        else
          wh = Float(w) / Float(h)
          h = thumb_size
          w = Integer(Float(h) * wh)
        end
        html = %!<img src="/Image/#{path}" width="#{w}px" height="#{h}px" alt="img" /><br />\n!
      else
        html = %!<img src="/Image/#{path}" alt="img" /><br />\n!
      end
      html += "#{path}<br />\n"
      #html += "type=" + img.type
      html += " width=" + w.to_s
      html += " height=" + h.to_s
      html += "<br />\n"
   end
  rescue => e
    return %!<p style="color:red;">fatal error. #{e.message}</p>!
  end
  return html
end


# ディレクトリ内の画像ファイルを検索し、縮小表示する。
def show_thumbs(dir)
  htm = <<EOS
<script>
function show_image_normal(path, i) {
  $('#image_normal').css('left', '240px');
  $('#image_normal').html('<img src="/image/' + base64.encode(path) + '" alt="" />');
}
</script>

<div id="image_normal" style="position:absolute;"></div>
EOS
  thumb_size = 48
  i = 1
  Dir.foreach(dir) do |file|
    next unless file.match(/.+\.jpg$|.+\.png$|.+\.gif$/)
    path = dir + "/" + file
    File.open(path) do |f|
      img = ImageSize.new(f)
      w = img.width
      h = img.height
      if w > thumb_size or h > thumb_size then
        if w >= h then
          hw = Float(h) / Float(w)
          w = thumb_size
          h = Integer(Float(w) * hw)
        else
          wh = Float(w) / Float(h)
          h = thumb_size
          w = Integer(Float(h) * wh)
        end
        htm += %!<a href="javascript:show_image_normal('#{path}', #{i});"><img id="thumb#{i}" src="/Image/#{path}" width="#{w}px" height="#{h}px" alt="img" /></a><br />#{file}<br />\n!
      else
        htm += %!<img src="/Image/#{path}" alt="img" /><br />#{file}<br />\n!
      end
    end
    i += 1
  end
  return htm
end



# ファイル管理データベースを検索してHTMLとして返す。
def query_files(path, sql, columns=true)
  db = nil
  html = ""
  begin
    db = SQLite3::Database.new(path)
    if columns then
      rows = db.execute2(sql)
    else
      rows = db.execute(sql)
    end
    if rows.size == 0 then
      return "<p>empty!</p>"
    end
    html += "<table>\n"
    i = 0
    if columns then
      html += "<tr>"
      rows[i].each do |c|
        html += "<th>#{c}</th>"
      end
      html += "</tr>\n"
      i += 1
    end
    while i < rows.size do
      html += "<tr>"
      rows[i].each do |c|
        html += "<td>#{c}</td>"
      end
      html += "</tr>\n"
      i += 1
    end
    html += "</table>\n"
  ensure
    db.close() if db
  end
  return html
end


# データをinfoに挿入する。
def insert_filedb(db, data)
  sql = "INSERT INTO info (path, info, method, icon, dir, bin, `group`, tstamp) VALUES(:path, :info, :method, :icon, :dir, :bin, :group, :tstamp)"
  tstamp = DateTime.now.to_s
  items = {:path=>data[0], :info=>data[1], :method=>data[2], :icon=>data[3], :dir=>data[4], :bin=>data[5], :group=>data[6], :tstamp=>tstamp}
  db.execute(sql, items)
end

# データをinfoから削除する。
#   criteria: WHERE 句
def delete_filedb(db, criteria)
  sql = "DELETE FROM info WHERE " + criteria
  db.execute(sql)
end

# キー n のデータを更新する。
#   data: フィールド名:値の連想配列 [path,info,method,icon,dir,bin,group] (変更する項目のみ含む)
#   criteria: WHERE 句
def update_filedb(db, data, criteria)
  sql = "UPDATE info SET "
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
  db.execute(sql)
end

# 同じパス名のレコードのうち新しいほうを返す。
#   path: パス名
def query_path(db, path)
  result = nil
  sql = "SELECT n,path,info,method,icon,dir,bin,`group`,tstamp FROM info WHERE path='" + path + "'"
  db.execute(sql) do |row|
    if result.nil? then
      result = row
    elsif row[0] > result[0] then
      result = row
    end
  end
  return result
end


# 主キーpkのレコードを取得する。
def query_pk(db, pk)
  result = nil
  sql = "SELECT n,path,info,method,icon,dir,bin,`group`,tstamp FROM info WHERE n=" + pk.to_s
  db.execute(sql) do |row|
    result = row
  end
  return result
end


# パスがsrcのレコードをdestにコピーする。destが未登録の場合は追加する。
def copy_filedb(db, src, dest)
  r1 = query_path(db, src)
  return if r1.nil?
  r2 = query_path(db, dest)
  if r2.nil? then
    data = [dest, '', r1[3], r1[4], r1[5], r1[6], r1[7]]
    insert_filedb(db, data)
  else
    hash = {:method=>r1[3], :icon=>r1[4], :dir=>r1[5], :bin=>r1[6], :group=>r1[7]}
    update_filedb(db, hash, "path='#{dest}'")
  end
end

# パスがpksrcのレコードをpkdestにコピーする。
def copy_filedb_pk(db, pksrc, pkdest)
  r1 = query_pk(db, pksrc)
  return if r1.nil?
  r2 = query_pk(db, pkdest)
  return if r2.nil?
  hash = {:method=>r1[3], :icon=>r1[4], :dir=>r1[5], :bin=>r1[6], :group=>r1[7]}
  update_filedb(db, hash, "n=#{pkdest}")
end


# ファイル管理データベースのレコードの内容を別のレコードにコピーする。
# ただし、n,path,info,tstampは除く。その他のフィールドも空欄の時はコピーしない。
# destがディレクトリの場合、そのディレクトリに含まれるsrcと同じ拡張子のすべてのファイルにコピーする。
# さらに、登録されていないパスがある場合は、新規登録する。
#  src: コピー元のパス名
#  dest: コピー先のパス名
def copy_records(path, src, dest)
  db = SQLite3::Database.new(path)
  ext = File.extname(src)
  if test(?d, dest) then
    files = Dir.glob(dest + "/*" + ext)
    dir = dest
  else
    files = [File.basename(dest)];
    dir = File.dirname(dest)
  end
  files.each do |f|
    copy_filedb(db, src, f)
  end
end
