
/* creators.js */
'use strict';
var express = require('express');
var session = require('express-session');
var mysql = require('./MySQL.js');

var router = express.Router();

/* 作者が登録済みかチェック */
function checkCreator(creator) {
  return new Promise((resolve) => {
    mysql.getValue(`SELECT count(*) FROM Creators WHERE creator='${creator}'`, (v) => {
      resolve(v > 0);
    });
  });
}

/* 次の id を得る。*/
function getNextId() {
  return new Promise((resolve) => {
    mysql.getValue("SELECT max(id)+1 AS n FROM Creators", (n) => {
      resolve(n);
    });
  });
}

/* 作者追加 */
async function insert_creator(req, res) {
  let {id, creator, marks, info, fav, refcount, titlecount} = req.body;
  if (creator == "") {
    res.render('showInfo', {'title':'エラー', 'message':'作者が空欄です。', 'icon':'cancel.png', 'link':null});
    return;
  }
  let b = await checkCreator(creator);
  if (b) {
    res.render('showInfo', {'title':'エラー', 'message':'作者がすでに登録済みです。', 'icon':'cancel.png', 'link':null});
    return;
  }
  id = await getNextId();
  creator = creator.replace(/'/g, "''");
  let sql = `INSERT INTO Creators VALUES(${id}, '${creator}', '${marks}', '${info}', ${fav}, ${refcount}, ${titlecount})`;
  mysql.execute(sql, () => {
    res.render('modify_creator', {'message':'作者 ' + creator + " を追加しました。", 'id':id, 'creator':creator, 'marks':marks, 'info':info, 'fav':fav, 'refcount':refcount, 'titlecount':titlecount, 'modify':false});
  });
}

/* 作者情報更新 */
async function update_creator(req, res) {
  let {id, creator, marks, info, fav, refcount, titlecount} = req.body;
  if (isNaN(parseInt(id))) {
    res.render('showInfo', {'title':'エラー', 'message':'id は数でなければなりません。', 'icon':'cancel.png', 'link':null});
    return;
  }
  if (creator == "") {
    res.render('showInfo', {'title':'エラー', 'message':'作者が空欄です。', 'icon':'cancel.png', 'link':null});
    return;
  }
  creator = creator.replace(/'/g, "''");
  info = info.replace(/'/g, "''");
  let sql = `UPDATE Creators SET id='${id}', marks='${marks}', info='${info}', fav=${fav}, refcount=${refcount}, titlecount=${titlecount} WHERE creator = '${creator}'`;
  mysql.execute(sql, () => {
    res.render('modify_creator', {'message':'作者 ' + creator + " を更新しました。", 'id':id, 'creator':creator, 'marks':marks, 'info':info, 'fav':fav, 'refcount':refcount, 'titlecount':titlecount, 'modify':true});
  });

}


/* 作者一覧表示 */
router.get('/', function(req, res, next) {
  let sql = "SELECT * FROM Creators ORDER BY creator";
  let results = [];
  mysql.query(sql, (row) => {
    if (row == null) {
      res.render('creators', {'title':'作者一覧', 'message':'Ctrl+F で作者の検索ができます。', 'results':results, 'checked0':'', 'checked1':'checked'});
    }
    else {
      let acreator = `<a href="/pictures/selectcreator?creator=${row.creator}" target="_blank">${row.creator}</a>`;
      let aid = `<a href="/creators/modify_creator?id=${row.id}">${row.id}</a>`;
      results.push([aid, acreator, row.marks, row.info, row.fav, row.refcount, row.titlecount]);
    }
  });
});


/* 作者の追加・更新 */
router.get('/modify_creator', function(req, res) {
  if (req.query.id) {
    let id = req.query.id;
    let sql = `SELECT * FROM Creators WHERE id=${id}`;
    mysql.getRow(sql, (row) => {
      res.render('modify_creator', {'message':'更新モードです。', 'id':row.id, 'creator':row.creator, 'marks':row.marks, 'info':row.info, 'fav':row.fav, 'refcount':row.refcount, 'titlecount':row.titlecount, 'modify':true});
    });
  }
  else {
    res.render('modify_creator', {'message':'id が空欄の場合は追加、数の場合は更新となります。', 'id':'', 'creator':'', 'marks':'', 'info':'', 'fav':'0', 'refcount':'0', 'titlecount':'1', 'modify':false});
  }
});

/* 作者の追加・更新 POST  */
router.post('/modify_creator', function(req, res) {
  let id = req.body.id;
  if (id == "") {
    insert_creator(req, res).catch(e => res.render('showInfo', {'title':'エラー', 'message':e.message, 'icon':'cancel.png', link:null}));
  }
  else {
    update_creator(req, res).catch(e => res.render('showInfo', {'title':'エラー', 'message':e.message, 'icon':'cancel.png', link:null}));;
  }
});

/* 作者の追加・更新 データ確認  */
router.get('/confirm_creator', function(req, res) {
  let id = req.query.id;
  if (isNaN(parseInt(id))) {
    res.render('showInfo', {'title':'エラー', 'message':'id は数でなければなりません。', 'icon':'cancel.png', 'link':null})
  }
  else {
    mysql.getRow("SELECT * FROM Creators WHERE id = " + id, (row) => {
      res.render('modify_creator', {'message':`id ${id} が検索されました。`, 'id':row.id, 'creator':row.creator, 'marks':row.marks, 'info':row.info, 'fav':row.fav, 'refcount':row.refcount, 'titlecount':row.titlecount, 'modify':true})
    });
  }
});

/* 降順で表示 */
router.get('/desc', function(req, res) {
  let sort = "id";
  if (req.query.sort) {
    sort = req.query.sort;
  }
  let sql = `SELECT * FROM Creators ORDER BY ${sort} DESC`;
  let results = [];
  mysql.query(sql, (row) => {
    if (row == null) {
      let checked0, checked1;
      if (sort == "id") {
        checked0 = "checked";
        checked1 = "";
      }
      else {
        checked0 = "";
        checked1 = "checked";
      }
      res.render('creators', {'title':'作者一覧', 'message':'Ctrl+F で作者の検索ができます。', 'results':results, 'checked0':checked0, 'checked1':checked1});
    }
    else {
      let acreator = `<a href="/pictures/selectcreator?creator=${row.creator}" target="_blank">${row.creator}</a>`;
      results.push([row.id, acreator, row.marks, row.info, row.fav, row.refcount, row.titlecount]);
    }
  });
});

/* 昇順で表示 */
router.get('/asc', function(req, res) {
  let sort = "id";
  if (req.query.sort) {
    sort = req.query.sort;
  }
  let sql = `SELECT * FROM Creators ORDER BY ${sort} ASC`;
  let results = [];
  mysql.query(sql, (row) => {
    let checked0, checked1;
    if (sort == "id") {
      checked0 = "checked";
      checked1 = "";
    }
    else {
      checked0 = "";
      checked1 = "checked";
    }
    if (row == null) {
      res.render('creators', {'title':'作者一覧', 'message':'Ctrl+F で作者の検索ができます。', 'results':results, 'checked0':checked0, 'checked1':checked1});
    }
    else {
      let acreator = `<a href="/pictures/selectcreator?creator=${row.creator}" target="_blank">${row.creator}</a>`;
      results.push([row.id, acreator, row.marks, row.info, row.fav, row.refcount, row.titlecount]);
    }
  });
});


/* エクスポート */
module.exports = router;
