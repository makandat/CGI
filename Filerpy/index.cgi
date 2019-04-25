#!/usr/bin/env python3
#  Filerpy index.cgi  v1.01 2019-04-23
from WebPage import WebPage
import os
import FileSystem as fs
import Text
import Common

VERSION = "1.0"

# ウェブページ (Filerpy index.cgi)
class FilerPage(WebPage) :
  # コンストラクタ
  def __init__(self, template="") :
    super().__init__(template)
    #Common.init_logger('/var/www/data/Logger.log')
    self.setPlaceHolder('title', 'Filerpy <span style="color:navy;font-size:20pt;">linux v' + VERSION + '</span>')
    self.setPlaceHolder('message', '')
    # AppConf.ini のデータを得る。
    self.home = self.conf['home']
    sp = self.conf['places']
    self.places = sp.split(':')
    self.texts = self.conf['text'].split(':')
    self.images = self.conf['image'].split(':')
    self.audio = self.conf['audio'].split(':')
    self.video = self.conf['video'].split(':')
    self.pdf = self.conf['pdf']
    self.zips = self.conf['zip'].split(':')
    # プレースホルダ places を決める。
    self.setPlaces()
    # 表示設定のデフォルト値
    # self.hiddenfile, self.orderby, self.reverse を初期化する。
    self.getFilter()
    # self.current_folder を初期化する。
    self.getCurrentFolder()
    # ポストバックか?
    if self.isParam("place") :
      # SELECT の選択項目を表示する。
      self.showFavPlace()
    elif self.isParam("folder") :
      # パラメータで指定されたフォルダを表示する。
      folder = self.getParam('folder')
      self.showFolder(folder)
    elif self.isParam('filter') :
      # 表示設定
      self.setFilter()
    else :
      # ホームディレクトリを表示
      self.showFolder(self.home)
    return


  # お気に入りのディレクトリを表示 (SELECT 選択項目)
  def showFavPlace(self) :
    favfolder = self.getParam('place')
    self.setCookie('current_folder', favfolder)
    self.current_folder = favfolder
    self.setPlaceHolder('folder', favfolder)
    self.listFolder(favfolder, sortby=self.orderby, order=self.reverse)
    return

  # 指定されたディレクトリを表示
  def showFolder(self, folder) :
    if folder == "" :
      # 空欄ならホームディレクトリ
      folder = self.home;
    elif folder == ".." :
      # ".." なら上のディレクトリ
      folder = fs.getParentDirectory(self.current_folder)
    elif folder.startswith('~') :
      # "~" で始まっていたらホームディレクトリに置き換える。
      folder = folder.replace('~', self.home)
    else :
      pass
    self.setCookie('current_folder', folder)
    self.current_folder = folder
    self.setPlaceHolder('folder', folder)
    self.listFolder(folder, sortby=self.orderby, order=self.reverse)
    return

  # 「表示設定」を適用する。
  def setFilter(self) :
    self.setPlaceHolder('folder', self.current_folder)
    # 隠しファイルの表示
    if self.isParam('hiddenfile') :
      hiddenfile = self.getParam('hiddenfile')
      if hiddenfile == 'hide' :
        # 表示しない
        self.hiddenfile = True
      else :
        # 表示する
        self.hiddenfile = False
    # 表示順
    self.orderby = self.getParam('orderby')
    # 並び順
    self.reverse = self.getParam('reverse')
    # クッキーに保存
    if self.hiddenfile :
      self.setCookie('hiddenfile', '1')  # 隠しファイルを表示しない。
    else :
      self.setCookie('hiddenfile', '0')  # 隠しファイルを表示する。
    self.setCookie('orderby', self.orderby)
    self.setCookie('reverse', self.reverse)
    # 現在のフォルダを表示
    if self.isCookie('current_folder') :
      self.current_folder = self.getCookie('current_folder')
    else :
      self.current_folder = self.home
    self.listFolder(self.current_folder, sortby=self.orderby, order=self.reverse)
    return
    
  # プレースホルダ places を決める。
  def setPlaces(self) :
    places = "<option>-</option>\n"
    places += f"<option>{self.home}</option>\n"
    for p in self.places :
      places += f"<option>{p}</option>\n"
    self.setPlaceHolder("places", places)
    return

  # 指定されたフォルダの内容を表示する。
  def listFolder(self, folder, sortby="name", order="asc") :
    buff = "<tr><th>番号(id)</th><th>種別</th><th>名称</th><th>モード</th><th>バイト数</th><th>最終更新日時</th><th>所有者</th><th>グループ</th><th>リンク先</th></tr>\n"
    # ディレクトリ一覧
    dirs = fs.listDirectories(folder)
    dirlist = self.makeFileList(dirs, True)
    sdirlist = self.sortlist(dirlist, sortby, order)
    # HTML テーブルに変換
    count = 0
    for li in sdirlist :
      count += 1
      fname = WebPage.stripTag(li[2])
      sibling = self.current_folder + "/" + fname
      li[0] = f"<a href=\"javascript:push('{sibling}')\">{count}</a>"
      buff += WebPage.table_row(li) + "\n"
    # ファイル一覧一覧
    files = fs.listFiles(folder)
    filelist = self.makeFileList(files, False)
    sfilelist = self.sortlist(filelist, sortby, order)
    # HTML テーブルに変換
    for li in sfilelist :
      count += 1
      fname = WebPage.stripTag(li[2])
      sibling = self.current_folder + "/" + fname
      li[0] = f"<a href=\"javascript:push('{sibling}')\">{count}</a>"
      buff += WebPage.table_row(li) + "\n"
    # content を設定
    self.setPlaceHolder('content', WebPage.tag("table", buff))
    if len(files) + len(dirs) == 0 :
      self.setPlaceHolder('message', '空のディレクトリです。')
    return

  # クッキーの表示フィルタを得る。(self.hiddenfile, self.orderby, self.reverse)
  def getFilter(self) :
    if self.isCookie('hiddenfile') :
      if self.getCookie('hiddenfile') == '1' :
        # 隠しファイルを表示しない
        self.hiddenfile = True
        self.setCookie('hiddenfile', '1')
      else :
        # 隠しファイルを表示する。
        self.hiddenfile = False
        self.setCookie('hiddenfile', '0')
    else :
      self.hiddenfile = False
      self.setCookie('hiddenfile', '0')
    # 表示順項目
    if self.isCookie('orderby') :
      self.orderby = self.getCookie('orderby')
    else :
      self.orderby = 'name'
      self.setCookie('orderby', 'name')
    # 並び順
    if self.isCookie('reverse') :
      self.reverse = self.getCookie('reverse')
    else :
      self.reverse = 'asc'
      self.setCookie('reverse', 'asc')
    return

  # 現在のフォルダを得る。
  def getCurrentFolder(self) :
    if self.isCookie('current_folder') :
      self.current_folder = self.getCookie('current_folder')
    else :
      self.current_folder = self.home
      self.setCookie('current_folder', self.home)
    return

  # ファイルまたはディレクトリの属性を含むリストを作成する。
  def makeFileList(self, files:list, dir = False) -> list:
    flist = []  # 表
    count = 0   # カウント(id) 初期化
    t = 'd' if dir else 'f'
    for f in files :
      # 隠しファイルをどうするか
      fname = fs.getThisDirectory(f)  # 2. file/dir name
      if self.hiddenfile and fname.startswith('.'):
        # 表示しない
        continue
      fdef = []  # 行
      count += 1  # count
      fname = fs.getThisDirectory(f)
      sibling = self.current_folder + "/" + fname
      lid = f"<a href=\"javascript:push('{sibling}')\">{count}</a>"
      fdef.append(lid)  # 0. id link  (仮に入れておく。ソート後再設定)
      if fs.isLink(f) :
        fdef.append('l' + t)  # 1. link
      else :
        fdef.append(t)  # 1. non link
      # 2. file/dir name
      if dir :
        lfname = f"<a href=\"index.cgi?folder={sibling}\">{fname}</a>"
        fdef.append(lfname)
      else :
        lfname = self.makeLink(fname)
        fdef.append(lfname)
      mode = "{:08o}".format(fs.getAttr(f))  # 3. mode
      fdef.append(mode)
      if dir :
        size = "0"  # 4. size
      else :
        size = fs.getFileSize(f)  # 4. size
      fdef.append(str(size))
      lastwrite = fs.getLastWrite(f)  # 5. time
      fdef.append(lastwrite)
      owner = fs.getOwner(f)  # 6. owner
      fdef.append(owner)
      group = fs.getGroup(f)  # 7. group
      fdef.append(group)
      if fs.isLink(f) :
        ldest = fs.getLinkedPath(f)  # 8. symbolic link
        fdef.append(ldest)
      else :
        fdef.append("")
      #  行(fdef)を表(flist)に追加する。
      flist.append(fdef)
    return flist


  # ディレクトリ・ファイル一覧を並べ替え処理
  def sortlist(self, dflist:list, sortby="name", order="asc") -> list:
    if sortby == 'name' :
      n = 2
    elif sortby == 'size' :
      n = 4
    elif sortby == 'time' :
      n = 5
    else :
      n = 0
    if order == "desc" :
      result = sorted(dflist, key=lambda x: x[n], reverse=True)
    else :
      result = sorted(dflist, key=lambda x: x[n])
    return result


  # テキストファイル表示のためのリンクを作る。
  def makeLink(self, fname) :
    ext = fs.getExtension(fname)
    if ext == "" :
      return fname
    ext = Text.tolower(Text.substring(ext, 1))
    path = self.current_folder + "/" + fname
    if ext in self.texts :
      link = f"<a href=\"showText.cgi?path={path}\" target=\"_blank\">{fname}</a>"
    elif ext in self.images :
      link = f"<a href=\"getImage.cgi?path={path}\" target=\"_blank\">{fname}</a>"
    elif ext in self.pdf :
      link = f"<a href=\"getPDF.cgi?path={path}\" target=\"_blank\">{fname}</a>"
    else :
      link = fname
    return link



# プログラムの開始
wp = FilerPage('templates/index.html')
wp.echo()
