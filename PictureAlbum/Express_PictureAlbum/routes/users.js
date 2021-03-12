'use strict';
/* users.js */
var express = require('express');
var router = express.Router();

var mysql = require('./MySQL.js');
var dt = require('./DateTime.js');

const MESSAGE0 = '正しいユーザIDとパスワードを入力して「ログイン」ボタンをクリックしてください。';
const MESSAGE1 = 'ログイン失敗： ユーザIDとパスワードを再確認してログインし直してください。';


/* デフォルトのリクエスト */
router.get('/', (req, res) => {
    if (req.query.force) {
        res.render('login', {'message':MESSAGE0, 'userid':'', 'password':''});
    }
    else if (req.session.user == undefined) {
        res.render('login', {'message':MESSAGE0, 'userid':'', 'password':''});
    }
    else if (req.query.from) {
        let from = req.query.from;
        res.redirect('/' + from);
    }
    else {
        res.redirect('/');
    }
});

/* ページのリクエスト */
router.get('/page', (req, res) => {
    if (req.session.user == undefined) {
        res.render('login', {'message':MESSAGE0, 'userid':'', 'password':''});
    }
    else {
        let pageurl = req.query.page;
        if (pageurl == undefined || pageurl == "") {
            pageurl = "/";
        }
        res.redirect(pageurl);
    }
});

/* LOGIN リクエスト */
router.post('/login', (req, res) => {
    let {userid, password, page} = req.body;
    if (userid == "" || password == "") {
        req.session.user = undefined;
        res.render("showInfo", {'title':'エラー', 'message':MESSAGE0, 'icon':'cancel.png', 'link':'<a href="/users">ログイン</a>'});
        return;
    }
    let sql = "SELECT `password`, expired FROM Users WHERE userid='" + userid + "'";
    mysql.getRow(sql, (row) => {
        if (row.password == password && row.expired == '0') {
            req.session.user = userid;
            switch (page) {
                case "AlbumGroup":
                    res.redirect('/album_group.html');
                    break;
                case "Pictures":
                    res.redirect('/pictures');
                    break;
                case "Videos":
                    res.redirect('/video');
                    break;
                default:
                    res.redirect('/');
                    break;
            }
        }
        else {
            res.render('login', {'message':MESSAGE1, 'userid':'', 'password':''});
        }
    });
});


/* ログアウト */
router.get('/logout', (req, res) => {
    req.session.user = undefined;
    res.render('showInfo', {title:"ログアウト", message:'ログアウトしました。', icon:"info.png", link:'<a href="/users?force=yes">再びログインする。</a>'});
});




/* ユーザ管理 */
router.get('/admin', (req, res) => {
    // 管理者かチェックする。
    let userid = req.query.userid;
    let password = req.query.password;
    let results = [];
    mysql.getRow(`SELECT password, priv FROM Users WHERE userid = '${userid}'`, (row) => {
        if (row.priv == '2' && row.password == password) {
            mysql.query("SELECT * FROM Users", (row) => {
                if (row == null) {
                    req.session.userid = userid;
                    res.render('userlist', {title:"ユーザ管理 " + userid, results:results});
                }
                else {
                    results.push([row.id, row.userid, row.password, row.priv, row.info, row.registered, row.expired]);
                }
            })
        }
        else {
            res.render('showInfo', {title:"エラー", message:"この機能は管理者のみ使用できます。", icon:"cancel.png", link:null});
        }
    });
});


/* ユーザを登録する。*/
function insertUser(req, res) {
    let {userid, password, priv, info, registered, expired} = req.body;
    if (registered == "") {
        registered = dt.getDateString();
    }
    let sql = `INSERT INTO Users VALUES(NULL, '${userid}', '${password}', '${priv}', '${info}', '${registered}', '${expired}')`;
    mysql.execute(sql, () => {
        let checked0, checked1, checked2, checked3;
        if (expired == "0") {
            checked0 = "checked";
            checked1 = "";
        }
        else {
            checked0 = "";
            checked1 = "checked";
        }
        if (priv == "1") {
            checked2 = "checked";
            checked3 = "";
        }
        else {
            checked2 = "";
            checked3 = "checked";
        }
        res.render('user_addmodify', {message:"ユーザ " + userid + " が登録されました。", id:"", userid:userid, password:password,
           priv:priv, info:info, registered:registered, expired:expired, checked0:checked0, checked1:checked1, checked2:checked2, checked3:checked3});
    });
}

/* ユーザ情報を更新する。*/
async function updateUser(req, res) {
    let {id, userid, password, priv, info, registered, expired} = req.body;
    let sql = `UPDATE Users SET userid='${userid}', password='${password}', priv='${priv}', info='${info}', registered='${registered}', expired='${expired}' WHERE id=${id}`;
    mysql.execute(sql, () => {
        let checked0, checked1, checked2, checked3;
        if (expired == "0") {
            checked0 = "checked";
            checked1 = "";
        }
        else {
            checked0 = "";
            checked1 = "checked";
        }
        if (priv == "1") {
            checked2 = "checked";
            checked3 = "";
        }
        else {
            checked2 = "";
            checked3 = "checked";
        }
        res.render('user_addmodify', {message:"ユーザ " + userid + " の情報が更新されました。", id:id, userid:userid, password:password, priv:priv,
          info:info, registered:registered, expired:expired, checked0:checked0, checked1:checked1, checked2:checked2, checked3:checked3});
    });
}


/* ユーザ登録・修正 (POST) */
router.post('/add_modify', (req, res) => {
    if (req.session.userid == undefined) {
        res.render('showInfo', {title:"エラー", message:"ログインが必要です。", icon:"cancel.png", link:'<a href="/users">ログイン</a>'});
        return;
    }
    let id = req.body.id;
    if (id == "") {
        // 登録
        insertUser(req, res);
    }
    else {
        // 修正
        updateUser(req, res);
    }
});

/* ユーザ登録・修正 (GET) */
router.get('/add_modify', (req, res) => {
    if (req.session.userid == undefined) {
        res.render('showInfo', {title:"エラー", message:"ログインが必要です。", icon:"cancel.png", link:'<a href="/users">ログイン</a>'});
        return;
    }
    res.render('user_addmodify', {message:"番号(id)が空欄の場合は追加になります。空欄でない場合は更新となります。追加の場合、登録日は空欄で構いません。", id:"", userid:"",
     password:"", priv:"1", info:"", registered:"", expired:"0", checked0:"checked", checked1:"", checked2:"checked", checked3:""});
});

/* ユーザ情報確認 */
router.get('/confirm/:id', (req, res) => {
    if (req.session.userid == undefined) {
        res.render('showInfo', {title:"エラー", message:"ログインが必要です。", icon:"cancel.png", link:'<a href="/users">ログイン</a>'});
        return;
    }
    let id = req.params.id;
    mysql.getRow("SELECT * FROM Users WHERE id=" + id, (row) => {
        let checked0, checked1, checked2, checked3;
        if (row.expired == "0") {
            checked0 = "checked";
            checked1 = "";
        }
        else {
            checked0 = "";
            checked1 = "checked";
        }
        if (row.priv == "1") {
            checked2 = "checked";
            checked3 = "";
        }
        else {
            checked2 = "";
            checked3 = "checked";
        }
        res.render('user_addmodify',{message:"id = " + id + " が検索されました。", id:row.id, userid:row.userid, password:row.password, priv:row.priv,
         info:row.info, registered:row.registered, expired:row.expired, checked0:checked0, checked1:checked1, checked2:checked2, checked3:checked3});
    });
});




/* エクスポート */
module.exports = router;
