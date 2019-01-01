<?php
include "OOLib1.php";
include "MySQL.php";

// 画像一覧クラス
class Pictures extends OOPHPLib\WebPage {

  // コンストラクタ
  public function __construct() {
    parent::__construct("index.html");
    // 条件指定があるか？
    if (isset($_GET['filterPath'])) {
      $this->v['table'] = $this->listManga("path LIKE '%" . $_GET['filterPath'] . "%'");
    }
    else if (isset($_GET['FAV'])) {
        $this->v['table'] = $this->listManga("FAV <> '0'");
    }
    else if (isset($_GET['mark'])) {
        $this->v['table'] = $this->listManga("mark='".$_GET['mark']."'");
    }
    else if (isset($_GET['info'])) {
      $this->v['table'] = $this->listManga("info LIKE '%" . $_GET['info'] . "%'");
    }
    else if ($_GET['creator'] == "") {
      $this->v['table'] = $this->listManga();
    }
    else {
      $this->v['table'] = $this->listManga("CREATOR='".$_GET['creator']."'");
    }
    $this->v['message'] = "";
  }

  // まんが一覧を取得する。
  private function listManga($criteria = null) {
    $strbuff = "";
    $conn = new OOPHPLib\MySQL('AppConf.ini');
    $sql = "SELECT * FROM Pictures";
    if (isset($criteria)) {
      $sql .= " WHERE " . $criteria;
    }
    $sql .= " ORDER BY id DESC LIMIT 500";
    $dataTable = $conn->query($sql);
    if (count($dataTable) > 0) {
      $strbuff .= "<table style='width:100%;'>\n<tr><th>ID</th><th>タイトル</th><th>作者</th><th>種別</th><th>備考</th>".
      "<th>お気に入り</th><th>閲覧回数</th></tr>\n";
      foreach ($dataTable as $row) {
        $strbuff .= "<tr>";
        $strbuff .= "<td class='bdr'>" . $row['ID'] . "</td>";
        if (OOPHPLib\File::isDirectory($row['PATH'])) {
            $strbuff .= "<td class='bdr'><a href='listImages.php?dirname=" . $row['PATH'] . "' target='_blank'>" . $row['TITLE'] . "</a></td>";
        }
        else {
            $strbuff .= "<td class='bdr'><a href='get_image.php?path=" . $row['PATH'] . "' target='_blank'>" . $row['TITLE'] . "</a></td>";
        }
        $strbuff .= "<td class='bdr'><a href='index.php?creator=" . $row['CREATOR'] . "'>" .$row['CREATOR']. "</a></td>";
        $strbuff .= "<td class='bdr'>" . $row['MARK'] . "</td>";
        $strbuff .= "<td class='bdr'>" . $row['INFO'] . "</td>";
        $strbuff .= "<td class='bdr'>" . $row['FAV'] . "</td>";
        $strbuff .= "<td class='bdr'>" . $row['COUNT'] . "</td>";
        $strbuff .= "</tr>\n";
      }
      $strbuff .= "</table>\n";
    }
    else {
      $strbuff .= "<p style='color:red;margin-left:5%;'>エラー：データがありません。</p>";
    }
    return $strbuff;
  }
}

// メインプログラム
$p = new Pictures();
$p->echo();

