<?php
/* ディレクトリ内の画像一覧表示 */
include "WebPage.php";
include "MySQL.php";
include "FileSystem.php";

class ListImages extends WebPage {
  // コンストラクタ
  public function __construct($template) {
    parent::__construct($template);

    $dirname = $this->getParam('dirname');
    $title = $this->getParentDirectory($dirname);
    $this->setPlaceHolder('dirname', $dirname);
    $this->setPlaceHolder('title', $title);
    $this->setPlaceHolder('list', $this->listPics($_GET['dirname']));
    $this->setPlaceHolder('message', "");
    $this->incrementCount();
  }

  # 画像ファイル一覧をテーブル行として返す。
  private function listPics($dirname) : string {
    $buff = "";
    $files = FileSystem\getFiles($dirname);
    #print_r($files);

    foreach ($files as $fn) {
        $ext = strtolower(FileSystem\getExtension($fn));
        if ($ext == ".jpg" || $ext == ".png" || $ext == ".gif") {
            $path = $dirname . "/" . $fn;
            $img = "<img src='get_image.php?path=".$path."' style='width:20%;padding:2px;' />";
            $buff .="<a href='move_image.php?path=".$path."'>".$img."</a>\n";
        }
    }
    return $buff;
  }

  # COUNT を更新する。
  private function incrementCount() {
    $conn = new MySQL();
    $sql = "SELECT `count` FROM Pictures WHERE `path`='". $this->getPlaceHolder('dirname') . "'";
    $count = $conn->getValue($sql);
    $count++;
    $sql = "UPDATE Pictures SET COUNT=" . $count . " WHERE PATH='" . $this->getPlaceHolder('dirname') . "'";
    $conn->execute($sql);
  }

  private function getParentDirectory($dir) {
    $parts = preg_split('/\\//', $dir);
    $n = count($parts);
    return $parts[$n-1];
  }
  
}

// メインプログラム
$p = new ListImages('templates/listImages.html');
$p->echo();
?>
