/* modify_folders.js */
var express = require('express');
var os = require('os');
var fs = require('fs');
var mysql = require('./MySQL.js');
var router = express.Router();
const PAGE_TITLE = "画像フォルダの追加・修正";

/* ファイルが存在するか確認する。*/
function dirExists(path) {
  return new Promise((resolve, reject) => {
    fs.stat(path, (err, stats) => {
      if (err) {
        reject(err);
      }
      else {
        resolve(stats.isDirectory());
      }
    });
  });
}

/* Pictures テーブルの次の sn を得る。*/
function getNextSN() {
  return new Promise((resolve) => {
    mysql.getValue("SELECT (max(sn)+1) AS nextSn FROM Pictures", (n) => {
      resolve(n);
    });
  });
}

/* Pictures テーブルにすでに登録済みかチェックする。*/
function checkPath(path) {
  return new Promise((resolve) => {
    mysql.getValue("SELECT count(path) AS pathcount FROM Pictures WHERE path= '" + path + "'", (n) => {
      resolve(n);
    });
  });
}

/* フォームデータをテーブルに挿入する。*/
async function insertData(req, res) {
  let name = req.body.name.replace(/'/g, "''").trim();
  if (name == "") {
    res.render('showInfo', {'title':'エラー', 'message':'名称が空欄です。', 'icon':'cancel.png', 'link':null});
    return;
  }
  let creator = req.body.creator.replace(/'/g, "''");
  if (creator == "") {
    res.render('showInfo', {'title':'エラー', 'message':'作者が空欄です。', 'icon':'cancel.png', 'link':null});
    return;
  }
  let mark = req.body.mark;
  let b = await dirExists(req.body.path);
  if (! b) {
    res.render('showInfo', {'title':'エラー', 'message':'指定したディレクトリは存在しません。', 'icon':'cancel.png', 'link':null})
    return;
  }
  let path = req.body.path;
  if (path.includes('#') || path.includes('&')) {
    res.render('showInfo', {'title':'エラー', 'message':'# や & がパスに含まれていますが使用できません。パス名を変更してください。', 'icon':'cancel.png', 'link':null});
    return;
  }
  if (os.platform() == "win32") {
    path = path.replace(/\\/g, '/');
  }
  let countpath = await checkPath(path);
  if (countpath > 0) {
    res.render('showInfo', {'title':'エラー', 'message':'指定したディレクトリは登録済みです。', 'icon':'cancel.png', 'link':null})
    return;
  }
  path = path.replace(/'/g, "''").trim();
  let info = req.body.info.replace(/'/g, "''");
  let fav = req.body.fav;
  let bindata = req.body.bindata;
  let sn = await getNextSN();
  let message = "データの挿入に成功しました。(" + name + ")";
  let sql = `INSERT INTO Pictures(title, creator, path, mark, info, fav, count, bindata, date, sn) VALUES('${name}', '${creator}', '${path}', '${mark}', '${info}', 0, 0, ${bindata}, CURRENT_DATE(), ${sn})`;
  mysql.execute(sql, () => {
    mysql.getValue("SELECT max(id) FROM Pictures", (maxId) => {
      switch (mark) {
        case "HCG":
          mysql.execute(`CALL InsertPictHcg(${maxId})`, (c) => {
            if (c == null) {
              res.render("modify_folder", {"title": PAGE_TITLE, "message": message, "id": "", "name": name, "creator": creator, "path": path, "mark": mark, "info": info, "fav": 0, "count": 0, "bindata": bindata});
            }
            else {
              res.render('showInfo', {'title':'エラー', 'message':sql, 'icon':'cancel.png', 'link':null});
            }
          });
          break;
        case "DOUJIN":
          mysql.execute(`CALL InsertPictDoujin(${maxId})`, (c) => {
            if (c == null) {
              res.render("modify_folder", {"title": PAGE_TITLE, "message": message, "id": "", "name": name, "creator": creator, "path": path, "mark": mark, "info": info, "fav": 0, "count": 0, "bindata": bindata});
            }
            else {
              res.render('showInfo', {'title':'エラー', 'message':sql, 'icon':'cancel.png', 'link':null});
            }
          });
          break;
        case "MANGA":
          mysql.execute(`CALL InsertPictManga(${maxId})`, (c) => {
            if (c == null) {
              res.render("modify_folder", {"title": PAGE_TITLE, "message": message, "id": "", "name": name, "creator": creator, "path": path, "mark": mark, "info": info, "fav": 0, "count": 0, "bindata": bindata});
            }
            else {
              res.render('showInfo', {'title':'エラー', 'message':sql, 'icon':'cancel.png', 'link':null});
            }
          });
          break;
        case "PIXIV":
          mysql.execute(`CALL InsertPictPixiv(${maxId})`, (c) => {
            if (c == null) {
              res.render("modify_folder", {"title": PAGE_TITLE, "message": message, "id": "", "name": name, "creator": creator, "path": path, "mark": mark, "info": info, "fav": 0, "count": 0, "bindata": bindata});
            }
            else {
              res.render('showInfo', {'title':'エラー', 'message':sql, 'icon':'cancel.png', 'link':null});
            }
          });
          break;
        case "PHOTO":
          mysql.execute(`CALL InsertPictPhoto(${maxId})`, (c) => {
            if (c == null) {
              res.render("modify_folder", {"title": PAGE_TITLE, "message": message, "id": "", "name": name, "creator": creator, "path": path, "mark": mark, "info": info, "fav": 0, "count": 0, "bindata": bindata});
            }
            else {
              res.render('showInfo', {'title':'エラー', 'message':sql, 'icon':'cancel.png', 'link':null});
            }
          });
          break;
        default:
          res.render("modify_folder", {"title": PAGE_TITLE, "message": message, "id": "", "name": name, "creator": creator, "path": path, "mark": mark, "info": info, "fav": 0, "count": 0, "bindata": bindata});
          break;
        }
    });
  });
}

/* フォームデータでテーブルを更新する。*/
async function updateData(req, res) {
  let id = req.body.id;
  let name = req.body.name.replace(/'/g, "''").trim();
  let creator = req.body.creator.replace(/'/g, "''");
  let b = await dirExists(req.body.path);
  if (! b) {
    res.render('showInfo', {'title':'エラー', 'message':'指定したディレクトリは存在しません。', 'icon':'cancel.png', 'link':null})
    return;
  }
  let path = req.body.path;
  if (os.platform() == "win32") {
    path = path.replace(/\\/g, '/');
  }
  path = path.replace(/'/g, "''").trim();
  let mark = req.body.mark;
  let info = req.body.info.replace(/'/g, "''");
  let fav = req.body.fav ? req.body.fav : 0;
  let count = req.body.count ? req.body.count : 0;
  let bindata = req.body.bindata ? req.body.bindata : 0;
  let message = `データの更新に成功しました。id = ${id}`;
  let sql = `UPDATE Pictures SET title='${name}', creator='${creator}', path='${path}', mark='${mark}', info='${info}', fav='${fav}', bindata=${bindata}, \`date\`=CURRENT_DATE() WHERE id=${id}`;
  mysql.execute(sql, () => {
    switch (mark) {
      case "HCG":
        sql = `UPDATE PicturesHcg SET title='${name}', creator='${creator}', path='${path}', mark='${mark}', info='${info}', fav='${fav}', bindata=${bindata}, \`date\`=CURRENT_DATE() WHERE id=${id}`;
        mysql.execute(sql, (c) => {
          if (c == null) {
            res.render("modify_folder", {"title": PAGE_TITLE, "message": message, "id": id, "name": name, "creator": creator, "path": path,
            "mark": mark, "info": info, "fav": fav, "count": count, "bindata": bindata});
          }
          else {
            res.render('showInfo', {'title':'エラー', 'message':sql, 'icon':'cancel.png', 'link':null});
          }
        });
        break;
      case "DOUJIN":
        sql = `UPDATE PicturesDoujin SET title='${name}', creator='${creator}', path='${path}', mark='${mark}', info='${info}', fav='${fav}', bindata=${bindata}, \`date\`=CURRENT_DATE() WHERE id=${id}`;
        mysql.execute(sql, (c) => {
          if (c == null) {
            res.render("modify_folder", {"title": PAGE_TITLE, "message": message, "id": id, "name": name, "creator": creator, "path": path,
            "mark": mark, "info": info, "fav": fav, "count": count, "bindata": bindata});
          }
          else {
            res.render('showInfo', {'title':'エラー', 'message':sql, 'icon':'cancel.png', 'link':null});
          }
        });
        break;
      case "MANGA":
        sql = `UPDATE PicturesManga SET title='${name}', creator='${creator}', path='${path}', mark='${mark}', info='${info}', fav='${fav}', bindata=${bindata}, \`date\`=CURRENT_DATE() WHERE id=${id}`;
        mysql.execute(sql, (c) => {
          if (c == null) {
            res.render("modify_folder", {"title": PAGE_TITLE, "message": message, "id": id, "name": name, "creator": creator, "path": path,
            "mark": mark, "info": info, "fav": fav, "count": count, "bindata": bindata});
          }
          else {
            res.render('showInfo', {'title':'エラー', 'message':sql, 'icon':'cancel.png', 'link':null});
          }
        });
        break;
      case "PIXIV":
        sql = `UPDATE PicturesPixiv SET title='${name}', creator='${creator}', path='${path}', mark='${mark}', info='${info}', fav='${fav}', bindata=${bindata}, \`date\`=CURRENT_DATE() WHERE id=${id}`;
        mysql.execute(sql, (c) => {
          if (c == null) {
            res.render("modify_folder", {"title": PAGE_TITLE, "message": message, "id": id, "name": name, "creator": creator, "path": path,
            "mark": mark, "info": info, "fav": fav, "count": count, "bindata": bindata});
          }
          else {
            res.render('showInfo', {'title':'エラー', 'message':sql, 'icon':'cancel.png', 'link':null});
          }
        });
        break;
      case "PHOTO":
        sql = `UPDATE PicturesPhoto SET title='${name}', creator='${creator}', path='${path}', mark='${mark}', info='${info}', fav='${fav}', bindata=${bindata}, \`date\`=CURRENT_DATE() WHERE id=${id}`;
        mysql.execute(sql, (c) => {
          if (c == null) {
            res.render("modify_folder", {"title": PAGE_TITLE, "message": message, "id": id, "name": name, "creator": creator, "path": path,
            "mark": mark, "info": info, "fav": fav, "count": count, "bindata": bindata});
          }
          else {
            res.render('showInfo', {'title':'エラー', 'message':sql, 'icon':'cancel.png', 'link':null});
          }
        });
        break;
      default:
        res.render("modify_folder", {"title": PAGE_TITLE, "message": message, "id": id, "name": name, "creator": creator, "path": path,
           "mark": mark, "info": info, "fav": fav, "count": count, "bindata": bindata});
        break;
    }
  });
}

/* データ確認 */
function confirmData(req, res) {
  let id = req.params.id;
  if (id == undefined) {
    res.render("modify_folder", {"title": PAGE_TITLE, "message": "エラー： id が空欄です。", "id": "", "album": "", "info": "", "bindata": 0, "groupname": ""});
  }
  else {
    let sql = `SELECT * FROM Pictures WHERE id=${id}`;
    mysql.getRow(sql, function(row, fields) {
      if (row == undefined) {
        res.render("showInfo", {"title":"エラー", "message":"id に対するデータがありません。", "icon":"cancel.png"});
      }
      else {
        res.render("modify_folder", {"title": PAGE_TITLE, "message": "データを取得しました。", "id": row.id, "name": row.title, "creator": row.creator,
        "path": row.path, "mark": row.mark, "info": row.info, "fav": row.fav, "bindata": row.bindata});
      }
    });
  }
}


/*  デフォルトのハンドラ */
router.get('/', function(req, res, next) {
  let id = "";
  if (req.query.id) {
    id = req.query.id;
    mysql.getRow(`SELECT * FROM Pictures WHERE id=${id}`, (row) => {
      res.render("modify_folder", {"title": PAGE_TITLE, "message": "", "id": id, "name": row.title, "creator": row.creator, "path": row.path, "mark": row.mark, "info": row.info, "fav": row.fav, "bindata": row.bindata});
    })
  }
  else {
    res.render("modify_folder", {"title": PAGE_TITLE, "message": "", "id": "", "name": "", "creator": "", "path": "", "mark": "", "info": "", "fav": 0, "bindata": 0});
  }
});

/* フォームデータを受け取る。*/
router.post("/", function(req, res, next) {
  let id = req.body.id;
  if (id == "") {
    // 挿入
    insertData(req, res).catch(e => res.render('showInfo', {'title':'エラー', 'message':e.message, 'icon':'cancel.png', link:null}))
    .catch(e => res.render('showInfo', {'title':'エラー', 'message':e.message, 'icon':'cancel.png', 'link':null}));
  }
  else {
    // 更新
    updateData(req, res).catch(e => res.render('showInfo', {'title':'エラー', 'message':e.message, 'icon':'cancel.png', link:null}))
    .catch(e => res.render('showInfo', {'title':'エラー', 'message':e.message, 'icon':'cancel.png', 'link':null}));
  }
});

/* データ確認 */
router.get('/confirm/:id', function(req, res, next) {
  confirmData(req, res);
});

module.exports = router;