# coding: utf-8

#
#  ファイラ 3.0 (Suruga)
#
require 'sinatra'
require 'fileutils'
require 'pathname'
require 'base64'
require 'sqlite3'
require "json/pure"
require "kconv"
require 'mylogger'
require "./files.rb"


Version = "3.0.2"

# ============================================================
#   メインページ 
# ============================================================
class Index
  enable :inline_templates

  # 動作環境がWindowsかどうか?
  if RUBY_PLATFORM.downcase =~ /mswin|mingw|cygwin|bccwin/ then
    Config = "config_win.ini"
    Locations = "locations_win.ini"
    UserMenu = "usermenu.html"
  else
    Config = "config.ini"
    Locations = "locations.ini"
    UserMenu = "usermenu.html"
  end

  #
  # config.iniファイルの読み込み
  #
  configure do
    @@start_dir = Dir.pwd()
    set :title, "Filer"
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
  end # configure


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
  end # template not found

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

  #
  #  ヘルパーメソッドの定義
  #  =======================
  helpers do
    # クライアントのIPアドレスをチェックする。
    def checkClient(ip)
      if settings.ip.nil? then
        regex_ip = /^192\.168\.\d+\.\d+/
      else
        regex_ip = settings.ip
      end
      return (ip == '127.0.0.1' or ip.match(regex_ip) != nil)
    end

    # 共通表示項目
    def set_common()
      @location = FileUtils.pwd()
      @locations = settings.bookmark
      @message = ""
      @title = settings.title + " " + Version
      @stylesheet = settings.stylesheet
      @usermenu = settings.usermenu
      @pwd = Dir.pwd()
    end

    # 属性 "r","w","x" を返す。
    def get_attr(path, mode=0)
      begin
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
      rescue
        str = " | ???"
      end
      return str
    end # get_attr

    # アイコンを返す。
    def get_icon(path)
      begin
        path.gsub!('//', '/')
        ext = File.extname(path).downcase()
        ret = ""
        case ext
        when '.txt','.ini','.cnf','.conf','.def','.log'
          ret = %!<a href="javascript:getMessage('/text/#{path}');"><img src="/img/mime_doc.png" alt="doc" border="0" /></a>\n!
        when '.pl','.php','.py','.rb','.c','.h','.cpp','.inc','.js','.cgi','.sh','.csh','.java'
          ret = %!<a href="javascript:getMessage('/text/#{path}');"><img src="/img/mime_doc.png" alt="doc" border="0" /></a>\n!
        when '.jpg','.png','.gif'
          ret = %!<a href="javascript:getMessage('/image/#{path}');"><img src="/img/mime_jpg.png" alt="img" border="0" /></a>\n!
        when '.html','.shtml'
          if settings.html then
            ret = %!<a href="javascript:getMessage('/markup/#{path}');"><img src="/img/mime_doc.png" alt="htm" border="0" /></a>\n!
          else
            ret = %!<a href="javascript:getMessage('/text/#{path}');"><img src="/img/mime_doc.png" alt="htm" border="0" /></a>\n!
          end
        when '.xml','.css','.xsl','.dtd','.xsd','.erb','.haml'
          ret = %!<a href="javascript:getMessage('/text/#{path}');"><img src="/img/mime_doc.png" alt="xml" border="0" /></a>\n!
        when '.swf'
          ret = %!<a href="javascript:getMessage('/flash/#{path}');"><img src="/img/mime_swf.png" alt="swf" border="0" /></a>\n!
        when '.svg'
          ret = %!<a href="javascript:getMessage('/svg/#{path}');"><img src="/img/mime_jpg.png" alt="svg" border="0" /></a>\n!
        when '.pdf'
          ret = %!<a href="javascript:getMessage('/pdf/#{path}');"><img src="/img/mime_doc.png" alt="pdf" border="0" /></a>\n!
        when '.mp3', '.ogg', '.wav'
          ret = %!<a href="javascript:getMessage('/audio/#{path}');"><img src="/img/mime_mp3.png" alt="aud" border="0" /></a>\n!
        when '.ogv', '.ogm', '.mp4', '.mov'
          ret = %!<a href="javascript:getMessage('/video/#{path}');"><img src="/img/mime_avi.png" alt="vid" border="0" /></a>\n!
        when '.zip', '.gz', '.tgz', '.7z', '.jar', '.lzh', '.rar'
          ret = %!<a href="javascript:getMessage('/zip/#{path}');"><img src="/img/mime_zip.png" alt="zip" border="0" /></a>\n!
        else
        end
      rescue
        ret = ""
      end
      return ret
    end # get_icon

    # ファイル管理データベースに登録されている項目ならアイコンを返す。
    def get_files_icon(path)
      row = @@filesdb.query_path(path)
      return "" if row.nil?
      str = %! <a href="javascript:show_file_info('#{path}');"><img src="/img/mini_warning.png" alt="@" /></a>!
      return str
    end

    # 指定したディレクトリの内容一覧を返す。
    #   dir: ディレクトリ
    #   all: 隠しファイルを含むかどうか
    #   info: ファイル情報アイコンを表示するかどうか（データベースを検索するかどうか）
    def getContent(dir, all=false, info=false)
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
        #p = Base64.encode64(path.parent.to_s)
        p = path.parent.to_s
        str += %!<li id="li1"><a href="/get_content/#{p}">[..]</a></li>\n! unless all
      end
      dirs = dir.tosjis
      items = Dir.entries(dirs)
      items.sort!
      i = 0
      i += 1 unless all
      items.each do |f|
        begin
          f = f.toutf8
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
            str += %!<li id="li#{i}"><a href="/get_content/#{abspath}">[#{f}]</a> #{attr}#{files_icon}</li>\n!
          else  # files
            icon = get_icon(abspath)
            attr = get_attr(abspath)
            files_icon = get_files_icon(abspath) if info
            str += %!<li id="li#{i}">#{icon} #{f}#{attr}#{files_icon}</li>\n!
          end
        rescue => e
          #MyLogger.logger(e.message)
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

  # ページがない時のエラーハンドラ　not found (404)
  not_found do
    erb :not_found
  end # not_found


  # ルートのハンドラ
  get '/' do
    set_common()
    @content = getContent('~')
    if checkClient(request.ip) then
      htm = erb(:index)
    else
      htm = "Client " + request.ip + " is not allowed."
    end
    return htm
  end # get '/'


  # 指定ディレクトリの内容一覧を返す。
  get '/get_content/*' do |dir|
    dir = dir.gsub('//', '/')
    set_common()
    @location = dir
    @content = getContent(dir)
    if checkClient(request.ip) then
      htm = erb(:index)
    else
      htm = "Client " + request.ip + " is not allowed."
    end
    return htm
  end # /get_content/*

  # テキストをpreで囲んだHTMLとして返す。
  get '/text/*' do |path|
    f = nil
    str = "<pre>\n"
    begin
      f = open(path)
      i = 0
      while f.gets() do
        str += escape_html($_)
        i += 1
        if i > 2000 then
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

  # 画像を返す
  get '/image/*' do |path|
    contentType = "image/" + File.extname(path).gsub!('.', '')
    contentType.gsub!(/jpg$/, 'jpeg')
    bindata = File.binread(path)
    content_type contentType
    return bindata
  end

  # SVGを返す。
  get '/svg/*' do |path|
    content_type "image/svg+xml"
    path = "/" + path unless path[0] == '/'
    bindata = File.binread(path)
    return bindata
  end

  # Flashを返す。
  get '/flash/*' do |path|
    content_type "application/x-shockwave-flash"
    path = "/" + path unless path[0] == '/'
    bindata = File.binread(path)
    return bindata
  end

  # 音声データを返す。
  get '/audio/*' do |path|
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

  # 動画データを返す。
  get '/video/*' do |path|
    path = "/" + path unless path[0] == '/'
    ext = File.extname(path)
    case ext
    when '.mp4'
      contentType = "video/mp4"
    when '.ogv'
      contentType = "video/ogg"
    when '.mov'
      contentType = "video/quicktime"
    when '.wmv'
      contentType = "video/x-ms-wmv"
    else
      contentType = "video/mpeg"
    end
    content_type contentType
    bindata = File.binread(path)
    return bindata
  end

  # PDFを返す。
  get '/pdf/*' do |path|
    content_type "application/pdf"
    path = "/" + path unless path[0] == '/'
    bindata = File.binread(path)
    return bindata
  end

  # マークアップされたテキストをそのまま返す。
  get '/markup/*' do |path|
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

  # バイナリーデータを返す。
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

  # コマンドを実行する。
  get '/command/*' do |cmd|
    result = "(null)"
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
        cmd.gsub!("/", "\\")
        result = `#{cmd}`
        if result.nil? or result == "" then
          result = "Done."
        end
      end
      result = escape_html(result)
    rescue => e
      result = e.message
    end
    result = result.toutf8
    return '<pre>' + result + '</pre>'
  end

  # スクリプト実行用フォームを返す。
  get '/form_script/' do
    erb :form_script
  end

  # スクリプト実行フォームを受け取り実行する。
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

  # ファイル参照ウィンドウの内容を返す。
  get '/reference/*' do |dir|
    @refer_dir = dir
    @stylesheet = settings.stylesheet
    @locations = settings.bookmark
    erb :reference
  end

  # ファイル参照ウィンドウの内容を返す。
  get '/get_fullpath_nav/*' do |dir|
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
      f.gsub!('//', '/')
      if test(?d, f) then
        buff << %!<a href="javascript:change_dir('#{f}');"><img src="/img/folder_down.png" alt="dir" style="border-width:0px;" /></a> !
      end
      buff << (f + "<br />\n")
    end
    return buff
  end

  # ファイルアップロード
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

# == クラスの終わり ==
end # class Index



# == インライン・テンプレート ==
__END__

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
  var url = '/get_fullpath_nav/' + dir;
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

