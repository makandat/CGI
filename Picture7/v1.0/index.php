<?php
#
#  画像フォルダ用 PHP アプリケーション
#    v1.2
#
include "OOLib1.php";

define("INFO", 'info.csv');
define("TITLE", 'Picture7 v1.2');
define("THUMBS", 'thumbs');
define("PHDIR", "/home/user/pictures");

#
#  Index ページ
#  =============
class IndexPage extends OOPHPLib\WebPage {
  private $dir;
  private $phdir;
  private $info;

  # コンストラクタ
  public function __construct(string $filePath = null) {
    parent::__construct($filePath);

    # パラメータがあるか？
    if (isset($_REQUEST['path'])) {
      $this->dir = $_REQUEST['path'];
    }
    else {
      $this->dir = ".";
    }

    # 設定ファイルがあるか？
    if (OOPHPLib\File::exists('AppConf.ini')) {
      $this->phdir = $this->conf['phdir'];
    }
    else {
      $this->phdir = PHDIR;
    }

    # 情報ファイルを読み込む。
    $this->readInfo($this->dir);

    # 戻り先をセット
    $this->v['back'] = "index.php?path=" . OOPHPLib\Directory::getParentPath($this->dir);
    $this->v['top'] = "index.php?path=.";

    # タイトル
    $this->v['title'] = TITLE;

    # ディレクトリのファイル一覧を得る。
    $this->v['files'] = $this->listDirectories($this->dir);
  }

  #
  #  情報ファイルがあれば読み込む。
  #  =============================
  private function readInfo($dir) {
    if (OOPHPLib\File::exists($dir . '/' . INFO)) {
       $file = new SplFileObject($dir . '/' . INFO);
       $file->setFlags(SplFileObject::READ_CSV);
       $this->info = array();
       foreach ($file as $line) {
         $this->info[$line[0]] = $line[1];
       }
    }
    else {
      $this->info = null;
    }
  }

  #
  #  ディレクトリのファイル一覧 HTML を得る。
  #  =======================================
  private function listDirectories(string $path) : string {
    $this->v['folder'] = $path;
    $htm = '<ul>';
    $files = OOPHPLib\Directory::getSubDirectories($path);
    // thumbs フォルダがあるか
    if (in_array(THUMBS, $files)) {
      // あればサムネイル画像一覧を作成
      $this->v['folder'] = $path;
      $htm = $this->listThumbs($path . "/" . THUMBS);
    }
    else {
      // なければフォルダ一覧を作成
      foreach ($files as $f) {
        $htm .= "<li><a href=\"index.php?path=$path/$f\">";
        // ファイル情報があるか？
        if (isset($this->info[$f])) {
          $htm .= $this->info[$f];
        }
        else {
          $htm .= $f;
        }
        $htm .= "</a></li>\n";
      }
      $htm .= "</ul>\n";
    }
    return $htm;
  }

  #
  #  サムネイル画像一覧 HTML を作成
  #  ===============================
  private function listThumbs(string $path) : string {
    $vdir = str_replace($this->phdir, '', $path);
    $htm = '<ul>';
    $files = OOPHPLib\Directory::getFiles($path);
    $i = 0;
    foreach ($files as $f) {
      $path0 = substr($path, 0, strpos($path, "/".THUMBS));
      $htm .= "<a href=\"showImage.php?path=$path0/$f&index=$i\">";
      $htm .= "<img src=\"$vdir/$f\" />";
      $htm .= "</a>\n";
      $i++;
    }
    $htm .= "</ul>";
    return $htm;
  }
}

#
#  メインプログラム
#  =================
$page = new IndexPage("index.template");
$page->echo();
?>
