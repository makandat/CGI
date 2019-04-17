<?php
require_once "MySQL.php";

//
//  MySQL INFORMATION_SCHEMA 情報
//
class MySQLInfo extends MySQL {

  // データベース一覧を得る。
  public function getDatabases() {
    $sql = "SELECT * FROM INFORMATION_SCHEMA.SCHEMATA ORDER BY SCHEMA_NAME";
    $databases = $this->query($sql);
    return $databases;
  }

  // ユーザ一覧を得る。
  public function getUsers() {
    $sql = "SELECT DISTINCT GRANTEE FROM INFORMATION_SCHEMA.USER_PRIVILEGES ORDER BY GRANTEE";
    $users = $this->query($sql);
    return $users;
  }

  // テーブル一覧を得る。
  public function getTables($schema) {
    $sql = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='" . $schema ."'";
    $tables = $this->query($sql);
    return $tables;
  }

  // ビュー一覧を得る。
  public function getViews($schema) {
    $sql = "SELECT * FROM INFORMATION_SCHEMA.VIEWS WHERE TABLE_SCHEMA='" . $schema ."'";
    $views = $this->query($sql);
    return $views;
  }

  // ビューの定義を得る。
  public function getViewDef($schema, $view) : string {
    $sql = "SELECT VIEW_DEFINITION FROM INFORMATION_SCHEMA.VIEWS WHERE TABLE_SCHEMA='" . $schema ."' AND TABLE_NAME='" . $view . "'";

    $result = $this->query($sql);
    if (count($result) > 0) {
      $row = $result[0];
      return $row['VIEW_DEFINITION'];
    }
    else
      return '';
  }

  // ルーチン一覧を得る。
  public function getRoutines($schema) {
    $sql = "SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_SCHEMA='" . $schema ."'";
    $routines = $this->query($sql);
    return $routines;
  }

  // ルーチンの定義を得る。
  //   PARAM_LIST, RETURNS, BODY フィールド
  public function getRoutineDef($schema, $routine) {
    $sql = "SELECT * FROM mysql.proc WHERE DB='" . $schema ."' AND NAME='" . $routine . "'";
    $result = $this->query($sql);
    return $result;
  }

  // トリガ一覧を得る。
  public function getTriggers($schema) {
    $sql = "SELECT * FROM INFORMATION_SCHEMA.TRIGGERS WHERE TRIGGER_SCHEMA='" . $schema ."'";
    $triggers = $this->query($sql);
    return $triggers;
  }

  // トリガの定義を得る。
  public function getTriggerDef($schema, $trigger) {
    $sql = "SELECT ACTION_STATEMENT FROM INFORMATION_SCHEMA.TRIGGERS WHERE TRIGGER_SCHEMA='". $schema ."' AND TRIGGER_NAME='". $trigger ."'";
    $result = $this->getValue($sql);
    return $result;
  }

  // カラム一覧を得る。
  public function getColumns($schema, $tableName) {
    $sql = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='" . $schema ."' AND TABLE_NAME='" . $tableName . "'";
    $columns = $this->query($sql);
    return $columns;
  }

  // インデックス一覧を得る。
  public function getIndexes($schema) {
    $sql = "SELECT * FROM INFORMATION_SCHEMA.STATISTICS WHERE INDEX_SCHEMA='" . $schema . "'";
    $indexes = $this->query($sql);
    return $indexes;
  }

  // 文字コード一覧を得る。
  public function getCharacterSets() {
    $sql = "SELECT * FROM INFORMATION_SCHEMA.CHARACTER_SETS";
    $this->charactersets = $this->query($sql);
    return $this->charactersets;
  }

  // 比較順序一覧を得る。
  public function getCollations() {
    $sql = "SELECT * FROM INFORMATION_SCHEMA.COLLATIONS";
    $collations = $this->query($sql);
    return $collations;
  }
}

?>
