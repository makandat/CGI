<?php
include "OOLib1.php";
include "MySQL.php";

// まんが作者一覧
class AddNewPage extends OOPHPLib\WebPage {

  // コンストラクタ
  public function __construct() {
    parent::__construct('addNew.html');

    if ($_POST['id'] != "") {
        // データを更新する。
        $need =False;
        $sql = "UPDATE Pictures SET ";
        if ($_POST['title'] != "") {
            $sql .= "title='".$_POST['title']."'"; $need=true;
        }
        if ($_POST['path'] != "") {
            if ($need) {
                $sql .= ",";
            }
            $sql .= "path='".$_POST['path']."'"; $need=true;
        }
        if ($_POST['creator'] != "") {
            if ($need) {
                $sql .= ",";
            }
            $sql .= "creator='".$_POST['creator']."'"; $need=true;
        }
        if ($_POST['info'] != "") {
            if ($need) {
                $sql .= ",";
            }
            $sql .= "info='".$_POST['info']."'"; $need=true;
        }
        if (isset($_POST['fav']) && $_POST['fav'] == "1") {
            if ($need) {
                $sql .= ",";
            }
            $sql .= "fav='1'"; $need=true;
        }
        else {
            if ($need) {
                $sql .= ",";
            }
            $sql .= "fav='0'"; $need=true;
        }
        $sql .= " WHERE id=".$_POST['id'];
        if ($need == false) {
            $this->v['message'] = "<span style='color:red;'>ERROR: 更新項目がありません。</span>";
            return;
        }
    }
    else {
        if ($_POST['title'] == "") {
            $this->v['message'] = "<span style='color:red;'>ERROR: TITLE 項目がありません。</span>";
            return;
        }
        if ($_POST['path'] == "") {
            $this->v['message'] = "<span style='color:red;'>ERROR: PATH 項目がありません。</span>";
            return;
        }
        if ($_POST['creator'] == "") {
            $this->v['message'] = "<span style='color:red;'>ERROR: CREATOR 項目がありません。</span>";
            return;
        }
        // データをテーブルに追加する。
        $sql = "INSERT INTO Pictures (TITLE, PATH, CREATOR, MARK, INFO, FAV) VALUES(";
        $sql .= "'" . $_POST['title'] . "',";
        $sql .= "'" . $_POST['path'] . "',";
        $sql .= "'" . $_POST['creator'] . "',";
        $sql .= "'" . $_POST['mark'] . "',";
        if (isset($_POST['info'])) {
             $sql .= "'" . $_POST['info'] . "',";
        }
        else {
             $sql .= "'',";
        }
        if (isset($_POST['fav']) && $_POST['fav'] == "1") {
            $sql .= "'1'";
        }
        else {
            $sql .= "'0'";
        }
        $sql .= ")";
    }
print $sql;
    $conn = new OOPHPLib\MySQL('AppConf.ini');
    if ($conn->execute($sql) == false) {
      $this->v['message'] = "<span style='color:red;'>ERROR: " . $conn->error . "</span>";
    }
    else if ($_POST['id'] != "") {
      $this->v['message'] = "OK: データを更新しました。(" . $_POST["id"] . ")";
    }
    else {
      $this->v['message'] = "OK: データを追加しました。(" . $_POST["title"] . ")";
    }
  }

}

// メインプログラム
$p = new AddNewPage();
$p->echo();
