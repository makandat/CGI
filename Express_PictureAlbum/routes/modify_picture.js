/* modify_picture.js */
var express = require('express');
var mysql = require('./MySQL.js');
var fs = require('fs');
var os = require('os');
var router = express.Router();
const PAGE_TITLE = "画像の追加・修正 (PictureAlbum)";

/* id の最大値を得る。*/
function getMaxId() {
  return new Promise((resolve=>{
    mysql.getValue("SELECT max(id) FROM PictureAlbum", (mid) => {
      resolve(mid);
    });
  }));
}

/* ファイルが存在するか確認する。*/
function fileExists(path) {
  return new Promise((resolve, reject) => {
    fs.stat(path, (err, stats) => {
      if (err) {
        reject(err);
      }
      else {
        resolve(stats.isFile());
      }
    });
  });
}

/* フォームデータをテーブルに挿入する。*/
async function insertData(req, res) {
  let message;
  let album = req.body.album;
  if (album == "" || parseInt(album) <= 0) {
    message = `データの挿入に失敗しました。アルバム番号は 1 以上です (album=0)。`;
    res.render('showInfo', {'title':'エラー', 'message':message, 'icon':'cancel.png', 'link':null});
    return;
  }
  let name = req.body.name.replace(/'/g, "''").trim();
  if (name == "") {
    message = `データの挿入に失敗しました。タイトルは空欄ではいけません。`;
    res.render('showInfo', {'title':'エラー', 'message':message, 'icon':'cancel.png', 'link':null});
    return;
  }
  let creator = req.body.creator.replace(/'/g, "''").trim();
  if (creator == "") {
    message = `データの挿入に失敗しました。作者は空欄ではいけません。`;
    res.render('showInfo', {'title':'エラー', 'message':message, 'icon':'cancel.png', 'link':null});
    return;
  }
  let path = req.body.path;
  let b = await fileExists(path);
  if (b == false) {
    message = `データの挿入に失敗しました。パスはファイルでなければなりません。`;
    res.render('showInfo', {'title':'エラー', 'message':message, 'icon':'cancel.png', 'link':null});
    return;
  }
  if (os.platform() == "win32") {
    path = path.replace(/\\/g, '/');
  }
  path = path.replace(/'/g, "''").trim();
  if (path.includes('#') || path.includes('&')) {
    res.render('showInfo', {'title':'エラー', 'message':'# や & がパスに含まれていますが使用できません。パス名を変更してください。', 'icon':'cancel.png', 'link':null});
    return;
  }
  let info = req.body.info.replace(/'/g, "''");
  let fav = req.body.fav;
  if (fav == "") {
    message = `データの挿入に失敗しました。「好き」は非負の整数でなければなりません。`;
    res.render('showInfo', {'title':'エラー', 'message':message, 'icon':'cancel.png', 'link':null});
    return;
  }
  let bindata = req.body.bindata;
  if (bindata == "") {
    message = `データの挿入に失敗しました。「イメージリンク」は非負の整数でなければなりません。`;
    res.render('showInfo', {'title':'エラー', 'message':message, 'icon':'cancel.png', 'link':null});
    return;
  }
  let picturesid = req.body.picturesid;
  if (picturesid == "") {
    message = `データの挿入に失敗しました。「Pictures ID」は非負の整数でなければなりません。`;
    res.render('showInfo', {'title':'エラー', 'message':message, 'icon':'cancel.png', 'link':null});
    return;
  }
  if (isNaN(parseInt(album))) {
    message = `データの挿入に失敗しました。アルバム番号が不正です。`;
    res.render('showInfo', {'title':'エラー', 'message':message, 'icon':'cancel.png', 'link':null});
  }
  else if (isNaN(parseInt(fav))) {
    message = `データの挿入に失敗しました。「好き」が不正です。`;
    res.render('showInfo', {'title':'エラー', 'message':message, 'icon':'cancel.png', 'link':null});
  }
  else {
    let id = await getMaxId();
    message = `データの挿入に成功しました。id = ${id+1}`;
    let sql = `INSERT INTO PictureAlbum(album, title, path, creator, info, fav, bindata, picturesid, date, sn) VALUES(${album}, '${name}', '${path}', '${creator}', '${info}', ${fav}, ${bindata}, ${picturesid}, CURRENT_DATE(), user.NextPictureAlbumSN())`;
    mysql.execute(sql, function() {
      res.render("modify_picture", {"title": PAGE_TITLE, "message": message, "id": "", "album": album, "name": name, "creator": creator, "path": path,
      "info": info, "fav": fav, "bindata": bindata, "picturesid": picturesid});
    });
  }
}

/* フォームデータでテーブルを更新する。*/
async function updateData(req, res) {
  let message;
  let id = req.body.id;
  let album = req.body.album;
  if (album == "" || parseInt(album) <= 0) {
    message = `データの更新に失敗しました。アルバム番号は 1 以上です。`;
    res.render('showInfo', {'title':'エラー', 'message':message, 'icon':'cancel.png', 'link':null});
    return;
  }
  let name = req.body.name.replace(/'/g, "''").trim();
  if (name == "") {
    message = `データの更新に失敗しました。タイトルは空欄ではいけません。`;
    res.render('showInfo', {'title':'エラー', 'message':message, 'icon':'cancel.png', 'link':null});
    return;
  }
  let creator = req.body.creator.replace(/'/g, "''").trim();
  if (name == "") {
    message = `データの更新に失敗しました。作者は空欄ではいけません。`;
    res.render('showInfo', {'title':'エラー', 'message':message, 'icon':'cancel.png', 'link':null});
    return;
  }
  let path = req.body.path;
  let b = await fileExists(path);
  if (b == false) {
    message = `データの更新に失敗しました。パスはファイルでなければなりません。`;
    res.render('showInfo', {'title':'エラー', 'message':message, 'icon':'cancel.png', 'link':null});
    return;
  }
  if (os.platform() == "win32") {
    path = path.replace(/\\/g, "/");
  }
  path = path.replace(/'/g, "''").trim();
  let info = req.body.info.replace(/'/g, "''");
  let fav = req.body.fav;
  let bindata = req.body.bindata;
  let picturesid = req.body.picturesid;
  if (isNaN(parseInt(id))) {
    message = `データの更新に失敗しました。id が不正です。`;
    res.render('showInfo', {'title':'エラー', 'message':message, 'icon':'cancel.png', 'link':null});
  }
  else if (isNaN(parseInt(album))) {
    message = `データの更新に失敗しました。アルバム番号が不正です。`;
    res.render('showInfo', {'title':'エラー', 'message':message, 'icon':'cancel.png', 'link':null});
  }
  else if (isNaN(parseInt(fav))) {
    message = `データの更新に失敗しました。「好き」が不正です。`;
    res.render('showInfo', {'title':'エラー', 'message':message, 'icon':'cancel.png', 'link':null});
  }
  else {
    message = `データの更新に成功しました。id = ${id}`;
    if (!picturesid) {
      picturesid = 0;
    }
    if (!bindata) {
      bindata = 0;
    }
    if (!fav) {
      fav = 0;
    }
    let sql = `UPDATE PictureAlbum SET album=${album}, title='${name}', creator='${creator}', path='${path}', info='${info}', bindata=${bindata}, picturesid=${picturesid}, \`date\`=CURRENT_DATE() WHERE id=${id}`;
    mysql.execute(sql, function() {
      res.render("modify_picture", {"title": PAGE_TITLE, "message": message, "id": id, "album": album, "name": name, "creator": creator, "path": path, "info": info,
        "fav": fav, "bindata": bindata, "picturesid": picturesid});
    });
  }
}

/* Pictures ID を取得する。*/
function getPicturesID(id) {
  return new Promise((resolve) => {
    mysql.getValue("SELECT p.id FROM PictureAlbum a, Pictures p WHERE INSTR(a.path, p.path) AND a.id=" + id, (pid) => {
        resolve(pid.toString());
    });
  });
}

/* データ確認 */
async function confirmData(req, res) {
  let id = req.params.id;
  if (id == undefined) {
    res.render("modify_picture", {"title": PAGE_TITLE, "message": "エラー： id が空欄です。", "id": "", "album": "", "info": "", "fav": 0, "bindata": 0, "picturesid": 0});
  }
  else {
    let picturesId = await getPicturesID(id);
    let sql = `SELECT * FROM PictureAlbum WHERE id=${id}`;
    mysql.getRow(sql, function(row, fields) {
      res.render("modify_picture", {"title": PAGE_TITLE, "message": "データを取得しました。", "id": row.id, "album": row.album, "name": row.title, "path": row.path, "creator": row.creator, "mark": row.mark,
      "info": row.info, "fav": row.fav, "bindata": row.bindata, "picturesid": picturesId});
    });
  }
}

/* ハンドラ */
/*  デフォルトのハンドラ */
router.get('/', function(req, res, next) {
  if (req.query.id) {
    mysql.getRow(`SELECT * FROM PictureAlbum WHERE id=${req.query.id}`, (row) => {
      res.render("modify_picture", {"title": PAGE_TITLE, "message": "", "id": row.id, "album": row.album, "name": row.title, "creator": row.creator, "path": row.path, "mark": row.mark, "info": row.info, "fav": row.fav, "bindata": row.bindata, "picturesid":row.picturesid});
    });
  }
  else {
    res.render("modify_picture", {"title": PAGE_TITLE, "message": "", "id": "", "album": 0, "name": "", "creator":"", "path": "", "mark": "", "info": "", "fav": 0, "bindata": 0, "picturesid":0});
  }
});

/* フォームデータを受け取る。*/
router.post("/", function(req, res, next) {
  let id = req.body.id;
  if (id == "") {
    // 挿入
    insertData(req, res).catch(e => res.render('showInfo', {'title':'エラー', 'message':e.message, 'icon':'cancel.png', link:null}));
  }
  else {
    // 更新
    updateData(req, res).catch(e => res.render('showInfo', {'title':'エラー', 'message':e.message, 'icon':'cancel.png', link:null}));
  }
});

/* データ確認 */
router.get('/confirm/:id', function(req, res, next) {
  let id = req.params.id;
  confirmData(req, res);
});


/* エクスポート */
module.exports = router;
