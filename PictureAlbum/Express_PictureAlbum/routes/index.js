/* index.js */
/*  Ver 1.0.20  ログイン画面オプション　起動パラメータを付けるとログイン画面が表示されない。*/
"use strict";
var express = require('express');
var fs = require('fs');
var router = express.Router();
var mysql = require('./MySQL.js');
var dt = require('./DateTime.js');

const LIMIT = 200;  // 1ページの表示数
const SELECT0 = "SELECT id, name, mark, (SELECT COUNT(album) FROM PictureAlbum GROUP BY album HAVING album=id) AS count, info, bindata, groupname, `date` FROM Album";

/* package.json からバージョン番号を得る。*/
function getVersion() {
  let pstr = fs.readFileSync("package.json", "utf-8");
  let p = JSON.parse(pstr);
  return p.version;
}


/* SELECT 文を作成する。*/
function makeSelect(req) {
  let sql = SELECT0;
  let where = " WHERE mark='picture'";
  let orderby = "";

  if (req.session.desc) {
    // 降順
    orderby = " ORDER BY id DESC";
    if (req.session.groupname == "ALL") {
    }
    else if (req.session.groupname == "NONAME") {
      where = ` WHERE mark='picture' AND (groupname = '' OR groupname IS NULL)`;
    }
    else {
      where = ` WHERE mark='picture' AND groupname = '${req.session.groupname}'`;
    }
  }
  else {
    // 昇順
    orderby = " ORDER BY id ASC";
    if (req.session.groupname == "ALL") {
    }
    else if (req.session.groupname == "NONAME") {
      where = ` WHERE mark = 'picture' AND (groupname = '' OR groupname IS NULL)`;
    }
    else {
      where = ` WHERE mark = 'picture' AND groupname = '${req.session.groupname}'`;
    }
  }

  sql += (where + orderby + ` LIMIT ${LIMIT}`);
  return sql;
}


/* アルバム一覧を表示 */
function showResults(req, res) {
  let albums = [];
  let sql = makeSelect(req);
  mysql.query(sql, (row) => {
    if (row == null) {
      let albumgroups = [];
      let mark = 'picture';
      if (req.query.mark != undefined) {
        mark = req.query.mark;
      }
      let sql = `SELECT DISTINCT groupname AS grpname FROM Album WHERE mark = '${mark}'`;

      mysql.query(sql, (row) =>{
        if (row == null) {
          res.render('index', {'title':'画像アルバム for Express4', 'version':getVersion(), 'message':'アルバムグループ：' + req.session.groupname, 'albums':albums, 'albumgroups':albumgroups});
        }
        else {
          if (row.grpname != null) {
            albumgroups.push(row.grpname);
          }
        }
      });
    }
    else {
      let hid = `<a href="/pictalbum/?album=${row.id}" target="_blank">${row.name}</a>`;
      let abin;
      if (row.bindata == null || row.bindata == 0) {
        abin = "";
      }
      else {
        abin = `<figure><img src="/bindata/extract/${row.bindata}" id="thumb${row.bindata}" /><figcaption>${row.bindata}</figcaption><figure>`;
      }
      let aid = `<a href="/modify_album?id=${row.id}" target="_blank">${row.id}</a>`;
      albums.push([aid, hid, row.count, row.info, abin, row.groupname, dt.getDateString(row.date)]);
    }
  });
}


/* アルバム一覧をアイコン形式で表示 */
function showIcons(req, res) {
  let albums = [];
  let sql = makeSelect(req);
  mysql.query(sql, (row) => {
    if (row == null) {
      let albumgroups = [];
      let mark = 'picture';
      if (req.query.mark != undefined) {
        mark = req.query.mark;
      }
      let sql = `SELECT DISTINCT groupname AS grpname FROM Album WHERE mark = '${mark}'`;

      mysql.query(sql, (row) =>{
        if (row == null) {
          res.render('index2', {'title':'画像アルバム for Express4', 'version':getVersion(), 'message':'アルバムグループ：' + req.session.groupname, 'albums':albums, 'albumgroups':albumgroups});
        }
        else {
          if (row.grpname != null) {
            albumgroups.push(row.grpname);
          }
        }
      });
    }
    else {
      let caption = row.name.length > 15 ? row.name.slice(0, 12) + ' ...' : row.name;
      caption = `<a href="/pictalbum/?album=${row.id}" target="_blank">${caption}</a>`;
      let icon;
      if (row.bindata == null || row.bindata == 0) {
        icon = "/img/no_icon.png";
      }
      else {
        icon = `/bindata/extract/${row.bindata}`;
      }
      albums.push({'id':row.id, 'icon':icon, 'caption':caption});
    }
  });
}


/*  リクエストハンドラ */
/* GET home page.  表示リセット */
router.get('/', function(req, res, next) {
  if (process.argv.length == 2) {
    if (req.session.user == undefined) {
      res.redirect('/users');
    }
    else {
      req.session.desc = false;
      req.session.groupname = "ALL";
      req.session.mode = "list";
      showResults(req, res);
    }
  }
  else {
    req.session.desc = false;
    req.session.groupname = "ALL";
    req.session.mode = "list";
    req.session.user = "root";
    showResults(req, res);
  }
});

/* アイコン形式で表示 */
router.get('/icon', function(req, res, next) {
  if (process.argv.length == 2) {
    if (req.session.user == undefined) {
      res.redirect('/users');
    }
    else {
      req.session.desc = false;
      req.session.groupname = "ALL";
      req.session.mode = "icons";
      showIcons(req, res);
    }
  }
  else {
    req.session.desc = false;
    req.session.groupname = "ALL";
    req.session.mode = "list";
    req.session.user = "root";
    showResults(req, res);
  }
});

/* 逆順で表示 */
router.get('/reverse', function(req, res, next) {
  req.session.desc = ! req.session.desc;
  if (req.session.mode == "list") {
    showResults(req, res);
  }
  else {
    showIcons(req, res);
  }
});


/* アルバムグループの指定 */
router.get('/groupname', function(req, res, next) {
  let name = req.query.name;
  name = name == '[無名]' ? 'NONAME' : name;
  let mark = req.query.mark;
  req.session.groupname = name;
  if (mark == undefined || mark == "picture") {
    if (req.session.mode == "list") {
      showResults(req, res);
    }
    else {
      showIcons(req, res);
    }
  }
  else if (mark == "video") {
    res.redirect("/video/groupname?name=" + name);
  }
  else {
    res.render('showInfo', {title:"エラー", message:"不正な分類マークです。" + mark, icon:"cancel.png", link:null});
  }
});

/* 画像ファイルを送る。*/
router.get("/getimage", function(req, res) {
  res.sendFile(req.query.path);
});

/* アルバムグループ一覧を返す。*/
router.get('/album_group/:mark', function(req, res) {
  let mark = req.params.mark;
  let groups = [];
  mysql.query(`SELECT DISTINCT groupname AS g FROM Album WHERE mark='${mark}'`, (row) => {
    if (row == null) {
      res.json(groups);
    }
    else {
      groups.push(row.g);
    }
  });
});


/* エクスポート */
module.exports = router;
