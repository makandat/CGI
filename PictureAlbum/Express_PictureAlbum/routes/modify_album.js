/* modify_album.js */
var express = require('express');
var mysql = require('./MySQL.js');
var router = express.Router();

/* フォームデータをAlbumテーブルに挿入する。*/
function insertData(req, res) {
  let name = req.body.album;
  let info = req.body.info.replace(/'/g, "''");
  let bindata = req.body.bindata;
  let mark = req.body.mark;
  let groupname = req.body.groupname.replace(/'/g, "''");
  let message = "データの挿入に成功しました。(" + name + ")";
  let sql = `INSERT INTO Album VALUES(NULL, '${name}', '${mark}', '${info}', ${bindata}, '${groupname}', CURRENT_DATE())`;
  mysql.execute(sql, function() {
    res.render("modify_album", {"title": "アルバムの作成・修正", "message": message, "id": "", "album": name, "mark":mark, "info": info, "bindata": bindata, "groupname": groupname});
  });
}

/* フォームデータでAlbumテーブルを更新する。*/
function updateData(req, res) {
  let id = req.body.id;
  let name = req.body.album;
  let mark = req.body.mark;
  let info = req.body.info.replace(/'/g, "''");
  let bindata = req.body.bindata ? req.body.bindata : 0;
  let groupname = req.body.groupname.replace(/'/g, "''");
  let message = `データの更新に成功しました。id = ${id}: ${name}`;
  let sql = `UPDATE Album SET name='${name}', info='${info}', mark='${mark}', bindata=${bindata}, groupname='${groupname}', \`date\`=CURRENT_DATE() WHERE id=${id}`;
  mysql.execute(sql, function() {
    res.render("modify_album", {"title": "アルバムの作成・修正", "message": message, "id": id, "album": name, "mark":mark, "info": info, "bindata": bindata, "groupname": groupname});
  });
}

/* データ確認 */
function confirmData(req, res) {
  let id = req.params.id;
  if (id == undefined) {
    res.render("modify_album", {"title": "アルバムの作成・修正", "message": "エラー： id が空欄です。", "id": "", "album": "", "info": "", "bindata": 0, "groupname": ""});
  }
  else {
    let sql = `SELECT * FROM Album WHERE id=${id}`;
    mysql.getRow(sql, function(row, fields) {
      res.render("modify_album", {"title": "アルバムの作成・修正", "message": "データを取得しました。", "id": row.id, "album": row.name, "mark":row.mark, "info": row.info, "bindata": row.bindata, "groupname": row.groupname});
    });
  }
}




/* ハンドラ */
/* フォームを表示する。 */
router.get('/', function(req, res, next) {
  let mark = "picture";
  if (req.query.mark != undefined) {
    mark = req.query.mark;
  }
  if (req.query.id) {
    let sql = `SELECT * FROM Album WHERE id = ${req.query.id}`;
    mysql.getRow(sql, (row) => {
      res.render("modify_album", {"title": "アルバムの作成・修正", "message": "", "id": row.id, "album": row.name, "mark": row.mark, "info": row.info, "bindata": row.bindata, "groupname": row.groupname});
    });
  }
  else {
    res.render("modify_album", {"title": "アルバムの作成・修正", "message": "", "id": "", "album": "", "mark":mark, "info": "", "bindata":0, "groupname": ""});
  }
});

/* フォームデータを受け取る。*/
router.post("/", function(req, res, next) {
  let id = req.body.id;
  if (id == "") {
    // 挿入
    insertData(req, res);
  }
  else {
    // 更新
    updateData(req, res);
  }
});

/* データ確認 */
router.get('/confirm/:id', function(req, res, next) {
  let id = req.params.id;
  confirmData(req, res);
});

/* エクスポート */
module.exports = router;
