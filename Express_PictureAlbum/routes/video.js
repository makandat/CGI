/* index.js */
"use strict";
var fs = require('fs');
var express = require('express');
var os = require('os');
var router = express.Router();
var mysql = require('./MySQL.js');
var dt = require('./DateTime.js');
var fso = require('./FileSystem.js');
const LIMIT = 200;  // 1ページの表示数

const SELECT0 = "SELECT id, name, (SELECT COUNT(album) FROM Videos GROUP BY album HAVING album=id) AS count, info, bindata, groupname, `date` FROM Album";

/* package.json からバージョン番号を得る。*/
function getVersion() {
  let pstr = fs.readFileSync("package.json", "utf-8");
  let p = JSON.parse(pstr);
  return p.version;
}

/* SQL を作成する。*/
function makeSelect(req) {
    let sql = SELECT0;
    let where;
    let orderby;

    if (req.session.desc) {
      // 降順
      orderby = " ORDER BY id DESC";
      if (req.session.groupname == "ALL") {
        where = " WHERE mark='video'";
      }
      else if (req.session.groupname == "NONAME") {
        where = ` WHERE mark='video' AND (groupname = '' OR groupname IS NULL)`;
      }
      else {
        where = ` WHERE mark='video' AND groupname = '${req.session.groupname}'`;
      }
    }
    else {
      // 昇順
      orderby = " ORDER BY id ASC";
      if (req.session.groupname == "ALL") {
        where = " WHERE mark = 'video'";
      }
      else if (req.session.groupname == "NONAME") {
        where = ` WHERE mark = 'video' AND (groupname = '' OR groupname IS NULL)`;
      }
      else {
        where = ` WHERE mark = 'video' AND groupname = '${req.session.groupname}'`;
      }
    }

    sql += (where + orderby + ` LIMIT ${LIMIT}`);
    return sql;
}

/* アルバム一覧を表示 */
function showAlbum(req, res) {
  let albums = [];
  let sql = makeSelect(req);
  mysql.query(sql, (row) => {
    if (row == null) {
      let albumgroups = [];
      let sql = "SELECT DISTINCT groupname AS grpname FROM Album WHERE mark = 'video'";
      mysql.query(sql, (row) =>{
        if (row == null) {
          res.render('video', {'title':'ビデオアルバム for Express4', 'version':getVersion(), 'message':'アルバムグループ：' + req.session.groupname, 'albums':albums, 'albumgroups':albumgroups});
        }
        else {
          if (row.grpname != null) {
            albumgroups.push(row.grpname);
          }
        }
      });
    }
    else {
      let hid = `<a href="/video/videoalbum/${row.id}" target="_blank">${row.name}</a>`;
      let abin;
      if (row.bindata == null || row.bindata == 0) {
        abin = "";
      }
      else {
        abin = `<img src="/bindata/extract/${row.bindata}" alt="${row.bindata}" />`;
      }
      let aid = `<a href="/modify_album?id=${row.id}" target="_blank">${row.id}</a>`;
      albums.push([aid, hid, row.count, row.info, abin, row.groupname, dt.getDateString(row.date)]);
    }
  });
}

/* ビデオ一覧表示 */
function showVideoList(req, res) {
  let album = req.query.album;
  let sn = req.session.sn;
  let results = [];
  let sql = "SELECT id, album, title, path, creator, series, mark, info, fav, count, bindata FROM Videos";
  if (album == undefined) {
    if (req.session.desc) {
      sql = sql + ` WHERE sn <= ${sn} ORDER BY id DESC LIMIT ${LIMIT}`;
    }
    else {
      sql = sql + ` WHERE sn >= ${sn} ORDER BY id ASC LIMIT ${LIMIT}`;
    }
  }
  else {
    if (req.session.desc) {
      sql = sql +  `WHERE album = ${album} AND sn <= ${sn} ORDER BY id DESC`;
    }
    else {
      sql = sql + ` WHERE album = ${album} AND sn >= ${sn} ORDER BY id ASC`;
    }
  }
  mysql.query(sql, (row) => {
    let title;
    if (row == null) {
      if (album == undefined) {
        title = "ビデオ一覧";
      }
      else {
        title = 'ビデオ一覧 (album=' + album + ")";
      }
      mysql.getRow("SELECT max(id) AS maxId, min(id) AS minId, count(id) AS countId FROM Videos", (row) => {
        let message = `レコード数=${row.countId}, 最小 id = ${row.minId}, 最大 id = ${row.maxId}`;
        res.render('videolist', {'title':title, 'message':message, 'results':results, 'menu0':'block', 'menu1':'none'});
      });
    }
    else {
      let aid = `<a href="/video/modify_video?id=${row.id}" target="_blank">${row.id}</a>`;
      let afav = `<a href="/video/increase_fav">${row.count}</a>`;
      let abindata = `<figure><img src="/bindata/extract/${row.bindata}" alt="${row.bindata}" /><figcaption>${row.bindata}</figcaption><figure>`;
      if (row.bindata == "" || row.bindata == 0) {
        abindata = "";
      }
      let atitle = `<a href="/video/video_viewer?source=${row.path}&title=${row.title}" target="_blank">${row.title}</a>`;
      let apath = `<a href="/video/download?path=${row.path}" target="_blank">${row.path}</a>`;
      results.push([aid, row.album, atitle, apath, row.creator, row.series, row.mark, row.info, afav, row.count, abindata]);
    }
  });
}


/* 指定されたアルバム内のビデオ一覧表示 */
function showVideosInAlbum(req, res) {
  let album = req.params.album;
  let sql = `SELECT * FROM Videos WHERE album = ${album}`;
  let results = [];
  mysql.getValue(`SELECT name FROM Album WHERE id=${album}`, (albumName) => {
    mysql.query(sql, (row) => {
      if (row == null) {
        res.render('videoalbum', {'title':`(${album}) ${albumName}`, 'message':'', 'results':results});
      }
      else {
        let aid = `<a href="/video/modify_video?id=${row.id}" target="_blank">${row.id}</a>`;
        let atitle = `<a href="/video/video_viewer?source=${row.path}&title=${row.title}" target="_blank">${row.title}</a>`;
        let apath = `<a href="/video/download?path=${row.path}" target="_blank">${row.path}</a>`;
        let afav = `<a href="/video/increase_fav/${row.id}">${row.fav}</a>`;
        let aextract = `<figure><img src="/bindata/extract/${row.bindata}" alt="id=${row.bindata}" /><figcaption>${row.bindata}</figcaption></figure>`;
        if (row.bindata == "" || row.bindata == null)
          aextract = "";
        results.push([aid, atitle, apath, row.creator, row.series, row.mark, row.info, afav, row.count, aextract]);
      }
    });
  });
}



/*  リクエストハンドラ */
/* GET home page.  表示リセット */
router.get('/', function(req, res, next) {
  if (req.session.user == undefined) {
    res.redirect('/users?from=video');
  }
  else {
    req.session.desc = true;
    req.session.groupname = "ALL";
    mysql.getValue("SELECT max(sn) FROM Videos", (n) => {
      req.session.sn = n;
      showAlbum(req, res);
    });
  }
});

/* ビデオアルバム内容の表示 */
router.get('/videoalbum/:album', function(req, res, next) {
  showVideosInAlbum(req, res);
});


/* ビデオファイル表示 */
router.get('/video_viewer', function(req, res, next) {
  let path = req.query.source;
  let title = req.query.title;
  mysql.getValue(`SELECT id FROM Videos WHERE path='${path}'`, (id) => {
    mysql.execute(`CALL increaseVideoCount(${id})`, () => {
      res.render('video_viewer', {'title':title, 'message':path, 'source':path});
    });
  });
});

/* ビデオファイルのダウンロード */
router.get('/download', function(req, res, next) {
  let path = req.query.path;
  mysql.getValue(`SELECT id FROM Videos WHERE path='${path}'`, (id) => {
    mysql.execute(`CALL increaseVideoCount(${id})`, () => {
      res.sendFile(path);
    });
  });
});


/* 逆順で表示 */
router.get('/reverse', function(req, res, next) {
  req.session.desc = ! req.session.desc;
  if (req.session.desc) {
    mysql.getValue("SELECT max(sn) FROM Videos", (n) => {
      req.session.sn = n;
    });
  }
  else {
    req.session.sn = 0;
  }
  showAlbum(req, res);
});

/* ワード検索 */
router.get('/find', function(req, res, next) {
  let word = req.query.word;
  let sql = `SELECT * FROM Videos WHERE path LIKE '%${word}%' OR info LIKE '%${word}%'`;
  let results = [];
  mysql.query(sql, (row) => {
    if (row == null) {
      let title = "検索ワード: " + word;
      res.render('videolist', {'title':title, 'message':'', 'results':results, 'menu0':'none', 'menu1':'block'})
    }
    else {
       results.push([row.id, row.album, row.title, row.path, row.creator, row.series, row.mark, row.info, row.fav, row.count, row.bindata]);
    }

  });
});


/* アルバムグループの指定 */
router.get('/groupname', function(req, res, next) {
  req.session.groupname = req.query.name;
  req.session.desc = false;
  showAlbum(req, res);
});


/* ビデオ一覧表示 */
router.get('/videolist', function(req, res, next) {
  if (req.query.id) {
    mysql.getValue(`SELECT sn FROM Videos WHERE id=${req.query.id}`, (sn) => {
      if (sn) {
        req.session.sn = sn;
        showVideoList(req, res);
      }
      else {
        res.render('showInfo', {title:'エラー', message:'指定した id は存在しません。', icon:'cancel.png', link:null});
      }
    });
  }
  else {
    req.session.desc = true;
    mysql.getValue("SELECT max(sn) AS maxSN FROM Videos", (maxSN) => {
      req.session.sn = maxSN;
      showVideoList(req, res);
    });
  }
});

/* ビデオ一覧で逆順表示 */
router.get('/reverse_list', function(req, res, next) {
  req.session.desc = ! req.session.desc;
  if (req.session.desc) {
    mysql.getValue("SELECT max(sn) AS maxSN FROM Videos", (maxSN) => {
      req.session.sn = maxSN;
    });
  }
  else {
    req.session.sn = 0;
    showVideoList(req, res);
  }
});

/* ビデオ一覧 先頭へ */
router.get('/first', function(req, res, next) {
  if (req.session.desc) {
    mysql.getValue("SELECT max(sn) AS maxSN FROM Videos", (maxSN) => {
      req.session.sn = maxSN;
      showVideoList(req, res);
    });
  }
  else {
    req.session.sn = 0;
    showVideoList(req, res);
  }
});

/* ビデオ一覧 前へ */
router.get('/prev', function(req, res, next) {
  if (req.session.desc) {
    mysql.getValue("SELECT max(sn) AS maxSN FROM Videos", (maxSN) => {
      if (req.session.sn + LIMIT > maxSN) {
        req.session.sn = maxSN - LIMIT + 1;
      }
      else {
        req.session.sn += LIMIT;
      }
      showVideoList(req, res);
    });
  }
  else {
    req.session.sn -= LIMIT;
    if (req.session.sn < 0) {
      req.session.sn = 0;
    }
    showVideoList(req, res);
  }
});


/* ビデオ一覧 次へ */
router.get('/next', function(req, res, next) {
  if (req.session.desc) {
    req.session.sn -= LIMIT;
    if (req.session.sn < 0) {
      req.session.sn = 0;
    }
    showVideoList(req, res);
  }
  else {
    mysql.getValue('SELECT max(sn) FROM Videos', (maxSN) => {
      req.session.sn += LIMIT;
      if (maxSN < req.session.sn) {
        req.session.sn = maxSN - LIMIT;
      }
      showVideoList(req, res);
    });
  }
});

/* ビデオ一覧 最後へ */
router.get('/last', function(req, res, next) {
  if (req.session.desc) {
    req.session.sn = LIMIT;
    showVideoList(req, res);
  }
  else {
    mysql.getValue('SELECT max(sn) FROM Videos', (maxSN) => {
      req.session.sn = maxSN - LIMIT + 1;
      showVideoList(req, res);
    });
  }
});


/* ビデオを追加 */
async function insertVideo(req, res) {
  let {title, album, path, creator, series, mark, info, fav, bindata} = req.body;
  if (album == "") {
    res.render('showInfo', {'title':'エラー', 'message':'アルバム番号が空欄です。', 'icon':'cancel.png', link:null});
    return;
  }
  if (title == "") {
    res.render('showInfo', {'title':'エラー', 'message':'タイトルが空欄です。', 'icon':'cancel.png', link:null});
    return;
  }
  if (path == "") {
    res.render('showInfo', {'title':'エラー', 'message':'パスが空欄です。', 'icon':'cancel.png', link:null});
    return;
  }
  if (os.platform() == "win32") {
    path = path.replace(/\\/g, "/");
  }
  let b = await checkPath(path);
  if (b) {
    res.render('showInfo', {'title':'エラー', 'message':path + ' はすでに登録されています。', 'icon':'cancel.png', link:null});
    return;
  }
  title = title.replace(/'/g, "''").trim();
  path = path.replace(/'/g, "''").trim();
  let sql = `INSERT INTO Videos VALUES(NULL, ${album}, '${title}', '${path}', '${creator}', '${series}', '${mark}', '${info}', '${fav}', 0, ${bindata}, 0, 0)`;
  mysql.execute(sql, () => {
    res.render('modify_video', {'message':title + 'を追加しました。', 'id':'', 'album':album, 'title':title, 'path':path, 'creator':creator, 'series':series, 'mark':mark, 'info':info, 'fav':fav, 'bindata':bindata});
  });
}


/* パスが登録されているかチェックする。*/
function checkPath(path) {
  return new Promise((resolve) => {
    mysql.getValue(`SELECT count(id) FROM Videos WHERE path='${path}'`, (n) => {
      resolve(n > 0);
    });
  });
}

/* ビデオを更新 */
async function updateVideo(req, res) {
  let {id, album, title, path, creator, series, mark, info, fav, bindata} = req.body;
  if (album == "") {
    res.render('showInfo', {'title':'エラー', 'message':'アルバム番号が空欄です。', 'icon':'cancel.png', link:null});
    return;
  }
  if (os.platform() == "win32") {
    path = path.replace(/\\/g, "/");
  }
  title = title.replace(/'/g, "''").trim();
  path = path.replace(/'/g, "''").trim();
  let sql = `UPDATE Videos SET album=${album}, title='${title}', path='${path}', creator='${creator}', series='${series}', mark='${mark}', info='${info}', fav=${fav}, bindata=${bindata} WHERE id = ${id}`;
  mysql.execute(sql, () => {
    res.render('modify_video', {'message':"id = " + id + 'を更新しました。', 'id':id, 'album':album, 'title':title, 'path':path, 'creator':creator, 'series':series, 'mark':mark, 'info':info, 'fav':fav, 'bindata':bindata});
  });
}

/* ビデオの追加・更新 */
router.get('/modify_video', function(req, res, next) {
  if (req.query.id) {
    mysql.getRow(`SELECT * FROM Videos WHERE id=${req.query.id}`, (row) => {
      res.render('modify_video', {'message':'', 'id':row.id, 'album':row.name, 'title':row.title, 'path':row.path, 'creator':row.creator, 'series':row.series, 'mark':row.mark, 'info':row.info, 'fav':row.fav, 'bindata':row.bindata});
    });
  }
  else {
    res.render('modify_video', {'message':'', 'id':'', 'album':'', 'title':'', 'path':'', 'creator':'', 'series':'', 'mark':'', 'info':'', 'fav':'0', 'bindata':'0'});
  }
});

/* ビデオの追加・更新 POST */
router.post('/modify_video', function(req, res, next) {
    let id = req.body.id;
    if (id == "") {
        insertVideo(req, res).catch(e => res.render('showInfo', {'title':'エラー', 'message':e.message, 'icon':'cancel.png', link:null}));
    }
    else {
        updateVideo(req, res).catch(e => res.render('showInfo', {'title':'エラー', 'message':e.message, 'icon':'cancel.png', link:null}));
    }
});


/* id が存在するかチェックする。*/
function checkId(id) {
    return new Promise((resolve) => {
        mysql.getValue("SELECT count(id) FROM Videos WHERE id=" + id, (n) => {
            resolve(n > 0);
        });
    });
}


/* id から path を得る。*/
function getPathFromId(id) {
  return new Promise((resolve) => {
    mysql.getValue(`SELECT path FROM Videos WHERE id='${id}'`, path => resolve(path));
  });
}

/* 前の id を得る。*/
function getPrevId(path) {
  return new Promise((resolve) => {
    mysql.getValue(`SELECT max(id) AS maxId FROM Videos WHERE id < (SELECT id FROM Videos WHERE path='${path}')`, maxId => resolve(maxId));
  });
}

/* 次の id を得る。*/
function getNextId(path) {
  return new Promise((resolve) => {
    mysql.getValue(`SELECT min(id) AS maxId FROM Videos WHERE id > (SELECT id FROM Videos WHERE path='${path}')`, maxId => resolve(maxId));
  });
}

/* タイトルを得る。*/
function getTitle(id) {
  return new Promise((resolve) => {
    mysql.getValue(`SELECT title FROM Videos WHERE id = ${id}`, title => resolve(title));
  });

}

/* ビデオのナビゲート表示 Previous */
router.get('/nav_prev', async function(req, res, next) {
  let path = req.query.path;
  let prevId = await getPrevId(path);
  if (prevId) {
    let prevPath = await getPathFromId(prevId);
    let title = await getTitle(prevId);
    res.srender('video_viewer', {'title':title, 'message':prevPath, 'source':prevPath});
  }
  else {
    res.render('showInfo', {'title':'エラー', 'message':'前へ移動できません。', 'icon':'cancel.png', link:null});
  }
});

/* ビデオのナビゲート表示 Next */
router.get('/nav_next', async function(req, res, next) {
  let path = req.query.path;
  let nextId = await getNextId(path);
  if (nextId) {
    let nextPath = await getPathFromId(nextId);
    let title = await getTitle(nextId);
    res.render('video_viewer', {'title':title, 'message':nextPath, 'source':nextPath});
  }
  else {
    res.render('showInfo', {'title':'エラー', 'message':'次へ移動できません。', 'icon':'cancel.png', link:null});
  }
});



/* データ確認 ヘルパ関数 */
async function confirmVideo(req, res) {
    let id = req.params.id;
    let b = await checkId(id);
    if (b == false) {
        res.render('showInfo', {'title':'エラー', 'message':`id = ${id} は存在しません。`, 'icon':'cancel.png', 'link':null});
    }
    else {
        mysql.getRow("SELECT * FROM Videos WHERE id=" + id, (row) => {
            res.render('modify_video', {'message':'id = ' + id + ' が検索されました。', 'id':row.id, 'album':row.album, 'title':row.title, 'path':row.path, 'creator':row.creator, 'mark':row.mark, 'series':row.series, 'info':row.info, 'fav':row.fav, 'bindata':row.bindata});
        });
    }
}

/* ビデオの追加・更新 データ確認 */
router.get('/confirm/:id', function(req, res, next) {
    confirmVideo(req, res).catch(e => res.render('showInfo', {'title':'エラー', 'message':e.message, 'icon':'cancel.png', link:null}));
});

/* Videos テーブルで fav を増やす。*/
router.get('/increase_fav/:id', function(req, res, next) {
  let id = req.params.id;
  mysql.execute(`CALL IncreaseVideoFav(${id})`, ()=> {
    mysql.getValue("SELECT album FROM Videos WHERE id=" + id, (album) => {
      req.params.album = album;
      showVideosInAlbum(req, res);
    })
  });
});




/* エクスポート */
module.exports = router;

