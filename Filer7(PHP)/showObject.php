<?php
require "OOLib1.php";

//
//  メインプログラム
//
$p = new OOPHPLib\WebPage("showObject.htmp");
$path = $_GET['path'];
$filename = OOPHPLib\File::getFileName($path);

// tmp フォルダの内容をクリアする。
//   ** tmp フォルダは Public Write であること！ **
$tmpdir = OOPHPLib\Directory::getCurrentDirectory() . "/tmp";
array_map('unlink', glob($tmpdir . "/*"));

// Object ファイルのシンボリックリンク作成
OOPHPLib\File::createSymlink($path, 'tmp/'.$filename);

// パラメータ設定
$p->v['filename'] = $filename;
$p->v['title'] = 'showObject.php';
$p->v['getobject'] = "tmp/" . $filename;
$p->v['path'] = urlencode(OOPHPLib\File::getDirectory($path));

// 表示する。
$p->echo();
?>
