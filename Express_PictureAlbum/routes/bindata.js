/* bindata.js */
'use strict';
var express = require('express');
var router = express.Router();

var mysql = require('./MySQL.js');

const LIMIT = 200;  // 1ページの表示数
const SELECT0 = "SELECT id, title, original, datatype, info, size FROM BINDATA WHERE (datatype='.jpg' OR datatype='.png')";

/* BINDATA テーブルの内容一覧を表示する。*/
function showBINDATAList(req, res) {
  let sql = makeSelect(req);
  let results = [];
  mysql.query(sql, (row) => {
    if (row == null) {
      res.render('bindata', { "title": '画像サムネール一覧 (BINDATA テーブル)', "results": results, "message": "データの挿入や更新はコマンドで行う。詳細はヘルプを参照。" });
    }
    else {
      let aid = `<a href="/bindata/modify_bindata?id=${row.id}" target="_blank">${row.id}</a>`;
      let aextract = `<img src="/bindata/extract/${row.id}" alt="id=${row.id}" />`;
      results.push([aid, aextract, row.title, row.original, row.datatype, row.info, row.size]);
    }
  });
}


/* SELECT 文を作成する。*/
function makeSelect(req) {
  let sql = SELECT0;
  let where;
  let orderby;

  if (req.session.desc) {
    // 降順
    orderby = " ORDER BY id DESC";
    where = " AND sn <= " + req.session.sn;
  }
  else {
    // 昇順
    orderby = " ORDER BY id ASC";
    where = " AND sn >= " + req.session.sn;
  }

  sql = sql + where + orderby + " LIMIT " + LIMIT;
  return sql;
}



/*  リクエストハンドラ */
/* GET BINDATA table listing. */
router.get('/', function(req, res, next) {
  req.session.sn = 0;
  req.session.desc = false;
  showBINDATAList(req, res);
});

/* 逆順で表示 */
router.get('/reverse', function(req, res, next) {
  req.session.desc = !req.session.desc;
  if (req.session.desc) {
    mysql.getValue("SELECT max(sn) FROM BINDATA", (maxSN) => {
      req.session.sn = maxSN;
      showBINDATAList(req, res);
    });
  }
  else {
    req.session.sn = 0;
    showBINDATAList(req, res);
  }
});

/* 先頭のページへ */
router.get('/first', function(req, res, next) {
  if (req.session.desc) {
    mysql.getValue("SELECT max(sn) FROM BINDATA", (maxSN) => {
      req.session.sn = maxSN;
      showBINDATAList(req, res);
    });
  }
  else {
    req.session.sn = 0;
    showBINDATAList(req, res);
  }
});

/* 前のページへ */
router.get('/prev', function(req, res, next) {
  if (req.session.desc) {
    req.session.sn += LIMIT;
  }
  else {
    req.session.sn -= LIMIT;
  }
  showBINDATAList(req, res);
});

/* 次のページへ */
router.get('/next', function(req, res, next) {
  if (req.session.desc) {
    req.session.sn -= LIMIT;
  }
  else {
    req.session.sn += LIMIT;
  }
  showBINDATAList(req, res);
});

/* 最後のページへ */
router.get('/last', function(req, res, next) {
  if (req.session.desc) {
    req.session.sn = LIMIT;
    showBINDATAList(req, res);
  }
  else {
    mysql.getValue("SELECT max(sn) FROM BINDATA", (n) =>{
      req.session.sn = n - LIMIT + 1;
      showBINDATAList(req, res);
    });
  }
});


/* 指定 id から表示する。(表示は昇順へもどる) */
router.get('/jump/:id', function(req, res, next) {
  req.session.desc = false;
  mysql.getValue("SELECT sn FROM BINDATA WHERE id=" + req.params.id, (sn) => {
    req.session.sn = sn;
    showBINDATAList(req, res);
  })
});

/* 情報の修正 */
router.get('/modify_bindata', function(req, res, next) {
  if (req.query.id) {
    mysql.getRow(`SELECT * FROM BINDATA WHERE id=${req.query.id}`, (row) => {
      res.render('modify_bindata', {'message':'', 'id':row.id, 'title':row.title, 'original':row.original, 'datatype':row.datatype, 'data':row.data, 'info':row.info, 'size':row.size});
    });
  }
  else {
    res.render('modify_bindata', {'message':'', 'id':'', 'title':'', 'original':'', 'datatype':'', 'data':'', 'info':'', 'size':''});
  }
});

/* 情報の修正 POST */
router.post('/modify_bindata', function(req, res, next) {
  let {id, title, original, datatype, data, info, size} = req.body;
  if (id == "" || isNaN(parseInt(id))) {
    res.render('showInfo', {'title':'エラー', 'message':'id が空欄であるか数ではありません。', 'icon':'cancel.png', 'link':null});
    return;
  }
  title = title.replace(/'/g, "''").trim();
  original = original.replace(/'/g, "''").trim();
  let sql = `UPDATE BINDATA SET title='${title}', original='${original}', datatype='${datatype}', info='${info}' WHERE id=${id}`;
  mysql.execute(sql, () => {
    res.render('modify_bindata', {'message':'id = ' + id + ' が更新されました。', 'id':id, 'title':title, 'original':original, 'datatype':datatype, 'data':'(更新されません)', 'info':info, 'size':size});
  });
});

/* データ確認 */
router.get('/confirm/:id', function(req, res, next) {
  let id = req.params.id;
  let sql = "SELECT id, title, original, datatype, info, size FROM BINDATA WHERE id=" + id;
  mysql.getRow(sql, (row) => {
    res.render('modify_bindata', {'message':'id = ' + id + ' のデータを取得しました。', 'id':id, 'title':row.title, 'original':row.original, 'datatype':row.datatype, 'data':'(変更できません)', 'info':row.info, 'size':row.size});
  });
});



/* BINDATA テーブルから画像データを得る。 */
router.get('/extract/:id', function(req, res, next){
  let id = req.params.id;
  let sql = "SELECT datatype, data FROM BINDATA WHERE id = " + id;
  mysql.getRow(sql, (row) => {
    let type;
    if (row == undefined) {
      res.send(null);
    }
    else {
      if (row.datatype == undefined) {
        type = 'image/jpeg';
      }
      else if (row.datatype == '.jpg') {
        type = 'image/jpeg';
      }
      else if (row.datatype == '.png') {
        type = 'image/png';
      }
      else {
        type = "image/gif";
      }
      res.set("Content-Type", type);
      res.send(row.data);
    }
  });
});


/* エクスポート */
module.exports = router;
