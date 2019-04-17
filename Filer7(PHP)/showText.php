<?php
require "OOLib1.php";


//
// メインプログラム
//
$p = new OOPHPLib\WebPage("showText.htmp");
$path = $_GET['path'];
$text = htmlspecialchars(OOPHPLib\File::readAllText($path));
$text = str_replace("\t", "&nbsp;&nbsp;", $text);
$p->v['title'] = "showText.php";
$p->v['text'] = $text;
$p->v['path'] = urlencode(OOPHPLib\File::getDirectory($path));
$p->v['filename'] = OOPHPLib\File::getFileName($path);

$p->echo();

?>
