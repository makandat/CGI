<?php
/* ディレクトリ内の画像一覧表示 */
include "OOLib1.php";
include "MySQL.php";

class ListImages extends OOPHPLib\WebPage {
  // コンストラクタ
  public function __construct($template) {
    parent::__construct($template);
    
    $this->v['dirname'] = $_GET['dirname'];
    $this->v['list'] = $this->listPics($_GET['dirname']);
    $this->v['message'] = "";
    $this->incrementCount();
  }
  
  # 画像ファイル一覧をテーブル行として返す。
  private function listPics($dirname) : string {
    #print($dirname);
    $buff = "";
    $files = OOPHPLib\Directory::getFiles($dirname);
      
    foreach ($files as $fn) {
        $ext = strtolower(OOPHPLib\File::getExtension($fn));
        if ($ext == "jpg" || $ext == "png" || $ext == "gif") {
            $path = $dirname . "/" . $fn;
            $img = "<img src='get_image.php?path=".$path."' style='width:10%;padding:2px;' />";
            $buff .="<a href='move_image.php?path=".$path."'>".$img."</a>\n";
        }
    }
    return $buff;
  }

  # COUNT を更新する。
  private function incrementCount() {
    $conn = new OOPHPLib\MySQL('AppConf.ini');
    $sql = "SELECT COUNT FROM Pictures WHERE PATH='". $this->v['dirname'] . "'";
    $count = $conn->getValue($sql);
    $count++;
    $sql = "UPDATE Pictures SET COUNT=" . $count . " WHERE PATH='" . $this->v['dirname'] . "'";
    $conn->execute($sql);
  }
}

// メインプログラム
$p = new ListImages('listImages.html');
$p->echo();
?>
