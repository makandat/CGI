<?php
require "WebPage.php";
require "FileSystem.php";

//
//  メインプログラム
//
$p = new WebPage("templates/showImage.html");
$path = $p->getParam('path');

$index = (int)$p->getparam('index');

// path がファイルかディレクトリか判別
if (FileSystem\isDirectory($path)) {
  $files = FileSystem\getFiles($path, $p->conf['Image']);
  if ($index < 0)
    $index = 0;
  $n = count($files);
  if ($index >= $n)
    $index = $n - 1;
  $filename = $files[$index];
}
else {
  $filename = FileSystem\getFileName($path);
}

// ハッシュ
$hash = md5(FileSystem\getDirectory($path));

// tmp フォルダの内容をクリアする。
//   tmp フォルダは Public Write であること！
$tmpdir = FileSystem\getCurrentDirectory() . "/tmp";
if (FileSystem\isDirectory($tmpdir) == false) {
  echo "エラー ./tmp が存在しません。(./tmp は書き込み可能であること)";
}

array_map('unlink', glob($tmpdir . "/*"));

// 画像ファイルのシンボリックリンク作成
if (FileSystem\exists($path)) {
  FileSystem\createSymlink($path, "tmp/".$hash.$filename);
}
else {
  FileSystem\createSymlink($path . "/" . $filename, "tmp/".$hash.$filename);
}

// パラメータ設定
$p->setPlaceHolder('filename', urlencode($filename));
$p->setPlaceHolder('title', 'showImage.php');
$p->setPlaceHolder('getimage', "tmp/" . $hash.$filename);
$p->setPlaceHolder('previous', (string)($index - 1));
$p->setPlaceHolder('next', (string)($index + 1));
$dir = $path;
if (FileSystem\exists($path))
  $dir = FileSystem\getDirectory($path);
$p->setPlaceHolder('path', = urlencode($dir));

// 表示する。
$p->echo();
?>
