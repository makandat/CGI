/* MySQL.js v1.10 */
"use strict";
var mysql = require("mysql");
var fs = require("fs");

/* "mysql.json" から接続情報を読み取る。(ヘルパ関数) */
var getConf = () => {
  let confstr = fs.readFileSync("mysql.json", "utf-8");
  let conf = JSON.parse(confstr);
  return conf;
}


/* 結果セットを返すクエリー関数 */
/*  callback は結果の行数回コールされ、最後に null が返される。*/
exports.query = (sql, callback, conf = null) => {
  if (conf == null) {
    conf = getConf();
  }
  let conn = mysql.createConnection(conf);
  conn.query(sql, (error, results, fields) => {
    if (error) {
      throw error;
    }
    else {
       for (let i = 0; i < results.length; i++) {
         callback(results[i], fields);
       }
       callback(null);
       conn.end();
    }
  });
}

/* コマンドを実行するクエリ関数. INSERT,DELETE,UPDATE などの場合 */
/*  callback は１回だけコールされる。値は何も返さない。*/
exports.execute = (sql, callback, conf = null) => {
  if (conf == null) {
    conf = getConf();
  }
  let conn = mysql.createConnection(conf);
  conn.query(sql, (error, results, fields)=>{
      if (error) {
        throw error;
      }
      else {
         callback();
         conn.end();
      }
  });
}

/* １つの値（スカラー）を返すクエリ関数. sql は1つの値を返すものであること。 */
exports.getValue = (sql, callback, conf = null) => {
  if (conf == null) {
    conf = getConf();
  }
  let conn = mysql.createConnection(conf);
  conn.query(sql, (error, results, fields)=>{
      if (error) {
        throw error;
      }
      else {
         let row = results[0];
         let key = fields[0].name;
         let value = row[key];
         callback(value);
         conn.end();
      }
  });
}

/* １つの行を返すクエリ関数。クエリ結果が複数行の場合は先頭行を返す。*/
exports.getRow = (sql, callback, conf = null) => {
  if (conf == null) {
    conf = getConf();
  }
  let conn = mysql.createConnection(conf);
  conn.query(sql, (error, results, fields)=>{
      if (error) {
        throw error;
      }
      else {
         callback(results[0], fields);
         conn.end();
      }
  });
}
