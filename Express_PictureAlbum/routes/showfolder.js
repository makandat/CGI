/* showfolder.js */
'use strict';
var express = require('express');
var session = require('express-session');
var fso = require('./FileSystem.js');
var mysql = require('./MySQL.js');
var os = require('os');
var path_module = require('path');
var router = express.Router();


/* 画像ナビ表示 (移動) */
function moveImage(res, move, dir) {
    if (os.platform() == "win32")
        dir = dir.replace(/\\/g, '/');
    fso.getFiles(dir, ['.jpg', '.JPG', '.png', '.gif', '.jpeg'], (files)=>{
        let last = files.length - 1;
        let n = session.navimg;
        switch (move) {
            case "first":
                n = 0;
                break;
            case "prev":
                n = (n <= 0) ? 0 : n - 1;
                break;
            case "next":
                n = (n >= last) ? last : n + 1;
                break;
            case "last":
                n = last;
                break;
            default:
                n = 0;
                break;
        }
        session.navimg = n;
        let path = files[n];
        let parts = dir.split(/[\\|\/]/g);
        let title = parts[parts.length-1];
        let message = (n + 1).toString() + " / " + files.length.toString() + ": " + path;
        res.render('showNavImage', {'title':title, 'message':message, 'path':path, 'dir':dir});
    });
}

/* 画像ナビ表示 (画像指定) */
function jumpImage(res, n, dir) {
    session.navimg = n;
    if (os.platform() == "win32")
        dir = dir.replace(/\\/g, '/');
    fso.getFiles(dir, ['.jpg', '.JPG', '.png', '.gif', '.jpeg'], (files)=>{
        let path = files[n];
        let parts = dir.split(/[\\|\/]/g);
        let title = parts[parts.length-1];
        let message = (n + 1).toString() + " / " + files.length.toString() + ": " + path
        res.render('showNavImage', {'title':title, 'message':message, 'path':path, 'dir':dir});
    });
}



/* デフォルトの表示 /showfolder */
router.get('/', function(req, res, next) {
    let dir = req.query.path;
    let reverse = req.query.reverse;

    if (req.session.showfolder_desc == undefined) {
        req.session.showfolder_desc = false;
    }
    else {
        if (reverse) {
            req.session.showfolder_desc = ! req.session.showfolder_desc;
        }
    }
    if (dir == undefined) {
        res.render('showfolder', {'title':'エラー', 'message':'フォルダが指定されていません。', 'dir':'', 'files':[], 'id':0});
    }
    else if (! fso.exists(dir)) {
        res.render('showfolder', {'title':'エラー', 'message':'フォルダが存在しません。', 'dir':'', 'files':[], 'id':0});
    }
    else {
        mysql.getValue(`SELECT id FROM Pictures WHERE path='${dir}'`, (id) => {
            let parts = dir.split(/[\/|\\]/g);
            let title = parts[parts.length-1]
            fso.getFiles(dir, ['.jpg', '.JPG', '.png', '.gif', '.jpeg'], (files) => {
                let files1 = files.sort();
                if (req.session.showfolder_desc) {
                    files1 = files.reverse();
                }
                mysql.execute(`CALL IncreaseCount(${id})`, () => {
                    res.render('showfolder', {'title':title, 'message':'画像をクリックしてファイルリストを作成できます。', 'dir':dir, 'files':files1, 'id':id});
                });
            });
        });
    }
});

/* サムネール表示 */
router.get('/thumbs', function(req, res, next) {
    let dir = req.query.path;

    if (dir == undefined) {
        res.render('showthumb', {'title':'エラー', 'message':'フォルダが指定されていません。', 'dir':'', 'files':[]});
    }
    else {
        let parts = dir.split(/[\/|\\]/g);
        let title = parts[parts.length-1]
        fso.getFiles(dir, ['.jpg', '.JPG', '.png', '.gif', '.jpeg'], (files)=>{
            let files1 = files.sort();
            res.render('showthumb', {'title':title, 'message':'', 'dir':dir, 'files':files1});
        });
    }
});

/* 画像ナビゲート表示 */
router.get('/nav/:move', function(req, res, next) {
    let move = req.params.move;

    let n = parseInt(move);
    if (isNaN(n)) {
        moveImage(res, move, session.dir);
    }
    else {
        jumpImage(res, n, session.dir);
    }
});

/* 画像ナビゲート表示 (初期画像) */
router.get('/navinit', function(req, res, next){
    let path = req.query.path;
    let dir = fso.getDirectory(path);
    session.dir = dir;
    let n = 0;
    fso.getFiles(dir, ['.jpg', '.JPG', '.png', '.gif', '.jpeg'], (files) => {
        for (let i = 0; i < files.length; i++) {
            if (os.platform() == "win32") {
                files[i] = files[i].replace(/\\/g, '/');
            }
            if (path == files[i]) {
                n = i;
                break;
            }
        }
        jumpImage(res, n, dir);
    });
});

/* エクスポート */
module.exports = router;

