<?php
# 画像フォルダ用 PHP アプリケーション
#  - 画像表示  v2.2
include "OOLib1.php";

# 画像表示画面
class ShowImagePage extends OOPHPLib\WebPage {
  private $pictureFolder;
  private $pictureVirtual;

  # コンストラクタ
  public function __construct(string $filePath = null) {
    parent::__construct($filePath);

    $this->v['title'] = '画像表示';
    if (isset($this->conf['pictureFolder'])) {
      $this->pictureFolder = $this->conf['pictureFolder'];
    }
    else {
      $this->pictureFolder = ".";
    }
    if (isset($this->conf['pictureVirtual'])) {
      $this->pictureVirtual = $this->conf['pictureVirtual'];
    }
    else {
      $this->pictureVirtual = ".";
    }

    # 画像
    if (isset($_REQUEST['path']) && isset($_REQUEST['index'])) {
      if (strpos($_REQUEST['path'], " ") > 0) {
        $path = $_REQUEST['path'];
      }
      else {
        $path = urldecode($_REQUEST['path']);
      }
      $index = $_REQUEST['index'];
      # 画像
      $this->v['image'] = str_replace($this->pictureFolder, $this->pictureVirtual, $path);
      # タイトル
      $this->v['title'] = OOPHPLib\File::getDirectory($path);
      # メッセージ
      $this->v['message'] = OOPHPLib\File::getFileName($path);
      # ナビゲーション
      $currentDir = OOPHPLib\File::getDirectory($path);
      $parentDir = OOPHPLib\Directory::getParentPath($path);
      $this->v['back'] = "index.php?path=" . $parentDir;
      $this->v['top'] = ".";
      # 画像一覧を得る。
      $files = OOPHPLib\Directory::getFiles($currentDir);
      if ($index - 1 < 0) {
        $index = 1;
      }
      if (count($files) == $index + 1) {
        $this->v['message'] = "<b>Last Image: " . OOPHPLib\File::getFileName($path) . "</b>";
      }
      else {
        $this->v['message'] = OOPHPLib\File::getFileName($path);
      }
      $this->v['prev'] = "showImage.php?path=$currentDir/" . $files[$index - 1] . "&index=" . ($index - 1);
      $index = $_REQUEST['index'];
      if (count($files) - 1 <= $index) {
        $index = count($files) - 2;
      }
      $this->v['next'] = "showImage.php?path=$currentDir/" .  $files[$index + 1] . "&index=" . ($index + 1);
    }
    else {
      $this->v['message'] = 'エラー：画像の指定がありません。';
      $this->v['image'] = "/img/LoveLive.png";
      # ナビゲーション
      $this->v['back'] = '#';
      $this->v['top'] = ".";
      $this->v['prev'] = '#';
      $this->v['next'] = '#';
    }
  }
}

# メインプログラム
$page = new ShowImagePage('showImage.template');
$page->echo();
