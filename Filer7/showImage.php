<?php
require "OOLib1.php";

//
//  メインプログラム
//
$p = new OOPHPLib\WebPage("showImage.htmp");
$path = $_GET['path'];

$index = (int)$_GET['index'];

// path がファイルかディレクトリか判別
if (OOPHPLib\File::isDirectory($path)) {
  $files = OOPHPLib\Directory::getFiles($path, $p->conf['Image']);
  if ($index < 0)
    $index = 0;
  $n = count($files);
  if ($index >= $n)
    $index = $n - 1;
  $filename = $files[$index];
}
else {
  $filename = OOPHPLib\File::getFileName($path);
}

// ハッシュ
$hash = md5(OOPHPLib\File::getDirectory($path));

// tmp フォルダの内容をクリアする。
//   tmp フォルダは Public Write であること！
$tmpdir = OOPHPLib\Directory::getCurrentDirectory() . "/tmp";
if (OOPHPLib\File::isDirectory($tmpdir) == false) {
  echo "エラー ./tmp が存在しません。(./tmp は書き込み可能であること)";
}

array_map('unlink', glob($tmpdir . "/*"));

// 画像ファイルのシンボリックリンク作成
if (OOPHPLib\File::exists($path)) {
  OOPHPLib\File::createSymlink($path, "tmp/".$hash.$filename);
}
else {
  OOPHPLib\File::createSymlink($path . "/" . $filename, "tmp/".$hash.$filename);
}

// パラメータ設定
$p->v['filename'] = urlencode($filename);
$p->v['title'] = 'showImage.php';
$p->v['getimage'] = "tmp/" . $hash.$filename;
$p->v['previous'] = (string)($index - 1);
$p->v['next'] = (string)($index + 1);
$dir = $path;
if (OOPHPLib\File::exists($path))
  $dir = OOPHPLib\File::getDirectory($path);
$p->v['path'] = urlencode($dir);

// 表示する。
$p->echo();
?>
