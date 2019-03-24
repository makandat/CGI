<?php
include "WebPage.php";
include "FileSystem.php";
include "MySQL.php";

// 画像一覧クラス
class Pictures extends WebPage {

  // コンストラクタ
  public function __construct($template) {
    parent::__construct($template);
    // 条件指定があるか？
    if ($this->isParam('filterPath')) {
      $this->setPlaceHolder('table', $this->listManga("path LIKE '%" . $this->getParam('filterPath') . "%'"));
    }
    else if ($this->isParam('FAV')) {
        $this->setPlaceHolder('table', $this->listManga("FAV <> '0'"));
    }
    else if ($this->isParam('mark')) {
        $this->setPlaceHolder('table', $this->listManga("mark='".$this->getParam('mark')."'"));
    }
    else if ($this->isParam('info')) {
      $this->setPlaceHolder('table', $this->listManga("info LIKE '%" . $this->getparam('info') . "%'"));
    }
    else if ($this->isParam('creator') == "") {
      $this->setPlaceHolder('table', $this->listManga());
    }
    else {
      $this->setPlaceHolder('table', $this->listManga("CREATOR='".$this->getParam('creator')."'"));
    }
    $this->v['message'] = "";
  }

  // まんが一覧を取得する。
  private function listManga($criteria = null) {
    $strbuff = "";
    $conn = new MySQL();
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
        if (FileSystem\isDirectory($row['PATH'])) {
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
    $this->setPlaceHolder('message', '');
    return $strbuff;
  }
}

// メインプログラム
$p = new Pictures('templates/index.html');
$p->echo();

