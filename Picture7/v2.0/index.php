<?php
#
# 画像フォルダ用 PHP アプリケーション
#   v2.2
include "OOLib1.php";

define("THUMBS", 'thumbs');
define("INFO", 'info.csv');
define("PHDIR", "/var/www/html/php/Picture7");
define("TITLE", "Picture viewer 7 v2.2");

#
#  Index ページ
#  =============
class IndexPage extends OOPHPLib\WebPage {
  private $dir;
  private $thumb;
  private $pictures;
  private $vdir;
  private $info;

  # コンストラクタ
  public function __construct(string $filePath = null) {
    parent::__construct($filePath);

    # サムネイルフォルダ名
    if (isset($this->conf['thumbFolder'])) {
      $this->thumb = $this->conf['thumbFolder'];
    }
    else {
      $this->thumb = THUMBS;
    }

    # 画像フォルダ (Physical folder)
    if (isset($this->conf['pictureFolder'])) {
      $this->pictures = $this->conf['pictureFolder'];
    }
    else {
      $this->pictures = PHDIR;
    }

    # 画像フォルダ (Virtual folder)
    if (isset($this->conf['pictureVirtual'])) {
      $this->vdir = $this->conf['pictureVirtual'];
    }
    else {
      $this->vdir = PHDIR;
    }

    # パラメータがあるか？
    if (isset($_REQUEST['path'])) {
      # path パラメータあり。
      $this->dir = $_REQUEST['path'];
    }
    else if (isset($this->conf['pictureFolder'])) {
      # パラメータなし、設定ファイルに baseFoder あり。
      $this->dir = $this->pictures;
    }
    else {
      # パラメータなし、設定ファイルに baseFoder なし。
      $this->dir = ".";
    }

    # 情報ファイルを読み込む。
    $this->readInfo($this->dir);

    # 戻り先をセット
    #  BACK リンク
    if (isset($_REQUEST['path'])) {
      if ($this->dir == $this->pictures) {
        $parentFolder = $this->pictures;
      }
      else {
        $parentFolder = OOPHPLib\Directory::getParentPath($this->dir);
      }
      $this->v['back'] = "index.php?path=" . $parentFolder;
    }
    else {
      $this->v['back'] = $this->dir;
    }
    # TOP リンク
    $this->v['top'] = "index.php?path=" . $this->pictures;

    # タイトル
    $this->v['title'] = TITLE;

    # ディレクトリのファイル一覧を得る。
    $this->v['folder'] = $this->dir;
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
  #  ========================================
  private function listDirectories(string $path) : string {
    $htm = '';
    $files = OOPHPLib\Directory::getSubDirectories($path);
    // thumbs フォルダがあるか
    if (in_array($this->thumb, $files)) {
      // あればサムネイル画像一覧を作成
      $htm = $this->listThumbs($path . "/" . $this->thumb);
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
    }
    return $htm;
  }

  #
  #  サムネイル画像一覧 HTML を作成
  #  ==============================
  private function listThumbs(string $path) : string {
    $htm = '';
    $subdir = str_replace($this->pictures, '', $path);
    $vdir = $this->vdir;
    $files = OOPHPLib\Directory::getFiles($path);
    $i = 0;
    $_SESSION['count'] = count($files);
    foreach ($files as $f) {
      $path0 = substr($path, 0, strpos($path, "/" . $this->thumb));
      $htm .= "<a href=\"showImage.php?path=$path0/$f&index=$i\">";
      $htm .= "<img src=\"$vdir$subdir/$f\" />";
      $htm .= "</a>\n";
      $i++;
    }
    return $htm;
  }
}

# メインプログラム
$page = new IndexPage("index.template");
$page->echo();
?>
