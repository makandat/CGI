# coding: utf-8
require 'sinatra'
require 'fileutils'
require 'pathname'
require 'base64'
require 'sqlite3'
require "yaml"
require 'mylogger'

Version = "3.0.0 (Suruga)"

# =====================================================
#   ファイル管理 DB
# =====================================================
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


#  Sinatra Ajax filer 

# =====================================================
#   メインクラス
# =====================================================
class Main < Sinatra::Base
  enable :inline_templates

  if RUBY_PLATFORM.downcase =~ /mswin/ then
    Config = "config_win.ini"
    Locations = "locations_win.ini"
    UserMenu = "usermenu.html"
  else
    Config = "config.ini"
    Locations = "locations.ini"
    UserMenu = "usermenu.html"
  end

  # configuration
  configure do
    @@start_dir = Dir.pwd()
    set :title, "Sinatra filer"
    set :stylesheet, "default.css"
    set :html, true
    set :backup, true
    set :ip, nil
    set :start, nil
    set :usermenu, ""

    if test(?f, Config) then
      open(Config).each do |s|
        if s.match(/title=/) then  # ページのタイトル
          p = s.split('=')
          set :title, p[1].strip
        end
        if s.match(/stylesheet=/) then  # Stylesheet
          p = s.split('=')
          set :stylesheet, p[1].strip
        end
        if s.match(/html=/) then  # HTMLをソースで表示するかレンダリングして表示するか
          p = s.split('=')
          if p[1].strip == 'text' then
            set :html, false
          else
            set :html, true
          end
        end
        if s.match(/backup=/) then   # 上書きの時バックアップファイルを作成するか
          p = s.split('=')
          if p[1].strip == 'yes' then
            set :backup, true
          else
            set :backup, false
          end
        end
        if s.match(/sqlite3=/) then  # SQLite3 データベースのパス
          p = s.split('=')
          set :sqlite3, p[1].strip
          @@filesdb = FilesDb.new(p[1].strip)
        end
        if s.match(/ip=/) then  # 接続を許すIPアドレス(正規表現)
          p = s.split('=')
          set :ip, p[1].strip
        end
        if s.match(/start=/) then  # スタート時に表示するHTMLページ
          p = s.split('=')
          set :start, p[1].strip
        end
      end
    end

    # location select control
    if test(?f, Locations) then
      str = ""
      open(Locations).each do |s|
        s.chomp!
        str << "<option>#{s}</option>\n"
      end
      set :bookmark, str
    else
      set :bookmark, <<EOS
<option selected="selected">~</option>
<option>/</option>
<option>/home</option>
<option>/var</option>
<option>/var/www</option>
<option>/var/log</option>
<option>/bin</option>
<option>/etc</option>
<option>/mnt</option>
<option>/usr</option>
<option>/usr/local</option>
EOS
    end

    # user menu
    if test(?f, UserMenu) then
      um = ""
      open(UserMenu) do |f|
        um = f.read()
      end
      set :usermenu, um
    end
  end

  # filter before method
  before do
    if request.path_info =~ /\/load_script\/.*/ then
      url = request.path_info.gsub('/load_script/', '/load_text/')
      redirect url
    elsif request.path_info =~ /\/save_script\/.*/ then
      url = request.path_info.gsub('/save_script/', '/save_text/')
      redirect url
    end
  end

  # template not found
  template :not_found do
<<HTML
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Not Found</title>
</head>

<body>
<h3 style="color:red;"><img src="/img/mini_error.png" alt="Error" /> The page was not found!</h3>
<p>
<a href="javascript:history.back();">[back]</a>
</p>
</body>
</html>
HTML
  end

  # template script result
  template :script_result do
<<HTML
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>script result</title>
</head>
<body>
<div><%= @script_result %></div>
<br />
</body>
</html>
HTML
  end

  # helper methods
  helpers do
    # Check client ip
    def checkClient(ip)
      if settings.ip.nil? then
        regex_ip = /^192\.168\.\d+\.\d+/
      else
        regex_ip = settings.ip
      end
      return (ip == '127.0.0.1' or ip.match(regex_ip) != nil)
    end

    # return "r","w","x"
    def get_attr(path, mode=0)
      str = ""
      if mode == 0 then
        str = " | "
        str += File.size(path).to_s + " | "
        str += File.ctime(path).to_s + " | "
        str += FileTest.symlink?(path) ? 'l' : ' '
      end
      str += FileTest.symlink?(path) ? 'l' : ' '
      str += FileTest.readable_real?(path) ? 'r' : ' '
      str += FileTest.writable_real?(path) ? 'w' : ' '
      str += FileTest.executable_real?(path) ? 'x' : ' '
      return str
    end # get_attr

    # return icon link
    def get_icon(path)
      ext = File.extname(path).downcase()
      p64 = Base64.encode64(path)
      ret = ""
      case ext
      when '.txt','.ini','.cnf','.conf','.def','.log'
        ret = %!<a href="javascript:getMessage('/text/#{p64}');"><img src="/img/mime_doc.png" alt="doc" border="0" /></a>\n!
      when '.pl','.php','.py','.rb','.c','.h','.cpp','.inc','.js','.cgi','.sh','.csh','.java'
        ret = %!<a href="javascript:getMessage('/text/#{p64}');"><img src="/img/mime_doc.png" alt="doc" border="0" /></a>\n!
      when '.jpg','.png','.gif'
        ret = %!<a href="javascript:getMessage('/image/#{p64}');"><img src="/img/mime_jpg.png" alt="img" border="0" /></a>\n!
      when '.html','.shtml'
        if settings.html then
          ret = %!<a href="javascript:getMessage('/markup/#{p64}');"><img src="/img/mime_doc.png" alt="htm" border="0" /></a>\n!
        else
          ret = %!<a href="javascript:getMessage('/text/#{p64}');"><img src="/img/mime_doc.png" alt="htm" border="0" /></a>\n!
        end
      when '.xml','.css','.xsl','.dtd','.xsd','.erb','.haml'
        ret = %!<a href="javascript:getMessage('/text/#{p64}');"><img src="/img/mime_doc.png" alt="xml" border="0" /></a>\n!
      when '.swf'
        ret = %!<a href="javascript:getMessage('/flash/#{p64}');"><img src="/img/mime_swf.png" alt="swf" border="0" /></a>\n!
      when '.svg'
        ret = %!<a href="javascript:getMessage('/svg/#{p64}');"><img src="img/mime_jpg.png" alt="svg" border="0" /></a>\n!
      when '.pdf'
        ret = %!<a href="javascript:getMessage('/pdf/#{p64}');"><img src="img/mime_doc.png" alt="pdf" border="0" /></a>\n!
      when '.mp3', '.ogg', '.wav'
        ret = %!<a href="javascript:getMessage('/audio/#{p64}');"><img src="img/mime_mp3.png" alt="aud" border="0" /></a>\n!
      when '.ogv', '.ogm', '.mp4', '.mov'
        ret = %!<a href="javascript:getMessage('/video/#{p64}');"><img src="img/mime_avi.png" alt="vid" border="0" /></a>\n!
      when '.zip', '.gz', '.tgz', '.7z', '.jar', '.lzh', '.rar'
        ret = %!<a href="javascript:getMessage('/zip/#{path}');"><img src="img/mime_zip.png" alt="zip" border="0" /></a>\n!
      else
      end
      return ret
    end # get_icon

    # if path is registered in files.db, gives link icon
    def get_files_icon(path)
      row = @@filesdb.query_path(path)
      return "" if row.nil?
      str = %! <a href="javascript:show_file_info('#{path}');"><img src="/img/mini_warning.png" alt="@" /></a>!
      return str
    end

    # get entries of dir
    def getContent(dir, all=false, info=false)
      dir = Base64.decode64(dir)
      if RUBY_PLATFORM.downcase =~ /mswin/ then
        dir.gsub!(/^~/, 'c:/')
      else
        dir.gsub!(/^~/, ENV['HOME'])
      end
      dir.gsub!(/\.$/, FileUtils.pwd())
      if not test(?d, dir) then
        return '<p style="color:red;text-align:center;">error! bad path. ' + dir + '</p>'
      end
      path = Pathname.new(dir)
      str = "<ol>\n"
      if dir != '/' then
        p = path.parent.to_s
        str += %!<li id="li1"><a href="javascript:getContent('#{p}');">[..]</a></li>\n! unless all
      end
      items = Dir.entries(dir)
      items.sort!
      i = 0
      i += 1 unless all
      items.each do |f|
        begin
          next if all == false and f.match(/^\./)
          i += 1
          if dir == '/' then
            abspath = "/" + f
          elsif f == "."
            abspath = dir
          elsif f == ".."
            abspath = path.parent.to_s
          else
            abspath = dir + "/" + f
          end
          if test(?d, abspath) then # directories
            attr = get_attr(abspath, 1)
            files_icon = get_files_icon(abspath) if info
            str += %!<li id="li#{i}"><a href="javascript:getContent('#{abspath}');">[#{f}]</a> #{attr}#{files_icon}</li>\n!
          else  # files
            icon = get_icon(abspath)
            attr = get_attr(abspath)
            files_icon = get_files_icon(abspath) if info
            str += %!<li id="li#{i}">#{icon} #{f}#{attr}#{files_icon}</li>\n!
          end
        rescue
        end
      end
      str += "</ol>\n"
      return str
    end # getContent

    # convert &, <, > to HTML code
    def escape_html(str)
      result = str.gsub('&', '&amp;')
      result = result.gsub('<', '&lt;')
      result = result.gsub('>', '&gt;')
      return result
    end

    # files.info record to HTML
    def to_html_path_info(row)
      fmt = <<EOS
<table style="margin-left:10px;margin-bottom:12px;">
<tr><th>field</th><th>value</th></tr>
<tr><td>n</td><td>%d</td></tr>
<tr><td>path</td><td>%s</td></tr>
<tr><td>info</td><td>%s</td></tr>
<tr><td>method</td><td>%s</td></tr>
<tr><td>icon</td><td>%s</td></tr>
<tr><td>dir</td><td>%d</td></tr>
<tr><td>bin</td><td>%d</td></tr>
<tr><td>group</td><td>%s</td></tr>
<tr><td>timestamp</td><td>%s</td></tr>
</table>
EOS
      info = row[2][0..100]
      method = "<pre>" + escape_html(row[3][0..100]) + "</pre>"
      icon = escape_html(row[4][0..100])
      return format(fmt, row[0], row[1], info, method, icon, row[5], row[6], row[7], row[8])
    end
  end  # helpers

  # not found (404)
  not_found do
    erb :not_found
  end


  # root
  get '/' do
    @location = FileUtils.pwd()
    @locations = settings.bookmark
    @content = getContent('~')
    @message = ""
    @title = settings.title + " " + Version
    @stylesheet = settings.stylesheet
    @usermenu = settings.usermenu
    if checkClient(request.ip) then
      htm = erb(:main)
    else
      htm = "Client " + request.ip + " is not allowed."
    end
    return htm
  end

  # list of dir contents
  get '/get_content/:dir' do |dir|
    d = Base64.decode64(dir)
    if settings.start and d == "~" then
      start_html = @@start_dir + "/" + settings.start
      html = "<p>Could not read 'start.html'</p>"
      open(start_html) do |f|
        html = f.read()
      end
      return html
    end
#    return getContent(dir)
    @location = FileUtils.pwd()
    @locations = settings.bookmark
    @content = getContent(dir)
    @message = ""
    @title = settings.title + " " + Version
    @stylesheet = settings.stylesheet
    @usermenu = settings.usermenu
    if checkClient(request.ip) then
      htm = erb(:main)
    else
      htm = "Client " + request.ip + " is not allowed."
    end
    erb :main
  end

  get '/get_content_all/:dir' do |dir|
    return getContent(dir, true, true)
  end

  # Text view
  get '/text/:path' do |path|
    path = Base64.decode64(path)
    f = nil
    str = "<pre>\n"
    begin
      f = open(path)
      i = 0
      while f.gets() do
        str += escape_html($_)
        i += 1
        if i > 4000 then
          str += "\nToo long! truncated.\n"
          break
        end
      end
    rescue => e
      str << e.message
    ensure
      f.close() if f
    end
    str += "</pre>\n"
    return str
  end

  get '/Text/*' do |path|
    f = nil
    path = "/" + path unless path[0] == '/'
    str = "<pre>\n"
    begin
      f = open(path)
      i = 0
      while f.gets() do
        str += escape_html($_)
        i += 1
        if i > 4000 then
          str += "\nToo long! truncated.\n"
          break
        end
      end
    rescue => e
      str << e.message
    ensure
      f.close() if f
    end
    str += "</pre>\n"
    return str
  end

  # Image view
  get '/image/:path' do |path|
    path = Base64.decode64(path)
    contentType = "image/" + File.extname(path).gsub!('.', '')
    contentType.gsub!(/jpg$/, 'jpeg')
    bindata = File.binread(path)
    content_type contentType
    #MyLogger.logger(contentType + " " + path)
    return bindata
  end

  get '/Image/*' do |path|
    content_type "image/" + File.extname(path).gsub!('.', '')
    path = "/" + path unless path[0] == '/'
    bindata = File.binread(path)
    return bindata
  end


  # SVG view
  get '/svg/:path' do |path|
    path = Base64.decode64(path)
    content_type "image/svg+xml"
    bindata = File.binread(path)
    #MyLogger.logger("image/svg+xml " + path)
    return bindata
  end

  get '/Svg/*' do |path|
    content_type "image/svg+xml"
    path = "/" + path unless path[0] == '/'
    bindata = File.binread(path)
    return bindata
  end

  # Flash view
  get '/flash/:path' do |path|
    path = Base64.decode64(path)
    content_type "application/x-shockwave-flash"
    bindata = File.binread(path)
    #MyLogger.logger("application/x-shockwave-flash " + path)
    return bindata
  end

  get '/Flash/*' do |path|
    content_type "application/x-shockwave-flash"
    path = "/" + path unless path[0] == '/'
    bindata = File.binread(path)
    return bindata
  end

  # Music / audio
  get '/audio/:path' do |path|
    path = Base64.decode64(path)
    ext = File.extname(path)
    case ext
    when '.wav'
      contentType = "audio/wav"
    when '.mp3'
      contentType = "audio/mp3"
    when '.ogg'
      contentType = "audio/ogg"
    else
      contentType = "audio/basic"
    end
    content_type contentType
    bindata = File.binread(path)
    #MyLogger.logger(contentType + " " + path)
    return bindata
  end

  get '/Audio/*' do |path|
    path = "/" + path unless path[0] == '/'
    ext = File.extname(path)
    case ext
    when '.wav'
      contentType = "audio/wav"
    when '.mp3'
      contentType = "audio/mp3"
    when '.ogg'
      contentType = "audio/ogg"
    else
      contentType = "audio/basic"
    end
    content_type contentType
    bindata = File.binread(path)
    #MyLogger.logger(contentType + " " + path)
    return bindata
  end

  # Video / movie
  get '/video/:path' do |path|
    path = Base64.decode64(path)
    ext = File.extname(path)
    case ext
    when '.mp4'
      contentType = "video/mp4"
    when '.ogv'
      contentType = "video/ogg"
    when '.mov'
      contentType = "video/quicktime"
    else
      contenttype = "video/mpeg"
    end
    content_type contentType
    bindata = File.binread(path)
    #MyLogger.logger(contentType + " " + path)
    return bindata
  end

  get '/Video/*' do |path|
    path = "/" + path unless path[0] == '/'
    ext = File.extname(path)
    case ext
    when '.mp4'
      contentType = "video/mp4"
    when '.ogv'
      contentType = "video/ogg"
    when '.mov'
      contentType = "video/quicktime"
    else
      contentType = "video/mpeg"
    end
    content_type contentType
    bindata = File.binread(path)
    #MyLogger.logger(contentType + " " + path)
    return bindata
  end

  # PDF view
  get '/pdf/:path' do |path|
    path = Base64.decode64(path)
    content_type "application/pdf"
    bindata = File.binread(path)
    return bindata
  end

  get '/Pdf/*' do |path|
    content_type "application/pdf"
    path = "/" + path unless path[0] == '/'
    bindata = File.binread(path)
    #MyLogger.logger("application/pdf " + path)
    return bindata
  end

  # HTML/XML view
  get '/markup/:path' do |path|
    path = Base64.decode64(path)
    f = nil
    begin
      f = open(path)
      str = f.read()
    rescue => e
      str = e.message
    ensure
      f.close() if f
    end
    return str
  end

  get '/Markup/*' do |path|
    path = "/" + path unless path[0] == '/'
    f = nil
    begin
      f = open(path)
      str = f.read()
    rescue => e
      str = e.message
    ensure
      f.close() if f
    end
    return str
  end

  # ZIP, RAR, 7z, LZH, gz, tgz,..
  get '/zip/*' do |path|
    path = '/' + path unless path[0] == '/'
    ext = File.extname(path)
    case ext
    when '.zip'
      content_type "application/zip"
    when '.jar'
      content_type "application/java-archive"
    when '.gz', '.tgz'
      content_type "application/compress"
    when '.7z'
      content_type "application/x-7z"
    when '.lzh'
      content_type "application/lha"
    when '.rar'
      content_type "application/x-rar-compressed"
    end
    bindata = File.binread(path)
    return bindata
  end

  # Execute command
  get '/command/:cmd' do |cmd|
    result = "(null)"
    cmd = Base64.decode64(cmd)
    begin
      case cmd
      when 'cd', 'chdir'
        p = ENV['HOME']
        Dir.chdir(p)
        result = Dir.pwd()
      when /^cd\s.+|^chdir\s.+/
        p = cmd.split(/\s+/)
        Dir.chdir(p[1].strip)
        result = Dir.pwd()
      else
        result = `#{cmd}`
        if result.nil? or result == "" then
          result = "Done."
        end
      end
      result = escape_html(result)
    rescue => e
      result = e.message
    end
    return '<pre>' + result + '</pre>'
  end

  # get tree
  get '/get_tree/:dir' do |dir|
    dir = Base64.decode64(dir)
    str = "<pre>\n"
    str += `tree #{dir}`
    str += "</pre>\n"
    return str
  end

  # run script by command input
  get '/script/:param' do |param|
    begin
      script = ""
      command = Base64.decode64(param)
      p = command.split('&')
      open(p[0]) do |f|
        script = f.read()
      end
      script = p[1] + "\n" + script if p.size > 1
      html = eval(script)
    rescue => e
      html = '<span style="color:red">Error! ' + e.message + '</span><br />'
      html += '<pre>'
      html += escape_html(script)
      html += '</pre>'
    end
    return html
  end

  # get form_script
  get '/form_script/' do
    erb :form_script
  end

  # post form_script
  post '/form_script/' do
    result = ""
    script = ""
    begin
      script = params[:script]
      is_empty = (script.match(/\w+/) == nil)
      save_path = params[:save_path]
      ruby = params[:ruby]
      if test(?f, save_path) and is_empty then
        open(save_path) do |f|
          script = f.read()
        end
      elsif save_path != "" and not is_empty then
        FileUtils.copy(save_path, save_path+".bak") if test(?f, save_path) and settings.backup
        f = open(save_path, "w")
        f.write(script)
        f.close()
      end
      if ruby == 'on' then
        params_json = params[:params_json]
        unless params_json.match(/^{.+}$/) then
          params_json = %!'{#{params_json}}'!
        end
        script = "require 'json/pure'\nparams = JSON.parse(" + params_json + ")\n" + script
        result = eval(script).to_s
      else
        if script.count("\n") > 0 then
          sftmp = Dir.tmpdir + '/sf_tmp_script.sh'
          f = open(sftmp, 'w')
          f.write(script)
          f.close()
          FileUtils.chmod(0755, sftmp)
          system(sftmp)
          result = "exit status = " + $?.to_s #+ " (" + sftmp +")"
        else
          result = `#{script}`
          result = escape_html(result)
          result = '<pre>' + result + '</pre>'
        end
      end
    rescue => e
      result << '<span style="color:red;">' << e.message << '</span><br />'
      if ruby == 'on' then
        result << '<pre>' << escape_html(script) << '<pre>'
      end
    end
    return result
  end

  # run script on new window
  get '/script_window/:path' do |path|
    begin
      save_path = Base64.decode64(path)
      script = "echo Error!"
      open(save_path) do |f|
        script = f.read() 
      end
      if save_path.match(/\.rb$/) then
        @script_result = eval(script).to_s
      else
        result = `#{script}`
        result = escape_html(result)
        @script_result = '<pre>' + result + '</pre>'
      end
    rescue => e
      @script_result = "<h3>Error! " + e.message + "</h3>"
    end
    erb :script_result
  end

  # run script on new window
  post '/script_window/' do
    begin
      path = params[:path]
      param_data = ""
      params.each_key do |key|
        param_data << key.to_s << "=\"" + params[key] + "\"\n"
      end
      script = ""
      open(path) do |f|
        script = f.read() 
      end
      script = param_data + script
      @script_result = eval(script).to_s
    rescue => e
      @script_result = "<h3>Error! " + e.message + "</h3>"
    end
    result = <<EOS
<!DOCTYPE html>
<html>
<head>
<title>result</title>
</head>
<body>
<a href="javascript:window.close();">[close]</a>
<hr />
<div>%result%</div>
<br />
</body>
</html>
EOS
    result = result.gsub('%result%', @script_result)
  end

  # return raw text
  get '/load_text/:path' do |path|
    f = nil
    str = ""
    begin
      path = Base64.decode64(path)
      f = open(path)
      while f.gets() do
        str << $_
      end
    rescue => e
      str << e.message
    ensure
      f.close() if f
    end
    return str
  end

  #  save raw text
  post '/save_text/' do
    f = nil
    begin
      path = params[:edit_path]
      data = params[:editor]
      FileUtils.copy(path, path + ".bak") if test(?f, path) and settings.backup
      f = open(path, "w")
      f.write(data);
      str = "saved to " + path
    rescue => e
      str = e.message
    ensure
      f.close() if f
    end
    return str
  end

  # file upload
  post '/file_upload/' do
    begin
      location = params[:upload_dir]
      f = params[:file][:tempfile]
      name = params[:file][:filename]
      path = location + "/" + name
      data = f.read()
      FileUtils.copy(path, path + ".bak") if test(?e, path) and settings.backup
      fo = open(path, "w")
      fo.write(data)
      fo.close()
      @upload_result = "uploaded " + path
    rescue => e
      @upload_result = e.message
    end
    erb :file_upload
  end

  # get full-path file list
  get '/get_fullpath/:dir' do |dir|
    dir = Base64.decode64(dir)
    dir.gsub!(/^~/, ENV['HOME'])
    if not test(?d, dir) then
      return '<p style="color:red;text-align:center;">error! bad path.<br />Usage: \\dir absolute_path.</p>'
    end
    unless dir.match(/\*/) then
      dir += "/*"
    end
    buff = ""
    Dir.glob(dir) do |f|
      buff << (f + "<br />\n")
    end
    return buff
  end

  # get full-path file list (for reference)
  get '/get_fullpath_nav/:dir' do |dir|
    dir = Base64.decode64(dir)
    dir.gsub!(/^~/, ENV['HOME'])
    if not test(?d, dir) then
      return '<p style="color:red;text-align:center;">error! bad path.<br />Usage: \\dir absolute_path.</p>'
    end
    unless dir.match(/\*/) then
      dir += "/*"
    end
    p1 = Pathname.new(dir)
    p2 = p1.parent
    parent = p2.parent.to_s
    buff = %!<a href="javascript:change_dir('#{parent}');"><img src="/img/folder_get.png" alt="up" style="border-width:0px;" /> ..</a><br />!
    files = Dir.glob(dir)
    files.sort!
    files.each do |f|
      if test(?d, f) then
        buff << %!<a href="javascript:change_dir('#{f}');"><img src="/img/folder_down.png" alt="dir" style="border-width:0px;" /></a> !
      end
      buff << (f + "<br />\n")
    end
    return buff
  end

  # get absolute path
  get '/get_abspath/:path' do |path|
    path = Base64.decode64(path)
    return File.expand_path(path)
  end

  # get Env variable
  get '/env/:key' do |key|
    content_type 'text/plain'
    return ENV[key]
  end

  # get current working directory
  get '/pwd/' do
    content_type 'text/plain'
    return Dir.pwd
  end

  # file or directory exists?
  get '/exists/:path' do |path|
    content_type 'text/plain'
    path = Base64.decode64(path)
    if test(?e, path) then
      return "true"
    end
    return "false"
  end

  # select info form
  get '/select_info/' do
    erb :form_select_info
  end


  # select info db
  post '/select_info/' do
    if @@filesdb.nil? then
      return '<p style="color:red;">This feature is not available.</p>'
    end
    begin
      criteria = ""
      criteria += ((params[:select_n] and params[:select_n] != "") ? params[:select_n] : "")
      if params[:select_path] and params[:select_path] != "" then
        criteria += " AND " unless criteria == ""
        criteria += ("path like '" + params[:select_path] +"'")
      end
      if params[:select_info] and params[:select_info] != "" then
        criteria += " AND " unless criteria == ""
        criteria += ("info like '" + params[:select_info] +"'")
      end
      if params[:select_method] and params[:select_method] != "" then
        criteria += " AND " unless criteria == ""
        criteria += ("method like '" + params[:select_method] + "'")
      end
      if params[:select_icon] and params[:select_icon] != "" then
        criteria += " AND " unless criteria == ""
        criteria += ("icon like '" + params[:select_icon] + "'")
      end
      if params[:select_dir] then
        criteria += " AND " unless criteria == ""
        criteria += ("dir=" + (params[:select_dir] ? "1" : "0"))
      end
      if params[:select_bin] then
        criteria += " AND " unless criteria == ""
        criteria += ("bin=" + (params[:select_bin] ? "1" : "0"))
      end
      if params[:select_group] and params[:select_group] != "" then
        criteria += " AND " unless criteria == ""
        criteria += ("`group`='" + (params[:select_group] + "'"))
      end
      if criteria == "" then
        message = "<p style='color:red;'>Criteria is null.</p>"
      else
        message = '<p>' + criteria + '</p>' + @@filesdb.get_result(criteria, true)
      end
    rescue => e
      message = "<p style='color:red;'>Error! " + e.message + "</p>"
    end
    return message
  end

  # select info by path
  get '/select_path/:path' do |path|
    if @@filesdb.nil? then
      return '<p style="color:red;">This feature is not available.</p>'
    end
    begin
      path = Base64.decode64(path)
      row = @@filesdb.query_path(path)
      message = row ? to_html_path_info(row) : path + " is not registered."
    rescue => e
      message = "<p style='color:red;'>Error! " + e.message + "</p>"
    end
    return message
  end

  # insert info db (form)
  get '/insert_info/:path' do |path|
    if @@filesdb.nil? then
      return '<p style="color:red;">This feature is not available.</p>'
    end
    @insert_path = Base64.decode64(path)
    @insert_dir = test(?d, path) ? 'checked="checked"' : ''
    erb :form_insert_info
  end

  # insert info db (query)
  post '/insert_info/' do
    if @@filesdb.nil? then
      return '<p  style="color:red;">This feature is not available.</p>'
    end
    data = Array.new  # [path,info,method,icon,dir,bin,group]
    begin
      data.push(params[:insert_path])
      data.push(params[:insert_info])
      data.push(params[:insert_method].nil? ? '' : params[:insert_method])
      data.push(params[:insert_icon].nil? ? '' : params[:insert_icon])
      data.push(params[:insert_dir] ? 1 : 0)
      data.push(params[:insert_bin] ? 1 : 0)
      data.push(params[:insert_group].nil? ? '' : params[:insert_group])
      @@filesdb.insert(data)
      n = @@filesdb.get_max()
      message = "Done. record n = " + n.to_s
    rescue => e
      message = "<p style='color:red;'>Error! " + e.message + "</p>"
    end
    return message
  end

  # delete info db
  get '/delete_info/:path' do |path|
    if @@filesdb.nil? then
      return '<p style="color:red;">This feature is not available.</p>'
    end
    begin
      path = Base64.decode64(path)
      @@filesdb.delete("path='" + path + "'")
      message = "Deleted info " + path
    rescue => e
      message = "<p style='color:red;'>Error! " + e.message + "</p>"
    end
    return message
  end

  # update info db (form)
  get '/update_info/:path' do |path|
    if @@filesdb.nil? then
      return '<p style="color:red;">This feature is not available.</p>'
    end
    begin
      path = Base64.decode64(path)
      row = @@filesdb.query_path(path)
      return "<p style='color:red;'>Error! no data.</p>" if row.nil?
      @update_n = row[0]
      @update_path = row[1]
      @update_info = row[2]
      @update_method = row[3]
      @update_icon = row[4]
      @update_dir = row[5].to_i == 0 ? "" : 'checked="checked"'
      @update_bin = row[6].to_i == 0 ? "" : 'checked="checked"'
      @update_group = row[7]
      @update_tstamp = row[8]
      erb :form_update_info
    rescue => e
      "Error! " + e.message
    end
  end

  # update info db (query)
  post '/update_info/' do
    if @@filesdb.nil? then
      return '<p style="color:red;">This feature is not available.</p>'
    end
    begin
      criteria = "n=" + params[:n]
      if params[:dir].nil? then
        params[:dir] = 0
      elsif params[:dir] == "on" or params[:dir] == "true" then
        params[:dir] = 1
      else
        params[:dir] = 0
      end
      if params[:bin].nil? then
        params[:bin] = 0
      elsif params[:bin] == "on" or params[:bin] == "true" then
        params[:bin] = 1
      else
        params[:bin] = 0
      end
      @@filesdb.update(params, criteria)
      return "Updated! " + criteria
    rescue => e
      "Error! " + e.message
    end
  end

  # file info icon
  get '/detail_icon/:dir' do |dir|
    getContent(dir, false, true)
  end

  # ファイル情報データベースのメソッドを実行する。
  get '/method/:param' do |param|
    if @@filesdb.nil? then
      return '<p style="color:red;">This feature is not available.</p>'
    end
    p = Base64.decode64(param)
    ps = p.split('&')
    row = @@filesdb.query_path(ps[0])
    if row.nil? then
      return '<p style="color:red;">' + ps[0] + " is not registered.</p>"
    end
    method = row[3].to_s
    if not method.match(/\w+/) then
      return '<p style="color:red;">' + ps[0] + " 's method is empty.</p>"
    end
    script = "path = '" + ps[0] + "'\n"
    if ps.size > 1 then
      if ps[1] =~ /^echo/ then
        method = escape_html(method)
        s = escape_html(ps[1])
        return '<pre class="code">' + script + "\n" + s + "\n" + method + '</pre>'   # 実行スクリプト確認用
      else
        script += ps[1] + "\n" + method
      end
    else
      script += method
    end
    result = eval(script)
    if result.nil? or result == "" then
      result = "result: (null)"
    end
    return result
  end

  # ファイル情報の表示（HTML)
  get '/info_detail/:path' do |path|
    if @@filesdb.nil? then
      return '<p style="color:red;">This feature is not available.</p>'
    end
    path = Base64.decode64(path)
    row = @@filesdb.query_path(path)
    if row.nil? then
      return '<p style="color:red;">' + path + " is not registered.</p>"
    end
    return row[2]
  end

  # ファイルメソッドの表示（HTML)
  get '/method_detail/:path' do |path|
    if @@filesdb.nil? then
      return '<p style="color:red;">This feature is not available.</p>'
    end
    path = Base64.decode64(path)
    row = @@filesdb.query_path(path)
    if row.nil? then
      return '<p style="color:red;">' + path + " is not registered.</p>"
    end
    str = escape_html(row[3])
    return '<pre class="code">' + str + '</pre>'
  end


  #  show icon/thumb of files db
  get '/view_thumb/:path' do |path|
    path = Base64.decode64(path)
    row = @@filesdb.query_path(path)
    if row.nil? then
      return '<p style="color:red;">' + path + " is not registered.</p>"
    end
    icon = row[4].to_s
    pk = row[0].to_s
    if icon == "" then
      return '<p style="color:red;">icon record of ' + path + " is empty.</p>"
    end
    if test(?f, icon) then
      result = '<img src="/image/' + Base64.encode64(icon) + '" alt="img" />'
    else
      result = '<img src="/image_db/' + pk + '" alt="img" />'
    end
    return result
  end

  #  return icon content in files db
  get '/image_db/:pk' do |pk|
    rows = @@filesdb.query('n=' + pk)
    if rows.size == 0 then
      return '<p style="color:red;">' + path + " is not registered.</p>"
    end
    begin
      icon = rows[0][4].to_s
      image = Base64.decode64(icon)
    rescue => e
      return 'Error! ' + e.message
    end
    content_type 'image/jpeg'
    return image
  end

  #  update icon/thumb field of files db
  get '/update_thumb/:path' do |path|
    @path = Base64.decode64(path)
    row = @@filesdb.query_path(@path)
    if row.nil? then
      return '<p style="color:red;">' + path + " is not registered.</p>"
    end
    erb :update_thumb
  end

  #  update icon/thumb field of files db
  post '/update_thumb/' do
    path = params[:path]
    thumb = params[:thumb]
    row = @@filesdb.query_path(path)
    if row.nil? then
      return '<p style="color:red;">' + path + " is not registered.</p>"
    end
    begin
      icon = row[4].to_s
      b = File.binread(thumb)
      b64 = Base64.encode64(b)
      criteria = "path='" + path + "'"
      data = {:icon=>b64}
      @@filesdb.update(data, criteria)
      message = "Done."
    rescue => e
      message = "Error! " + e.message
    end
    return message
  end

  # reference window
  get '/reference/:dir' do |dir|
    @refer_dir = Base64.decode64(dir)
    @stylesheet = settings.stylesheet
    @locations = settings.bookmark
    erb :reference
  end

end # class

# ======================
#  Start Application
# ======================
Main.run!



__END__

@@ main

<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title><%= @title %></title>
<link rel="stylesheet" href="<%= @stylesheet %>" />
<script type="text/javascript" src="/js/jquery-1.6.1.min.js"></script>
<script type="text/javascript" src="/js/base64.js"></script>
<script type="text/javascript">

var list_all = false;
var timer_id = null;

// get path of list
function get_path(n) {
  var p1, p2;
  var p = $("#li" + n).text();
  if (p == null)
    return "";
  p = p.split('|');
  var dir = $('#location').text();
  if (p[0].match(/\[.+\]/)) {
    p1 = p[0].indexOf('[', 0);
    p2 = p[0].indexOf(']', 0);
    cs = dir + "/" + p[0].substring(p1+1, p2);
  }
  else {
    cs = dir + "/" + p[0].replace(/^\s+|\s+$/g, "");
  }
  return cs;
}

// internal command executing
function internal_command(cmd) {
  var n, p, dir, file, bm, path, cs, p1, p2;
  var abspath;
  if (cmd.match(/^\\\d+$/)) {   //  \n  (cache path name)
    n = cmd.substr(1, cmd.length - 1);
    cs = get_path(n);
    if (sessionStorage.cache == null)
      sessionStorage.cache = "";
    if (cs != "") {
      sessionStorage.last_cache = cs
      sessionStorage.cache += cs + "\n";
      $("#message").html('cached ' + cs);
    }
  }
  else if (cmd == "\\rl") {
    path = $("#locations option:selected").text();
    getContent(path);
  }
  else if (cmd == "\\r") {
    path = $('#location').text();
    getContent(path);
  }
  else if (cmd == "\\rs") {
    getContent("~");
  }
  else if (cmd == "\\ab") {  // add bookmark current dir
    bm = localStorage.bookmarks;
    if (bm == null)
      bm = "";
    bm += $("#location").text() + "\n";
    localStorage.bookmarks = bm;
    $("#message").html('bookmark ' + $("#location").text());
  }
  else if (cmd.match(/^\\ab\s\d+$/)) {  // \ab n  (add bookmark)
    // save localStorage
    n = cmd.substr(4, cmd.length - 4);
    bm = localStorage.bookmarks;
    if (bm == null)
      bm = "";
    bm += (get_path(n) + "\n");
    if (bm != "\n") {
      localStorage.bookmarks = bm;
      $("#message").html('bookmark ' + $("#li" + n).text());
    }
  }
  else if (cmd == "\\cb") {  //  \cb  (clear bookmark)
    localStorage.bookmarks = "";
    $("#message").html("bookmarks was cleared.");
  }
  else if (cmd.match(/^\\cd\s.+/)) {  // \cd .. (chdir ..)
    path = cmd.substr(4, cmd.length - 4);
    getContent(path);
  }
  else if (cmd == "\\dir") {
    dir = $("#location").text();
    url = "/get_abspath/" + base64.encode(dir);
    $("#message").html("fetching ..");
    $.get(url, function(data) {
      abspath = data
    });
    url = "/get_fullpath/" + base64.encode(dir);
    $.get(url, function(data) {
      $("#content").html(data);
      $("#message").html("get_fullpath " + dir);
      $("#location").html(abspath);
    });
  }
  else if (cmd.match(/^\\dir\s.+/)) {  // \dir .. (dir ..)
    dir = cmd.substr(5, cmd.length - 5);
    abspath = dir
    url = "/get_abspath/" + base64.encode(dir);
    $("#message").html("fetching ..");
    $.get(url, function(data) {
      abspath = data
    });
    url = "/get_fullpath/" + base64.encode(dir);
    $.get(url, function(data) {
      $("#content").html(data);
      $("#message").html("get_fullpath " + dir);
      $("#location").html(abspath);
    });
    $.get('/pwd/', function(pwd) {
      $("#pwd").text(pwd)
    });
  }
  else if (cmd == "\\h") {  // \h - history
    showHistory();
  }
  else if (cmd == "\\hc") {  // \hc - clear history
    sessionStorage.history = "";
    alert("Command history was cleared!");
    showHistory();
  }
  else if (cmd == "\\.") {
    p = 'cd ' + $('#location').text();
    execCommand(p);
    $.get('/pwd/', function(pwd) {
      $("#pwd").html('<a href="javascript:move_location();">pwd:</a> ' + pwd)
    });
  }
  else if (cmd.match(/^\\ed\s.+/) != null) {  // \ed - edit
    n = cmd.substr(4, cmd.length - 4);
    file = get_path(n);
    path = base64.encode(file);
    $("#edit_path").val(file);
    url = "/exists/" + path;
    $.get(url, function(data) {
      if (data == "true") {
        url = "/load_script/" + path;
        $.get(url, function(data) {
          $("#editor").css("display", "block");
          $("#message").css("display", "none");
          $("#edit_button").css("display", "none");
          $("#save_button").css("display", "block");
          $("#editor").val(data);
        });
      }
      else {
        $("#editor").css("display", "block");
        $("#message").css("display", "none");
        $("#edit_button").css("display", "none");
        $("#save_button").css("display", "block");
        $("#editor").val("");
      }
    });
  }
  else if (cmd == "\\cp") {
    if (sessionStorage.last_cache != null)
      $("#command").val("cp -v " + sessionStorage.last_cache + " " + $("#location").text());
  }
  else if (cmd == "\\mv") {
    if (sessionStorage.last_cache != null)
      $("#command").val("mv -v " + sessionStorage.last_cache + " " + $("#location").text());
  }
  else if (cmd == "\\rm") {
    if (sessionStorage.last_cache != null)
      $("#command").val("rm -v " + sessionStorage.last_cache);
  }
  else if (cmd == "\\bk" && sessionStorage.prev_location != null) {
    getContent(sessionStorage.prev_location);
  }
  else if (cmd == "\\cc") {
    sessionStorage.cache = "";
    alert("Path cache was cleared!");
  }
  else if (cmd.match(/\\ii\s.+/) != null) {  // insert info
    n = cmd.substr(4, cmd.length - 4);
    url = '/insert_info/' + base64.encode(get_path(n));
    $.get(url, function(data) {
     $("#message").html(data);
    });
  }
  else if (cmd.match(/\\id\s.+/) != null) {  // delete info
    n = cmd.substr(4, cmd.length - 4);
    if (n.match(/\d+/) != null) {
      url = '/delete_info/' + base64.encode(get_path(n));
    }
    else {
      url = '/delete_info/' + base64.encode(n);
    }
    $.get(url, function(data) {
     $("#message").html(data);
    });
  }
  else if (cmd.match(/\\iu\s.+/) != null) {  // update info
    n = cmd.substr(4, cmd.length - 4);
    if (n.match(/\d+/) != null) {
      url = '/update_info/' + base64.encode(get_path(n));
    }
    else {
      url = '/update_info/' + base64.encode(n);
    }
    $.get(url, function(data) {
     $("#message").html(data);
    });
  }
  else if (cmd.match(/\\iq\s.+/) != null) {  // query info
    n = cmd.substr(4, cmd.length - 4);
    if (n.match(/\d+/) != null) {
      url = '/select_path/' + base64.encode(get_path(n));
    }
    else {
      url = '/select_path/' + base64.encode(n);
    }
    $.get(url, function(data) {
     $("#message").html(data);
    });
  }
  else if (cmd.match(/\\is/) != null) {  // select info
    url = '/select_info/'
    $.get(url, function(data) {
     $("#message").html(data);
    });
  }
  else if (cmd.match(/\\iv/) != null) {  // registered info view
    dir = base64.encode($("#location").text());
    url = '/detail_icon/' + dir
    $.get(url, function(data) {
     $("#content").html(data);
    });
  }
  else if (cmd.match(/\\ix\s.+/) != null) {  // execute method
    p = cmd.indexOf(';', 0);
    if (p < 0) {
      n = cmd.substr(4, cmd.length - 4);
      p2 = "";
    }
    else {
      p1 = cmd.split(';');
      p2 = p1[1];
      n = p1[0].substr(4, p1[0].length - 4);
    }
    cs = get_path(n) + "&" + p2;
    url = '/method/' + base64.encode(cs);
    $.get(url, function(data) {
      $("#message").html(data);
    });
  }
  else if (cmd.match(/\\iz\s.+/) != null) {  // execute script
    p = cmd.indexOf(';', 0);
    if (p < 0) {
      n = cmd.substr(4, cmd.length - 4);
      p2 = "";
    }
    else {
      p1 = cmd.split(';');
      p2 = p1[1];
      n = p1[0].substr(4, p1[0].length - 4);
    }
    cs = get_path(n) + "&" + p2;
    url = '/script/' + base64.encode(cs);
    $.get(url, function(data) {
      $("#message").html(data);
    });
  }
  else if (cmd.match(/\\if\s.+/) != null) {  // file info detail (HTML view)
    n = cmd.substr(4, cmd.length - 4);
    if (n.match(/^\d+$/) != null)
      cs = get_path(n)
    else
      cs = n
    url = '/info_detail/' + base64.encode(cs);
    $.get(url, function(data) {
      $("#message").html(data);
    });
  }
  else if (cmd.match(/\\im\s.+/) != null) {  // file method detail
    n = cmd.substr(4, cmd.length - 4);
    if (n.match(/^\d+$/) != null)
      cs = get_path(n)
    else
      cs = n
    url = '/method_detail/' + base64.encode(cs);
    $.get(url, function(data) {
      $("#message").html(data);
    });
  }
  else if (cmd.match(/\\ip\s.+/) != null) {  // file icon view
    n = cmd.substr(4, cmd.length - 4);
    if (n.match(/^\d+$/) != null)
      cs = get_path(n)
    else
      cs = n
    url = '/view_thumb/' + base64.encode(cs);
    $.get(url, function(data) {
      $("#message").html(data);
    });
  }
  else if (cmd.match(/\\ig\s.+/) != null) {  // file icon update
    n = cmd.substr(4, cmd.length - 4);
    if (n.match(/^\d+$/) != null)
      cs = get_path(n)
    else
      cs = n
    url = '/update_thumb/' + base64.encode(cs);
    $.get(url, function(data) {
      $("#message").html(data);
    });
  }
  else if (cmd == "\\?") {
    $("#message").load("command_help.html");
  }
  else {
    $("#message").html('<span style="color:red;">' + cmd + " is not a command!</span>");
  }
}


// Simple command input and execute
function simple_command(cmd) {
  var n2 = cmd.indexOf(' ', 0);
  if (n2 < 0)
    n2 = cmd.length;
  var n = cmd.substring(1, n2);
  var pn = get_path(n);
  var cmd2 = (pn + cmd.substring(n2, cmd.length));
  if (pn.match(/\.class$/) != null) {
    var ss = pn.split('/');
    cmd2 = "java " + ss[ss.length-1].replace('.class', '');
  }
  else if (pn.match(/\.jar$/) != null) {
    cmd2 = "java -jar " + cmd2;
  }
  else if (pn.match(/\.exe$/) != null) {
    cmd2 = "mono " + cmd2;
  }
  else if (pn.match(/\.pl$/) != null) {
    cmd2 = "perl " + cmd2;
  }
  else if (pn.match(/\.py$/) != null) {
    cmd2 = "python " + cmd2;
  }
  else if (pn.match(/\.rb$/) != null) {
    cmd2 = "ruby " + cmd2;
  }
  $("#message").html("executing ..");
  url = '/command/' + base64.encode(cmd2);
  $.get(url, function(htm) {
    $("#message").html(htm);
  });
  location.href = "#message";  // jump to named anchor 'message'
}

// chdir id "location" place
function move_location() {
  var p = 'cd ' + $('#location').text();
  execCommand(p);
  $('#pwd').html('<a href="javascript:move_location();">pwd:</a> ' + $('#location').text())
}

// show top pane as location
function showLocation(dir) {
  if (dir == '~') {
    $.get('/env/HOME', function(data) {
      dir = data
    });
  }
  $.get('/pwd/', function(pwd) {
    $("#pwd").html('<a href="javascript:move_location();">pwd:</a> ' + pwd)
  });
  $("#location").html(dir);
}

// show bottom pane
function showMessage(msg) {
  $("#message").html(msg);
  location.href = "#message";
}

// get content of dir
function getContent(dir) {
  var url;

  $("#message").css('display', 'block');
  $("#editor").css('display', 'none');
  $("#edit_button").css('display', 'none');
  $("#save_button").css('display', 'none');

  sessionStorage.prev_location = $('#location').text();
  if (list_all == true)
    url = "/get_content_all/" + base64.encode(dir);
  else
    url = "/get_content/" + base64.encode(dir);
/*
  showLocation(dir);
  $("#message").html("fetching ..");
  $.get(url, function(htm) {
    $("#content").html(htm);
    showMessage('get_content ' + dir);
  });
*/
  location.replace(url);
}


// get message from url
function getMessage(url) {
  var p;

  $("#message").css('display', 'block');
  $("#editor").css('display', 'none');
  $("#edit_button").css('display', 'none');
  $("#save_button").css('display', 'none');

  if (url.match(/image\//) != null) {
    $("#message").html('<img src="' + url + '" alt="url" border="0" />');
  }
  else if (url.match(/svg\//) != null) {
    $("#message").html('<object type="image/svg+xml" data="' + url + '">svg</object>');
  }
  else if(url.match(/flash\//) != null) {
    $("#message").html('<object type="application/x-shockwave-flash" data="' + url + 
     '" width="300" height="300"><param name="movie" value="' + url + '" />flash</object>');
  }
  else if (url.match(/pdf\//) != null) {
    $("#message").html('<iframe src="' + url + '" width="800" height="500">pdf</ifrmae>');
  }
  else if (url.match(/markup\//) != null) {
    $("#message").html("fetching ..");
    $.get(url, function(htm) {
      s = '<iframe src="' + url + '" width="800" height="500">html</iframe>'
      $("#message").html(s);
    });
  }
  else if (url.match(/audio\//) != null) {
    $("#message").html('<audio src="' + url + '" controls="controls">audio</audio>');
  }
  else if (url.match(/video\//) != null) {
    $("#message").html('<video src="' + url + '" controls="controls">video</video>');
  }
  else if (url.match(/zip\//) != null) {
    window.location = url;
  }
  else {
    $("#message").html("fetching ..");
    $.get(url, function(htm) {
      $("#message").html(htm);
      $("#message").css('display', 'block');
      // $("#editor").css('display', 'none');
      $("#edit_button").css('display', 'block');
      // $("#save_button").css('display', 'none');
      p = base64.decode(url.substring(6, url.length));
      $("#edit_path").val(p);
    });
  }
  location.href = "#message";
}


// tree
function getTree(dir) {
  $("#message").css('display', 'block');
  $("#editor").css('display', 'none');
  $("#edit_button").css('display', 'none');
  $("#save_button").css('display', 'none');

  var url = "/get_tree/" + base64.encode(dir);
  showLocation(dir);
  $("#message").html("fetching ..");
  $.get(url, function(htm) {
    $("#content").html(htm);
    showMessage('get_tree ' + dir);
  });
}

// exec cmmand
function execCommand(cmd) {
  var s, m, n, p, dir, url, p1, p2, cs;

  $("#message").css('display', 'block');
  $("#editor").css('display', 'none');
  $("#edit_button").css('display', 'none');
  $("#save_button").css('display', 'none');

  if (cmd.match(/^\\.+/) != null) {
    internal_command(cmd);
  }
  else if (cmd == "?") {
    $("#message").load("command_help.html");
  }
  else if (cmd.match(/^\!\d+/) != null) {
    simple_command(cmd);
  }
  else {
    if (cmd.match(/\s#\d+/) != null) {
      try {
        m = cmd.match(/#\d+/);
        n = m[0].length;
        n = m[0].substring(1, n);
        p = $("#li" + n).text().split(' ');
        dir = $('#location').text();
        if (p[0].match(/\[.+\]/)) {
          p1 = p[0].indexOf('[', 0);
          p2 = p[0].indexOf(']', 0);
          cs = dir + "/" + p[0].substring(p1+1, p2);
        }
        else {
          cs = dir + "/" + p[1];
        }
        cmd = cmd.replace(/#\d+/, cs);
      }
      catch (e) {
        alert(e);
      }
    }
    $("#message").html("executing ..");
    url = '/command/' + base64.encode(cmd);
    $.get(url, function(htm) {
      $("#message").html(htm);
    });
    location.href = "#message";  // jump to named anchor 'message'
  }
  var his = "";
  if (sessionStorage.history != null)
    his = sessionStorage.history;
  //his += cmd.replace(/"/g, "\"");
  his += cmd
  his += "\n";
  sessionStorage.history = his;
}


// set value to command input control
function setCommand(c) {
  $("#command").val(c);
}

// show command history
function showHistory() {
  var h;
  $("#message").css('display', 'block');
  $("#editor").css('display', 'none');
  $("#edit_button").css('display', 'none');
  $("#save_button").css('display', 'none');

  var str = "<ol>\n";
  var hist = sessionStorage.history.split("\n");
  for (var i = 0; i < hist.length; i++) {
    if (hist[i] != "") {
      str += "<li>";
      h = hist[i];
      if (h.match(/^\\/) != null)
        h = h.replace(/^\\/, "\\\\");
      str += '<a href="javascript:setCommand(\'' + h + '\');">' + hist[i] + '</a>';
      str += "</li>\n";
    }
  }
  str += "</ol>\n";
  $("#content").html(str);
}


// get form for scripting
function getScript() {
  $("#message").css('display', 'block');
  $("#editor").css('display', 'none');
  $("#edit_button").css('display', 'none');
  $("#save_button").css('display', 'none');

  var url = '/form_script/'
  $("#message").html('opening ..')
  $.get(url, function(form) {
    $("#content").html(form);
    $("#message").html('OK')
  });
}

// post form (Save and Run button)
function postScript() {
  var url = '/form_script/'
  params = $("#form_script").serialize();
  $("#message").html('running ..')
  $.post(url, params, function(data, status) {
    if (status == "success") {
      $("#message").html(data);
    }
    else {
      $("#message").html('<span style="color:red;">error!</span>');
    }
  });
}


// post form in New Window (save_path)
function openScriptWindow() {
  if ($("#save_path").val() == "") {
    alert('Please, save script!');
  }
  else {
    var p = base64.encode($("#save_path").val());
    var url = '/script_window/' + p;
    window.open(url, "result");
  }
}


// post form in New Window (function parameter)
function runRuby(path) {
  var p = base64.encode(path);
  var url = '/script_window/' + p;
  window.open(url, "result");
}


// load script (Load button)
function loadScript() {
  if ($('#save_path').val() == "") {
    alert("Please, enter save path! (to load)");
    return;
  }
  var url = '/load_script/' + base64.encode($('#save_path').val());
  $("#message").html('loading ..');
  $.get(url, function(data) {
    $("#script").val(data);
    $("#message").html('loaded ' + $('#save_path').val());
  });
}


// Load script_gallery.html
function scriptGallery() {
  $("#content").load('script_gallery.html');
}


// save bookmarks from id="bookmarks"
function saveBookmark() {
  var s = $("#bookmarks").val();
  localStorage.bookmarks = s;
  alert("Bookmarks saved!");
}

// show bookmark
function showBookmark() {
  var bm, list;
  if (localStorage.bookmarks) {
    bm = localStorage.bookmarks;
  }
  else {
    bm = "";
  }

  list = bm.split("\n");
  var s = "<form action=\"javascript:saveBookmark();\">";
  s += "<textarea id=\"bookmarks\" cols=\"60\" rows=\"10\" style=\"font-size:small;\">"
  for (i = 0; i < list.length; i++) {
    s += list[i] + "\n";
  }
  s += "</textarea>\n";
  s += "<br /><input type=\"submit\" value=\"Save\" />";
  s += "</form>\n";
  $("#content").html(s);
}

// show cache
function showCache() {
  if (sessionStorage.cache) {
    cs = sessionStorage.cache;
  }
  else {
    cs = "no caches";
  }

  var list = cs.split("\n");
  var s = "<div id=\"cache\" style=\"background-color:#f0f8e0;\">"
  for (i = 0; i < list.length; i++) {
    s += list[i] + "<br />\n";
  }
  s += "</div>\n";
  $("#content").html(s);
}


// show textarea to edit
function editText() {
  $("#editor").css("display", "block");
  $("#editor").val($("#message").text());
  $("#message").css("display", "none");
  $("#edit_button").css("display", "none");
  $("#save_button").css("display", "block");
}


// save textarea to edit
function saveText(params) {
  var url = '/save_text/'
  var params = $("#form_save_text").serialize();
  //$("#message").html('saving ..');
  $.post(url, params, function(data, status) {
    if (status == "success") {
      alert(data);
    }
    else {
      alert("error!");
    }
  });
}



function showUploadForm() {
  $('#upload_dir').val($('#location').text());
  $('#upload_dir2').html("Will be uploaded to '" + $('#location').text() + "'");
  $('#upload_form').css('display', 'block');
}


// file upload (drag & drop)
function uploadFiles(files) {
  var filedata = new FormData();
  filedata.append('location', $("#location").text());
  filedata.append("file", files[0]);
  $.post('/file_upload/', filedata, function(data, status) {
    if (status == "success") {
      alert(data);
    }
    else {
      alert("error!");
    }
  });
}


// show new window to refer file list
function showReferenceWindow() {
  var dir = $('#location').text();
  var url = '/reference/' + base64.encode(dir);
  window.open(url, 'reference', 'width=800,height=600,location=no,scrollbars=yes');
}


// show file info of path
function show_file_info(path) {
  url = '/select_path/' + base64.encode(path);
  $.get(url, function(data) {
    $("#message").html(data);
  });
}

// action form_insert_info
function insert_info() {
  var url = '/insert_info/'
  params = $("#form_insert_info").serialize();
  $("#message").html('running ..')
  $.post(url, params, function(data, status) {
    if (status == "success") {
      $("#message").html(data);
    }
    else {
      $("#message").html('<span style="color:red;">error!</span>');
    }
  });
}


// action form_select_info
function select_info() {
  var url = '/select_info/'
  params = $("#form_select_info").serialize();
  $("#message").html('running ..')
  $.post(url, params, function(data, status) {
    if (status == "success") {
      $("#message").html(data);
    }
    else {
      $("#message").html('<span style="color:red;">error!</span>');
    }
  });
}


// action form_update_info
function update_info() {
  var url = '/update_info/'
  params = $("#form_update_info").serialize();
  $("#message").html('running ..')
  $.post(url, params, function(data, status) {
    if (status == "success") {
      $("#message").html(data);
    }
    else {
      $("#message").html('<span style="color:red;">error!</span>');
    }
  });
}

// post /update_thumb/
function update_thumb() {
  var url = "/update_thumb/";
  params = $('#form_update_thumb').serialize();
  $("#message").html('fetching ..')
  $.post(url, params, function(data, status) {
    if (status == "success") {
      $("#message").html(data);
    }
    else {
      $("#message").html('<span style="color:red;">error!</span>');
    }
  });
}

// Show HTML in content pane.
function show_content(path) {
  url = '/exists/' + base64.encode(path)
  $.get(url, function(data) {
    if (data == "true") {
      url = "/Markup" + path;
      $.get(url, function(htm) {
        $('#content').html(htm);
        $('#message').text(path);
      });
    }
    else {
      $('#message').text('error! not found');
    }
  });
}


// timer start
function timerStart(interval) {
  timer_id =  setTimeout(timerHandler, interval);  // return timer_id
}


// timer stop
function timerStop() {
  clearTimeout(timer_id);
}

// timer event
function timerHandler(interval) {
/*
  today = new Date();
  $('#message').text(today.toUTCString());
*/
  timerStart(interval);
}

//
// onload
$(document).ready(function() {
/*
  // show /home/user content
  $.get('/env/HOME', function(home) {
    var url = "/get_content/" + base64.encode("~");
    $("#message").html("fetching ..");
    $.get(url, function(htm) {
      $("#content").html(htm);
      $("#message").html('<span style="color:green;">OK</a>');
      $("#location").html(home);
    });
    $.get('/pwd/', function(pwd) {
      $("#pwd").html('<a href="javascript:move_location();">pwd</a>: ' + pwd)
    });
  });
*/

  // location changed
  $("#locations").bind('change', function() {
    dir = $("#locations option:selected").text();
    showLocation(dir);
    getContent(dir);
  });

  // exec button click
  $("#exec").click(function() {
    execCommand($("#command").val());
  });

  // bind drop event to 'location'
  $("#location").bind("drop", function (e) {
    var files = e.originalEvent.dataTransfer.files;
    uploadFiles(files);
  })
  .bind("dragenter", function () {
    return false;
  })
  .bind("dragover", function () {
    return false;
  });

  //timerStart(500);
});


</script>
</head>

<body>
<a name="top"></a>
<div class="body">

<table width="100%">
<!-- row 1 -->
<tr>
<td colspan="2">
<form id="upload_form" name="upload_form" method="post" action="/file_upload/" enctype="multipart/form-data" style="display:none;">
  upload file: <br />
  <input id="file" name="file" type="file"  size="80" />
  <input type="hidden" name="upload_dir" id="upload_dir" value="/home/user/temp" />
  <button type="submit">upload</button>
  <button type="button" onclick='$("#upload_form").css("display", "none");'>hide</button>
  <div id="upload_dir2"></div>
</form>
<h2 class="top" id="location" style="margin-left:7%;margin-right:10%;"><%= @location %></h2>
<div id="pwd" style="margin-left:10%;"></div>
</td>
</tr>
<!-- row 2 -->
<tr>
<td colspan="2">
 <a href="/"><img src="img/home.png" alt="reload" /></a> <a href="#message"><img src="img/arrow_down.png" alt="" border="0" /></a> 
 locations: <select id="locations">
<%= @locations %>
</select>
 command: <input id="command" type="text" size="50" /><button id="exec" type="button">exec</button>
<button type="reset" onclick="javascript:$('#command').val('');">clear</button>
</td>
</tr>
<!-- row 3 -->
<tr>
<!-- row 3 , col 1 -->
<td style="width:140px;vertical-align:top;">
<br />
<img src="/img/window.png" alt="menu" /> menu<br />
<ul>
<li><a href="javascript:list_all=false;getContent($('#location').text());">list</a></li>
<li><a href="javascript:list_all=true;getContent($('#location').text());">list all</a></li>
<li><a href="javascript:getTree($('#location').text());">tree</a></li>
<li><a href="javascript:getScript();">script</a></li>
<li><a href="javascript:showBookmark();">bookmark</a></li>
<li><a href="javascript:showCache();">cache</a></li>
<li><a href="javascript:showUploadForm();">file upload</a></li>
<li><a href="javascript:showReferenceWindow();">refer ..</a></li>
<li><a href="/help.html" target="_blank">help</a></li>
</ul>
<%= @usermenu %>
</td>
<!-- row 3, col 2 -->
<td  style="vertical-align:top;"><div id="content">
<%= @content %>
<div></td>
</tr>
<!-- row 4 -->
<tr>
<td colspan="2">

<form id="form_save_text" name="form_save_text" method="post" action='javascript: saveText();'>
<a href="#top"><img id="top_button" src="/img/arrow_up.png" alt="top" /></a>&nbsp;
<a href="javascript:editText();"><img id="edit_button" src="/img/mini_edit.png" style="display:none;" /></a>&nbsp;
<a href="javascript:document.form_save_text.submit();"><img id="save_button" src="/img/save.png" style="display:none;" /></a>
<input type="hidden" name="edit_path" id="edit_path" value="" />
<textarea id="editor" name="editor" cols="100" rows="25" style="display:none;font-size:small;"></textarea>
</form>

<div id="message">
<a name="message"></a>
<%= @message %>
</div></td>
</tr>
</table>

</div>
<%
 if @title then
%>
<p style="margin-left:10px;padding:5px;"><a href="/"><img src="img/home.png" alt="reload" /></a> <a href="#top"><img src="img/arrow_up.png" alt="top" /></a> <%= @title + ", Sinatra " + VERSION + ", ruby " + RUBY_VERSION %></p>
<%
 end
%>
<p>&nbsp;</p>
<p>&nbsp;</p>
</body>
</html>



@@ form_script

<h4>Scripting</h4>
<form name="form_script" id="form_script" method="post" 
action="javascript:if ($('#open_window').attr('checked')) openScriptWindow(); else postScript();">
script: <label for="ruby">
<input type="checkbox" id="ruby" name="ruby" checked="checked" />ruby
</label>&nbsp;
<label for="open_window"><input type="checkbox" id="open_window" name="open_window" checked="checked" /> open window</label>&nbsp;
|&nbsp;<a href="javascript:scriptGallery();">Script Gallery</a>
<br />
params (JSON) : <input type="text" id="params_json" name="params_json" size="80" style="font-size:small;" />
<br />
<textarea id="script" name="script" cols="80" rows="15" style="font-size:small;"></textarea><br />
Save path (option): <input name="save_path" id="save_path" type="text" size="80" style="font-size:small;" />
<br />
<input type="button" value=" Load " onclick="javascript:loadScript();" />&nbsp;
<input type="submit" id="save_run" value=" Save & Run " />&nbsp;
<input type="reset" value=" Reset " />
<br />
<br />
</form>


@@ form_insert_info
<h4>Add file info</h4>
<form name="form_insert_info"id="form_insert_info" method="post" action="javascript:insert_info();" style="margin-left:5%;">
<table style="border-width:0px">
<tr><td style="border-width:0px">path</td><td style="border-width:0px"><input type="text" name="insert_path" id="insert_path" size="100" value="<%= @insert_path %>"  style="font-size:small;" /></td></tr>
<tr><td style="border-width:0px">info</td><td style="border-width:0px"><textarea name="insert_info" cols="80" rows="6" style="font-size:small;"></textarea></td></tr>
<tr><td style="border-width:0px">method</td><td style="border-width:0px"><textarea name="insert_method" cols="80" rows="6" style="font-size:small;"></textarea></td></tr>
<tr><td style="border-width:0px">icon</td><td style="border-width:0px"><input type="text" name="insert_icon" id="insert_icon" size="80"  style="font-size:small;" /></td></tr>
<tr><td style="border-width:0px">dir</td><td style="border-width:0px"><input type="checkbox" name="insert_dir" <%= @insert_dir %>/> check if directory</td></tr>
<tr><td style="border-width:0px">bin</td><td style="border-width:0px"><input type="checkbox" name="insert_bin" /> check if binary file</td></tr>
<tr><td style="border-width:0px">group</td><td style="border-width:0px"><input type="text" name="insert_group" id="insert_group" size="80" /></td></tr>
<tr><td style="border-width:0px"></td><td style="border-width:0px"></td></tr>
<tr><td style="border-width:0px"></td><td style="border-width:0px"><input type="submit" value="insert" /><input type="reset" value="reset" /></td></tr>
</table>
</form>


@@ form_select_info
<h4>Select info</h4>
<form name="form_select_info"id="form_select_info" method="post" action="javascript:select_info();" style="margin-left:5%;">
<table style="border-width:0px">
<tr><td style="border-width:0px">n</td><td style="border-width:0px"><input type="text" name="select_n" id="select_n" size="20" value=""  style="font-size:small;" /></td></tr>
<tr><td style="border-width:0px">path</td><td style="border-width:0px"><input type="text" name="select_path" id="select_path" size="100" value=""  style="font-size:small;" /></td></tr>
<tr><td style="border-width:0px">info</td><td style="border-width:0px"><input type="text" name="select_info" size="80" style="font-size:small;" /></td></tr>
<tr><td style="border-width:0px">method</td><td style="border-width:0px"><input type="text" name="select_method" size="80" style="font-size:small;" /></td></tr>
<tr><td style="border-width:0px">icon</td><td style="border-width:0px"><input type="text" name="select_icon" id="select_icon" size="80"  style="font-size:small;" /></td></tr>
<tr><td style="border-width:0px">dir</td><td style="border-width:0px"><input type="checkbox" name="select_dir" /> check if directory</td></tr>
<tr><td style="border-width:0px">bin</td><td style="border-width:0px"><input type="checkbox" name="select_bin" /> check if binary file</td></tr>
<tr><td style="border-width:0px">group</td><td style="border-width:0px"><input type="text" name="select_group" id="select_group" size="80" /></td></tr>
<tr><td style="border-width:0px"></td><td style="border-width:0px"></td></tr>
<tr><td style="border-width:0px"></td><td style="border-width:0px"><input type="submit" value="select" /><input type="reset" value="reset" /></td></tr>
</table>
</form>


@@ form_update_info
<h4>Update file info (n=<%= @update_n %>)</h4>
<form name="form_update_info"id="form_update_info" method="post" action="javascript:update_info();" style="margin-left:5%;margin-left:10px;">
<input type="hidden" name="n" value="<%= @update_n %>" />
<table style="border-width:0px">
<tr><td style="border-width:0px">path</td><td style="border-width:0px"><input type="text" name="path" id="path" size="100" value="<%= @update_path %>"  style="font-size:small;" /></td></tr>
<tr><td style="border-width:0px">info</td><td style="border-width:0px"><textarea name="info" cols="80" rows="6" style="font-size:small;"><%= @update_info %></textarea></td></tr>
<tr><td style="border-width:0px">method</td><td style="border-width:0px"><textarea name="method" cols="80" rows="6" style="font-size:small;"><%= @update_method %></textarea></td></tr>
<tr><td style="border-width:0px">icon</td><td style="border-width:0px"><input type="text" name="icon" id="update_icon" size="80"  style="font-size:small;" value="<%= @update_icon %>" /></td></tr>
<tr><td style="border-width:0px">dir</td><td style="border-width:0px"><input type="checkbox" name="dir" <%= @update_dir %> /> check if directory</td></tr>
<tr><td style="border-width:0px">bin</td><td style="border-width:0px"><input type="checkbox" name="bin"  <%= @update_bin %> /> check if binary file</td></tr>
<tr><td style="border-width:0px">group</td><td style="border-width:0px"><input type="text" name="group" id="update_group" size="80" value="<%= @update_group %>" /></td></tr>
<tr><td style="border-width:0px"></td><td style="border-width:0px"></td></tr>
<tr><td style="border-width:0px"></td><td style="border-width:0px"><input type="submit" value="update" /><input type="reset" value="reset" /></td></tr>
</table>
</form>



@@ file_upload

<!DOCTYPE html>
<html>
<head>
<title>file upload</title>
<style>
h2 {
  color: green;
  padding: 6px;
  text-align:center;
  border-style: solid;
  border-width: 1px;
  border-color: #33aa33;
  background-color: #d0f0d0;
}

a:link {
  color:green;
  text-decoration: none;
}

div.result {
  border: solid 1px gray;
  padding: 8px;
  background-color: #f0f0f0;
}
</style>
</head>
<body style="background-color: #e0f0d8; margin-left:5%;margin-right:5%;">
<h2>file upload</h2>
<p><a href="javascript:history.back();">[back]</a></p>
<div class="result"><%= @upload_result %></div>
<br />
</body>
</html>


@@ update_thumb

<form id="form_update_thumb" name="form_update_thumb" method="post" action="javascript:update_thumb();">
<input type="hidden" name="path" value="<%= @path %>" />
Icon or Thumbnail image: <input type="text" size="100" name="thumb" id="thumb" /><br />
<br />
<button type="submit" style="margin-left:15px;">submit</button>
<br />
</form>


@@ reference

<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>reference</title>
<link rel="stylesheet" type="text/css" href="<%= @stylesheet %>" />
<script type="text/javascript" src="/js/jquery-1.6.1.min.js"></script>
<script type="text/javascript" src="/js/base64.js"></script>
<script type="text/javascript">

function change_dir(dir) {
  var url = '/get_fullpath_nav/' + base64.encode(dir);
  $.get(url, function(data) {
    $('#content').html(data);
    $('#refer_dir').text(dir);
  });
}

$(document).ready(function() {
  var dir = $('#refer_dir').text();
  change_dir(dir);

  $("#locations").bind('change', function() {
    dir = $("#locations option:selected").text();
    change_dir(dir);
  });

});
</script>
</head>

<body>
<h1 id="refer_dir" class="top" style="font-size:16pt;"><%= @refer_dir %></h1>
locations: <select id="locations">
<%= @locations %>
</select>&nbsp;
<a href="javascript:window.close();">close</a>
<br />
<br />
<div id="content" style="background-color: snow;padding:5px;font-size:small;"></div>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
</body>
</html>
