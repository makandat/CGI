<?php
require "WebPage.php";
require "FileSystem.php";

//
//  メインプログラム
//
$p = new WebPage("templates/showObject.html");
$path = $p->getParam('path');
$filename = FileSystem\getFileName($path);

// tmp フォルダの内容をクリアする。
//   ** tmp フォルダは Public Write であること！ **
$tmpdir = FileSystem\getCurrentDirectory() . "/tmp";
array_map('unlink', glob($tmpdir . "/*"));

// Object ファイルのシンボリックリンク作成
FileSystem\createSymlink($path, 'tmp/'.$filename);

// パラメータ設定
$p->setPlaceHolder('filename', $filename);
$p->setPlaceHolder('title', 'showObject.php');
$p->setPlaceHolder('getobject', "tmp/" . $filename);
$p->setPlaceHolder('path', urlencode(OOPHPLib\File::getDirectory($path)));

// 表示する。
$p->echo();
?>
