/* FileSystem.js */
'use strict';
const fs = require('fs');
const path = require('path');
const os = require('os');


/* (ローカル関数) ext が配列 exts の要素に含まれていれば true、そうでなければ false を返す。*/
function testExtension(ext, exts) {
  for (let i = 0; i < exts.length; i++) {
    if (exts[i] == ext)
      return true;
  }

  return false;
}


/* フォルダ内のファイル一覧を得る。*/
/*  dir は対象のディレクトリ */
/*  exts は拡張子一覧(配列)  (例) ['.jpg', '.jpeg', '.JPG', '.JPEG'] */
/*  callback はファイルパスの一覧(配列)を受け取るコールバック関数 */
exports.getFiles = async (dir, exts, callback) => {
  let files = [];
  let prom_items = await fs.promises.readdir(dir, {'withFileTypes': true});
  for (let item of prom_items) {
    let ext = path.extname(item.name);
    if (item.isFile() && testExtension(ext, exts)) {
      files.push(path.join(dir, item.name));
    }
  }
  callback(files);
}

/* フォルダ内のサブディレクトリ一覧を得る。*/
/*  dir は対象のディレクトリ */
/*  callback はディレクトリパスの一覧(配列)を受け取るコールバック関数 */
exports.getDirectories = async (dir, callback) => {
  let dirs = [];
  let prom_items = await fs.promises.readdir(dir, {'withFileTypes': true});
  for (let item of prom_items) {
    if (item.isDirectory()) {
      dirs.push(path.join(dir, item.name));
    }
  }
  callback(dirs);
}

/* パスがディレクトリか判別する。*/
/*   callback はブール値を受け取るコールバック関数 */
exports.isDir = async (path, callback) => {
  let prom_stat = await fs.promises.stat(path);
  callback(prom_stat.isDirectory());
}

/* パスがファイルか判別する。*/
/*   callback はブール値を受け取るコールバック関数 */
exports.isFile = async (path, callback) => {
  let prom_stat = await fs.promises.stat(path);
  callback(prom_stat.isFile());  
}

/* パスが存在するか判別する。*/
exports.exists = (path) => {
  let b = true;
  try {
    fs.accessSync(path);
  }
  catch (e) {
    b = false
  }
  return b;
}

/* ファイルサイズを得る。*/
/*   callback はファイルサイズを受け取るコールバック関数 */
exports.getSize = async (path, callback) => {
  let prom_stat = await fs.promises.stat(path);
  callback(prom_stat.size);    
}

/* ファイル・ディレクトリの更新日時を得る。*/
/*   callback は更新日時を受け取るコールバック関数 */
/*   optstr は false なら Date 型で、true なら String で結果を返す。*/
exports.getDateTime = async (path, callback, optstr = false) => {
  let prom_stat = await fs.promises.stat(path);
  let time = prom_stat.mtime; 
  if (optstr) {
    let sdate = `${time.getFullYear()}-${(time.getMonth()+1).toString().padStart(2, '0')}-${time.getDate().toString().padStart(2, '0')}`;
    let stime = `${time.getHours().toString().padStart(2, '0')}-${time.getMinutes().toString().padStart(2, '0')}-${time.getSeconds().toString().padStart(2, '0')}`;
    callback(sdate + " " + stime);
  }
  else {
    callback(time);
  }
}

/* パスの拡張子を得る。同期関数 */
exports.getExtension = (p) =>{
  return path.extname(p);
}

/* パスのディレクトリ部分を得る。同期関数 */
exports.getDirectory = (p) => {
  return path.dirname(p);
}

/* パスのファイル部分を得る。同期関数 */
exports.getFileName = (p) => {
  return path.basename(p);
}


/* ホームディレクトリ 同期関数 */
exports.getHome = () => {
  return os.homedir();
}

/* 一時ディレクトリ 同期関数 */
exports.getTemp = () => {
  return os.tmpdir();
}
