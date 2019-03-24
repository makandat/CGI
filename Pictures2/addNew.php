<?php
include "WebPage.php";
include "MySQL.php";
include "FileSystem.php";

// 新規ページ追加
class AddNewPage extends WebPage {

  // コンストラクタ
  public function __construct($template) {
    parent::__construct($template);

    if ($this->getParam('id') != "") {
        // id 指定がある場合、データを更新する。
        $need =False;
        $sql = "UPDATE Pictures SET ";
        if ($this->getParam('title') != "") {
            $sql .= "title='".$this->quote2($this->getParam('title'))."'"; $need=true;
        }
        if ($this->getParam('path') != "") {
            if ($need) {
                $sql .= ",";
            }
            if (FileSystem\isFile($this->getParam('path')) == FALSE) {
                $this->setPlaceHolder('message', "<span style='color:red;'>ERROR: 指定したパスが存在しません。</span>");
                return;
            }
            if ($this->checkString($this->getParam('path'))) {
                $this->setPlaceHolder('message', "<span style='color:red;'>ERROR: パスに #, &, +, %, [ , ] が含まれていると画像表示に失敗します。</span>");
                return;
            }
            $sql .= "path='". $this->quote2($this->getParam('path')) ."'"; $need=true;
        }
        if ($this->getParam('creator') != "") {
            if ($need) {
                $sql .= ",";
            }
            $sql .= "creator='". $this->quote2($this->getParam('creator')) ."'"; $need=true;
        }
        if ($this->getParam('mark') != "") {
            if ($this->getParam('mark') != "0") {
                if ($need) {
                    $sql .= ",";
                }
                $sql .= "mark='".$this->getParam('mark') ."'"; $need=true;
            }
        }
        if ($this->getParam('info') != "") {
            if ($need) {
                $sql .= ",";
            }
            $sql .= "info='".$this->quote2($this->getParam('info')) ."'"; $need=true;
        }
        if ($this->getParam('fav') == "1") {
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
        $sql .= " WHERE id=".$this->getParam('id');
        if ($need == false) {
            $this->setPlaceHolder('message', "<span style='color:red;'>ERROR: 更新項目がありません。</span>");
            return;
        }
    }
    else {
        // id 指定がない場合、データを追加する。
        if ($this->getParam('title') == "") {
            $this->setPlaceHolder('message', "<span style='color:red;'>ERROR: TITLE 項目がありません。</span>");
            return;
        }
        if ($this->getParam('path') == "") {
            $this->setPlaceHolder('message', "<span style='color:red;'>ERROR: PATH 項目がありません。</span>");
            return;
        }
        if (FileSystem\isFile($this->getParam('path')) == FALSE) {
            $this->setPlaceHolder('message', "<span style='color:red;'>ERROR: 指定したパスが存在しません。</span>");
            return;
        }
        if ($this->checkString($this->getparam('path'))) {
            $this->setPlaceHolder('message', "<span style='color:red;'>ERROR: パスに #, &, +, %, [ , ] が含まれていると画像表示に失敗します。</span>");
            return;
        }
        if ($this->getParam('creator') == "") {
            $this->setPlaceHolder('message', "<span style='color:red;'>ERROR: CREATOR 項目がありません。</span>");
            return;
        }
        // データをテーブルに追加する。
        $sql = "INSERT INTO Pictures (TITLE, PATH, CREATOR, MARK, INFO, FAV) VALUES(";
        $sql .= "'" . $this->quote2($_POST['title']) . "',";
        $sql .= "'" . $this->quote2($_POST['path']) . "',";
        $sql .= "'" . $this->quote2($_POST['creator']) . "',";
        if ($this->getParam('mark') == "0") {
            $sql .= "'',";
        }
        else {
            $sql .= "'" . $this->getParam('mark') . "',";
        }
        if ($this->isParam('info')) {
             $sql .= "'" . $this->quote2($this->getParam('info')) . "',";
        }
        else {
             $sql .= "'',";
        }
        if ($this->getParam('fav') == "1") {
            $sql .= "'1'";
        }
        else {
            $sql .= "'0'";
        }
        $sql .= ")";
    }
#print $sql;
    $conn = new MySQL();
    # 追加の場合、すでに登録済みかチェックする。v3.20
    if (strpos($sql, "INSERT") == 0) {
       if ($this->checkPath($conn, $this->getParam('path'))) {
          $this->setPlaceHolder('message', "ERROR: すでに登録されています。(" . $this->getParam("path") . ")");
          return;
       }
    }
    # 追加または更新する。
    if ($conn->execute($sql) == false) {
      $this->setPlaceHolder('message', "<span style='color:red;'>ERROR: " . $conn->error . "</span>");
    }
    else if ($this->getParam('id') != "") {
      $this->setPlaceHolder('message',  "OK: データを更新しました。(" . $this->getParam("id") . ")");
    }
    else {
      $this->setPlaceHolder('message', "OK: データを追加しました。(" . $this->getParam("title") . ")");
    }
  }


    //  すでにパスが登録されているかチェックする。
    function checkPath($conn, $path) {
        $sql = "SELECT count(*) FROM Pictures WHERE `path`='$path'";
        $n = $conn->getValue($sql);
        return $n > 0;
    }

    //  特定文字が含まれているかチェックする。
    function checkString($str) {
        $r = !(strpos($str, "#") == FALSE && strpos($str, "&") == FALSE && strpos($str, "+") == FALSE && strpos($str, "%") == FALSE && strpos($str, "[") == FALSE && strpos($str, "]") == FALSE);
        return $r;
    }

    //  ' を '' に変換する。
    function quote2($str) {
        $s = str_replace("'", "''", $str);
        return $s;
    }
}

// メインプログラム
$p = new AddNewPage('templates/addNew.html');
$p->echo();
