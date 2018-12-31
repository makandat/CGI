<?php
#  MySQL class version 1.10
namespace OOPHPLib;

class MySQL {
  // 接続情報
  public $host;
  public $uid;
  public $pwd;
  public $db;
  public $error;

  // 接続オブジェクト
  public $mysqli;

  // コンストラクタ
  public function __construct(string $inifile='MySQLConnect.ini') {
    // INI ファイルを解析して接続情報を読む。
    $coninfo = parse_ini_file($inifile);
    if (isset($coninfo['host']))
      $this->host = $coninfo['host'];
    else
      $this->host = 'localhost';  // host 省略時は 'localhost'
    if (isset($coninfo['db']))
      $this->db = $coninfo['db'];
    else
      $this->db = 'information_schema';  // db 省略時は 'information_schema'
    $this->uid = $coninfo['uid'];
    $this->pwd = $coninfo['pwd'];

    // 接続オブジェクトを構築
    $this->mysqli = new \mysqli($this->host, $this->uid, $this->pwd, $this->db);
    // エラーコードを格納。正常なら 0
    $this->error = $this->mysqli->connect_errno;
    // UTF-8 を使うように設定する。
    $this->mysqli->set_charset('utf8');
  }

  // デストラクタ
  function __destruct() {
    if ($this->error == 0)
      $this->mysqli->close();
  }

  // 接続を閉じる。
  public function close() {
    if ($this->error == 0) {
       $this->mysqli->close();
       $this->error = -1;
    }
  }

  // 接続を開く。
  public function open(string $db) {
    if ($this->error == 0)
       $this->close();
    $this->db = $db;
    // 接続オブジェクトを構築
    $this->mysqli = new mysqli($this->host, $this->uid, $this->pwd, $this->db);
    // エラーコードを格納。正常なら 0
    $this->error = $mysqli->connect_errno;
  }

  // SELECT クエリーを行う。
  public function query(string $sql) : array {
    $result = array();
    if ($q = $this->mysqli->query($sql)) {
      while ($row = $q->fetch_assoc()) {
        array_push($result, $row);
      }
      $q->close();
    }
    return $result;
  }

  // １つの値を返す SELECT クエリーを行う。
  public function getValue(string $sql) {
    $dt = $this->query($sql);

    if (count($dt) > 0) {
      $row = $dt[0];
      $result = $row[0];
    }

    return $result;
  }

  // 非 SELECT クエリーを行う。
  public function execute(string $sql) : bool {
    return ($this->mysqli->query($sql) == 0);  // Bug corrected on 2016/10/03
  }

  // 最後に実行したSQLのエラーメッセージを返す。
  public function getLastError() {
    return $this->mysqli->error;
  }
}

?>
