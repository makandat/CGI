'use strict';
/* tools.js */
var express = require('express');
var router = express.Router();

var mysql = require('./MySQL.js');
var fso = require('./FileSystem.js');
var child_process = require('child_process');
var os = require('os');

/* 指定したテーブルの指定 id データを削除する。*/
function deleteRow(tableName, id) {
    return new Promise((resolve) => {
        let sql = `DELETE FROM ${tableName} WHERE id=${id}`;
        mysql.execute(sql, () => {
            resolve(1);
        })
    });
}

/* Pictures テーブルの id から派生テーブル名を得る。*/
function getDerivedTable(id) {
    return new Promise((resolve) => {
        let sql = `SELECT mark FROM Pictures WHERE id=${id}`;
        mysql.getValue(sql, (mark) => {
            let tableName = "";
            switch (mark) {
                case "MANGA":
                    tableName = "PicturesManga";
                    break;
                case "HCG":
                    tableName = "PicturesHcg";
                    break;
                case "DOUJIN":
                    tableName = "PicturesDoujin";
                    break;
                case "PIXIV":
                    tableName = "PicturesPixiv";
                    break;
                default:
                    break;
            }
            resolve(tableName);
        });
    });
}

/* Pictures テーブルの id に対する bindata の id を得る。*/
function getBINDATAId(id) {
    return new Promise((resolve) => {
        let sql = "SELECT bindata FROM Pictures WHERE id = " + id;
        mysql.getValue(sql, (bid) => {
            resolve(bid);
        });
    });
}

/* データ削除 */
async function deleteData(id, derived_table, bindata) {
    if (derived_table) {
        let tableName = await getDerivedTable(id);
        await deleteRow(tableName, id);
    }
    if (bindata) {
        let bid = await getBINDATAId(id);
        if (!(bid == null || bid == 0)) {
            await deleteRow('BINDATA', bid);
        }
    }
    await deleteRow('Pictures', id);
}

/* デフォルトはエラーにする。*/
router.get("/", (req, res) => {
    res.render('showInfo', {'title':'エラー', 'message':'/tools は画面表示用ではありません。', 'icon':'cancel.png', 'link':null});
});

/* Pictures テーブルの指定した id のレコードを派生テーブルに追加 */
router.get('/insertDerivedTable', (req, res) => {
    let {id, stored} = req.query;
    let sql = `CALL ${stored}(${id})`;
    mysql.execute(sql, () => {
        res.json({'err':'0', 'message':"id = " + id + " を追加しました。"});
    });
});

/* テーブルの行番号 (sn) を付け直す。*/
router.get('/renumberSN', (req, res) =>{
    let {table, startId} = req.query;
    let sql;
    if (table == 'Creators') {
        sql = `CALL CreatorsID()`;
        mysql.execute(sql, () => {
            res.json({'err':'0', 'message':"ストアドプロシージャ CreatorsID を実行しました。"});
        });
    }
    else {
        sql = `CALL ${table}(${startId})`;
        mysql.execute(sql, () => {
            res.json({'err':'0', 'message':"ストアドプロシージャ " + table + " を実行しました。"});
        });
    }
});


/* 派生テーブルの再構築 TRUNCATE */
function rebuildTruncate(table) {
    return new Promise((resolve) => {
        let tableName = "Pictures" + table;
        if (table == "Creators") {
            tableName = table;
        }
        mysql.execute("TRUNCATE TABLE " + tableName, () => {
            resolve("OK");
        });
    });
}

/* 派生テーブルの再構築 INSERT */
function rebuildInsert(table) {
    return new Promise((resolve) => {
        let sql;
        if (table == 'Creators') {
            sql = "INSERT INTO user.Creators SELECT null, creator as name, '' as marks, '' as info, sum(fav) as fav, sum(count) as refcount, count(creator) as titlecount FROM user.Pictures GROUP BY creator;";
            mysql.execute(sql, () => {
                resolve("OK");
            });    
        }
        else {
            let tableName = "Pictures" + table;
            let mark = table.toUpperCase();
            if (table == "Time") {
                sql = `INSERT INTO ${tableName} SELECT * FROM Pictures ORDER BY id`;
            }
            else {
                sql = `INSERT INTO ${tableName} SELECT * FROM Pictures WHERE mark='${mark}' ORDER BY id`;
            }
            mysql.execute(sql, () => {
                resolve("OK");
            });    
        }
    });
}

/* 派生テーブルの再構築 Renumber SN */
function rebuildRenumSN(table) {
    return new Promise((resolve) => {
        if (table == "Creators") {
            mysql.execute("CALL CreatorsID()", () => {
                resolve("OK");
            });    
        }
        else {
            let ProcName = table + "SN()";
            mysql.execute("CALL " + ProcName, () => {
                resolve("OK");
            });    
        }
    });
}

/* 派生テーブルの再構築 ヘルパ関数 */
async function rebuildTable(table) {
    await rebuildTruncate(table);
    await rebuildInsert(table);
    await rebuildRenumSN(table);
}

/* 派生テーブルの再構築 */
router.get('/rebuild', (req, res) => {
    let table = req.query.rebuild;
    rebuildTable(table).catch(e => res.render('showInfo', {'title':'エラー', 'message':e.message, 'icon':'cancel.png', link:null}));
    res.send("再構築終了。Pictures" + table);
});

/* Pictures と派生テーブルからのデータ削除 */
router.get('/deletePictures', (req, res) => {
    let {id, derived_table, bindata} = req.query;
    let n = 0;
    if (id.includes('-')) {
        let ids = id.split('-');
        for (let i = ids[0]; i <= ids[1]; i++) {
            deleteData(i, derived_table, bindata)
            .then(() => {n++})
        }
        res.json({'err':'0', 'message':"Pictures からデータを削除しました。"});
    }
    else {
        deleteData(id, derived_table, bindata)
        .then(() => { res.json({'err':'0', 'message':"Picturs id = " + id + " を削除しました。"})})
        .catch(e => res.render('showInfo', {'title':'エラー', 'message':e.message, 'icon':'cancel.png', link:null}));
    }
});

/* アルバムを削除 */
router.get('/deleteAlbum', (req, res) => {
    let id = req.query.id;
    mysql.execute(`CALL DeleteAlbum(${id})`, () => {
        res.json({'err':'0', 'message':"アルバム id = " + id + " を削除しました。"});
    });
});

/* PictureAlbum の画像データを削除 */
router.get('/deletePictureAlbum', (req, res) => {
    let id = req.query.id;
    deleteRow('PictureAlbum', id)
      then((resolve) => {
        res.json({'err':'0', 'message':"PictureAlbum id = " + id + " を削除しました。"});
      });
});

/* ファイルを PictureAlbum にインポートする promise 関数 */
function insertFile(path, album, table) {
    return new Promise((resolve) => {
        let title = fso.getFileName(path).replace(/'/g, "''");
        let ext = fso.getExtension(path);
        title = title.replace(ext, '');
        let sql;
        if (table == "PictureAlbum") {
            sql = `INSERT INTO PictureAlbum VALUES(NULL, ${album}, '${title}', '${path}', 'creator', 'info', 0, 0, 0, CURRENT_DATE(), 0)`;
        }
        else {
            sql = `INSERT INTO Videos VALUES(NULL, ${album}, '${title}', '${path}', 'creator', 'series', 'video', 'info', 0, 0, 0, 0)`;
        }
        mysql.execute(sql, () => {
            resolve(1);
        });
    });
}


/* POST: ファイルリストを PictureAlbum or Videos にインポートする。*/
router.post('/import_filelist', (req, res) => {
    let {filelist, album, table} = req.body;
    let files = filelist.split(/\n/g);
    let promises = [];
    for (let i = 0; i < files.length; i++) {
        if (os.platform() == "win32") {
            files[i] = files[i].replace(/\\/g, "/");
        }
        files[i] = files[i].trim().replace(/'/g, "''");
        promises.push(insertFile(files[i], album, table));
    }
    Promise.all(promises).then(f => {
        let n = f.length.toString();
        res.send("アルバム " + album + " に " + n + " 個のデータを追加しました。");    
    });
});

/* path が テーブルに登録済みかチェックする。*/
function checkVideo(path, tableName) {
    return new Promise((resolve) => {
        let sql = `SELECT count(id) FROM ${tableName} WHERE path ='${path}'`;
        mysql.getValue(sql, n => resolve(n > 0));
    });
}

/* Videos テーブルの次の連続番号(sn)を得る。*/
function getNextSN(tableName) {
    return new Promise((resolve) => {
        mysql.getValue(`SELECT max(sn) FROM ${tableName}`, (n) => {
            if (n == null) {
                resolve(1);
            }
            else {
                n++;
                resolve(n);
            }
        });
    });
}

// importFile で使用する sn の値
var sn_import = 0;

/* ファイルをインポートする。*/
async function importFile(req, res, path, tableName) {
    let album = req.query.album;
    if (os.platform() == "win32") {
        path = path.replace(/\\/g, "/");
    }
    path = path.replace(/'/g, "''").trim();
    let fileName = fso.getFileName(path);
    let pp = fileName.lastIndexOf('.');
    let title = fileName.slice(0, pp);
    if (sn_import == 0) {
        sn_import = await getNextSN(tableName);
    }
    else {
        sn_import++;
    }
    let b = await checkVideo(path, tableName);
    let sql;
    if (b == false) {
        if (tableName == "Videos") {
            sql = `INSERT INTO Videos VALUES(NULL, ${album}, '${title}', '${path}', '', '', 'video', '', 0, 0, 0, ${sn_import})`;
        }
        else {
            sql = `INSERT INTO PictureTable VALUES(NULL, ${album}, '${title}', '${path}', '', '', 0, 0, 0, CURRENT_DATE(), ${sn_import})`;
        }
        mysql.execute(sql, () => { });
    }
}

/* 指定フォルダに含まれるファイル一覧を Videos にインポートする。*/
router.get('/import_folder', (req, res) => {
    let folder = req.query.folder;
    let table = req.query.table;
    sn_import = 0;
    
    if (table == "Videos") {
        fso.getFiles(folder, ['.mp4', '.avi', '.wmv', '.mkv', '.mov', '.mpg', '.gif'], (paths) => {
            for (let path of paths) {
                importFile(req, res, path, table);
            }
            res.send(`OK: ${folder} から動画ファイルを ${paths.length} 件インポートしました。`);
        });
    }
    else {
        fso.getFiles(folder, ['.jpg', '.png', '.gif', '.JPG', '.jpeg'], (paths) => {
            for (let path of paths) {
                importFile(req, res, path, table);
            }
            res.send(`OK: ${folder} から画像ファイルを ${paths.length} 件インポートしました。`);
        });
    }
});


/* サムネール画像を BINDATA テーブルにインポート(挿入)する。*/
router.get('/ins_bindata', (req, res) => {
    let path = req.query.path;
    if (os.platform() == "win32") {
        path = path.replace(/\\/g, "/");
    }
    path = path.trim().replace(/'/g, "''");
    let cmd = "InsBINDATA " + path;
    child_process.exec(cmd, (error, stdout, stderr) => {
        if (error) {
            res.send("エラーを検出。");
        }
        else {
            mysql.getValue("SELECT max(id) FROM BINDATA", (maxId) => {
                res.send("挿入成功 path:" + path + ", id:" + maxId);
            });
        }
    });    
});


/* BINDATA テーブルで指定された id の画像データを更新する。*/
router.get('/upd_bindata', (req, res) => {
    let {path, id} = req.query;
    if (os.platform() == "win32") {
        path = path.replace(/\\/g, "/");
    }
    path = path.trim().replace(/'/g, "''");
    let cmd = `UpdateBINDATA ${path} ${id}`;
    child_process.exec(cmd, (error, stdout, stderr) => {
        if (error) {
            res.send("エラーを検出。");
        }
        else {
            res.send("更新成功 path:" + path + ", id:" + id);
        }
    });    
});


/* 画像ファイルからサムネール画像を作成して BINDATA テーブルにインポート(挿入)し、Pictures テーブルの id に関連付ける。*/
router.get('/ins_bindata3', (req, res) => {
    let path = req.query.path;
    if (os.platform() == "win32") {
        path = path.replace(/\\/g, "/");
    }
    path = path.trim().replace(/'/g, "''");
    let id = req.query.id;
    child_process.exec("InsBINDATA3 " + path + " " + id, (error, stdout, stderr) => {
        if (error) {
            res.send("エラーを検出。");
        }
        else {
            res.send("成功 id=" + id + " path = " + path);
        }
    });    
});


/* BINDATA の最大 id を返す。*/
router.get('/bindata_maxid', (req, res) => {
    mysql.getValue("SELECT max(id) AS maxId FROM BINDATA", (maxId) => {
        res.set('Content-Type', 'text/plain');
        res.send(maxId.toString());
    });
});



/* テーブルの表示・最新１００件 */
router.get('/view100', (req, res) => {
    let tableName = req.query.table;
    let sql = "";
    let content = "";

    if (tableName == "Pictures" || tableName == "PicturesManga" || tableName == "PicturesHcg" || tableName == "PicturesDoujin" || tableName == "PicturesPixiv" || tableName == "PicturesTime" || tableName == "PicturesPhoto") {
        sql = "SELECT id, title, creator, path, mark, info, fav, count, bindata, DATE_FORMAT(`date`, '%Y-%m-%d') AS DT, sn FROM " + tableName + " ORDER BY id DESC LIMIT 100";
        mysql.query(sql, (row) => {
            if (content == "") {
                content = "<table>\n";
                content += "<tr><th>id</th><th>title</th><th>creator</th><th>path</th><th>mark</th><th>info</th><th>fav</th><th>count</th><th>bindata</th><th>date</th><th>sn</th></tr>";    
            }
            if (row == null) {
                content += "</table>\n";
                res.json({'message':tableName + " を降順で１００件表示しました。", 'content':content});
            }
            else {
                content += `<tr><td>${row.id}</td><td>${row.title}</td><td>${row.creator}</td><td>${row.path}</td><td>${row.mark}</td><td>${row.info}</td><td>${row.fav}</td><td>${row.count}</td><td>${row.bindata}</td><td>${row.DT}</td><td>${row.sn}</td></tr>\n`;
            }
        });
    }
    else if (tableName == "Creators") {
        sql = "SELECT id, creator, marks, info, fav, refcount, titlecount FROM Creators ORDER BY id DESC LIMIT 100";
        mysql.query(sql, (row) => {
            if (content == "") {
                content = "<table>\n";
                content += "<tr><th>id</th><th>creator</th><th>marks</th><th>info</th><th>fav</th><th>refcount</th><th>titlecount</th></tr>";    
            }
            if (row == null) {
                content += "</table>\n";
                res.json({'message':tableName + " を降順で１００件表示しました。", 'content':content});
            }
            else {
                content += `<tr><td>${row.id}</td><td>${row.creator}</td><td>${row.marks}</td><td>${row.info}</td><td>${row.fav}</td><td>${row.refcount}</td><td>${row.titlecount}</td></tr>\n`;
            }
        });
    }
    else if (tableName == "Album") {
        sql = "SELECT id, name, mark, info, bindata, groupname, DATE_FORMAT(`date`, '%Y-%m-%d') AS DT FROM Album ORDER BY id DESC LIMIT 100";
        mysql.query(sql, (row) => {
            if (content == "") {
                content = "<table>\n";
                content += "<tr><th>id</th><th>name</th><th>mark</th><th>info</th><th>bindata</th><th>groupname</th><th>date</th></tr>";    
            }
            if (row == null) {
                content += "</table>\n";
                res.json({'message':tableName + " を降順で１００件表示しました。", 'content':content});
            }
            else {
                content += `<tr><td>${row.id}</td><td>${row.name}</td><td>${row.mark}</td><td>${row.info}</td><td>${row.bindata}</td><td>${row.groupname}</td><td>${row.DT}</td></tr>\n`;
            }
        });
    }
    else if (tableName == "PictureAlbum") {
        sql = "SELECT id, album, title, path, creator, info, fav, bindata, picturesid, DATE_FORMAT(`date`, '%Y-%m-%d') AS DT, sn FROM PictureAlbum ORDER BY id DESC LIMIT 100";
        mysql.query(sql, (row) => {
            if (content == "") {
                content = "<table>\n";
                content += "<tr><th>id</th><th>album</th><th>title</th><th>path</th><th>creator</th><th>info</th><th>fav</th><th>bindata</th><th>picturesid</th><th>date</th><th>sn</th></tr>";    
            }
            if (row == null) {
                content += "</table>\n";
                res.json({'message':tableName + " を降順で１００件表示しました。", 'content':content});
            }
            else {
                content += `<tr><td>${row.id}</td><td>${row.album}</td><td>${row.title}</td><td>${row.path}</td><td>${row.creator}</td><td>${row.info}</td><td>${row.fav}</td><td>${row.bindata}</td><td>${row.picturesid}</td><td>${row.DT}</td><td>${row.sn}</td></tr>\n`;
            }
        });
    }
    else if (tableName == "BINDATA") {
        sql = "SELECT id, title, original, datatype, info, size, sn FROM BINDATA ORDER BY id DESC LIMIT 100";
        mysql.query(sql, (row) => {
            if (content == "") {
                content = "<table>\n";
                content += "<tr><th>id</th><th>title</th><th>original</th><th>datatype</th><th>info</th><th>size</th><th>sn</th></tr>";    
            }
            if (row == null) {
                content += "</table>\n";
                res.json({'message':tableName + " を降順で１００件表示しました。", 'content':content});
            }
            else {
                content += `<tr><td>${row.id}</td><td>${row.title}</td><td>${row.original}</td><td>${row.datatype}</td><td>${row.info}</td><td>${row.size}</td><td>${row.sn}</td></tr>\n`;
            }
        });
    }
    else if (tableName == "Videos") {
        sql = "SELECT id, album, title, path, creator, series, mark, info, fav, count, bindata, sn FROM Videos ORDER BY id DESC LIMIT 100";
        mysql.query(sql, (row) => {
            if (content == "") {
                content = "<table>\n";
                content += "<tr><th>id</th><th>album</th><th>title</th><th>path</th><th>creator</th><th>series</th><th>mark</th><th>info</th><th>fav</th><th>count</th><th>bindata</th><th>sn</th></tr>";
            }
            if (row == null) {
                content += "</table>\n";
                res.json({'message':tableName + " を降順で１００件表示しました。", 'content':content});
            }
            else {
                content += `<tr><td>${row.id}</td><td>${row.album}</td><td>${row.title}</td><td>${row.path}</td><td>${row.creator}</td><td>${row.series}</td><td>${row.mark}</td><td>${row.info}</td><td>${row.fav}</td><td>${row.count}</td><td>${row.bindata}</td><td>${row.sn}</td></tr>\n`;
            }
        });
    }
    else {
        res.json({'content':'<span style="color:red">エラー</span>', 'message':'エラー /view100?=' + tableName});
    }
});


/* パスが存在するかどうかを返す。*/
function existsPath(path) {
    return new Promise((resolve) => {
        fso.exists(path, (err) => {
            if (err) {
                resolve(false);
            }
            else {
                resolve(true);
            }
        });
    });
}


/* パスのチェックを行う。*/
function checkPath(req, res) {
    let badpaths = [];
    let table = req.query.table;
    let parts = req.query.range.split('-');
    let startId = parts[0];
    let endId = parts[1];
    let sql = `SELECT id, path FROM ${table} WHERE id BETWEEN ${startId} AND ${endId}`;
    mysql.query(sql, (row) => {
        if (row == null) {
            res.json(badpaths);        
        }
        else {
            let id = row.id;
            let path = row.path;
            if (!fso.exists(path)) {
                badpaths.push({'id':id, 'path':path});
            }           
        }
    });
}

/* tool: パスのチェック */
router.get('/check_paths', function(req, res,next) {
    checkPath(req, res);
});
  


/* エクスポート */
module.exports = router;
