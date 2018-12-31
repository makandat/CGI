<?php
# Videos フォルダ用 PHP アプリケーション
include "OOLib1.php";

define("PHDIR", "/home/user/videos");   # 物理ディレクトリ
define("VIRDIR", "/videos");            # 仮想ディレクトリ
define("INFO", "info.csv");             # 情報ファイル
#
#  Index ページ
#  =============
class IndexPage extends OOPHPLib\WebPage {
  private $dir;
  private $vdir;
  private $phdir;
  private $info;

  # コンストラクタ
  public function __construct(string $filePath = null) {
    parent::__construct($filePath);

    # 設定情報があるか？
    if (isset($this->conf['physicalFolder'])) {
      $this->phdir = $this->conf['physicalFolder'];
    }
    else {
      $this->phdir = PHDIR;
    }

    if (isset($this->conf['virtualFolder'])) {
      $this->vdir = $this->conf['virtualFolder'];
    }
    else {
      $this->vdir = VIRDIR;
    }

    # パラメータがあるか？
    if (isset($_REQUEST['path'])) {
      $this->dir = $_REQUEST['path'];
    }
    else {
      $this->dir = $this->phdir;
    }

    # 戻り先をセット
    if ($this->dir == $this->phdir) {
      $this->v['back'] = "";
    }
    else {
      $this->v['back'] = "index.php?path=" . OOPHPLib\Directory::getParentPath($this->dir);
    }
    $this->v['top'] = "index.php?path=.";

    # タイトル
    $this->v['title'] = "Video viewer 7";

    # ディレクトリのファイル一覧を得る。
    $this->v['group'] = $this->vdir . str_replace($this->phdir, '', $this->dir);
    $this->v['files'] = $this->listDirectories($this->dir);
  }

  # ディレクトリのファイル一覧 HTML を得る。
  private function listDirectories(string $path) : string {
    $files = OOPHPLib\Directory::getSubDirectories($path);
    // サブフォルダがあるか
    if (count($files) == 0) {
      // なければビデオファイル (*.mp4) 一覧を作成
      $htm = $this->listMP4($path);
    }
    else {
      // 情報ファイルがあれば読み込む。
      $this->readInfo($path);
      // なければフォルダ一覧を作成
      foreach ($files as $f) {
        $htm .= "<li><a href=\"index.php?path=$this->phdir/$f\">";
        if (isset($this->info)) {
          $htm .= $this->info[$f] == '' ? $f : $this->info[$f];
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
  #  ビデオファイル (*.mp4) 一覧 HTML を作成
  #  ========================================
  private function listMP4(string $path) : string {
    
    $htm = '';
    $files = OOPHPLib\Directory::getFiles($path, '*.mp4');
    $path0 = str_replace($this->phdir, $this->vdir, $path);
    $this->readInfo($path);
    foreach ($files as $f) {
      if (isset($this->info)) {
        $title = isset($this->info[$f]) ? $this->info[$f] : $f;
      }
      else {
        $title = $f;
      }
      $htm .= "<li><a href=\"$path0/$f\" target=\"_blank\">$title</a></li>";
    }
    return $htm;
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
}

# メインプログラム
$page = new IndexPage("index.template");
$page->echo();
?>
