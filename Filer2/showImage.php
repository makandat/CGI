<?php
require "WebPage.php";
require "FileSystem.php";

//
//  メインプログラム
//
$p = new WebPage("templates/showImage.html");
$path = $p->getParam('path');

$index = (int)$p->getParam('index');

// path がファイルかディレクトリか判別
if (FileSystem\isDirectory($path)) {
  $files = FileSystem\getFiles($path, $p->getConf('Image'));
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

// パラメータ設定
$p->setPlaceHolder('filename', urlencode($filename));
$p->setPlaceHolder('title', 'showImage.php');
if (FileSystem\isDirectory($path)) {
  $imgpath = $path . "/" . $filename;
  $p->setPlaceHolder('getimage', "getImage.php?path=$imgpath");
}
else {
  $p->setPlaceHolder('getimage', "getImage.php?path=$path");
}
$p->setPlaceHolder('previous', $index - 1);
$p->setPlaceHolder('next', $index + 1);
$dir = $path;
if (FileSystem\isFile($path))
  $dir = FileSystem\getDirectory($path);
$p->setPlaceHolder('path', urlencode($dir));

// 表示する。
$p->echo();
?>
