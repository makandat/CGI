<?php
require "WebPage.php";
require "FileSystem.php";

//
// メインプログラム
//
$p = new WebPage("templates/showText.html");
$path = $p->getParam('path');
$text = htmlspecialchars(FileSystem\readAllText($path));
$text = str_replace("\t", "&nbsp;&nbsp;", $text);
$p->setPlaceHolder('title', "showText.php");
$p->setPlaceHolder('text', $text);
$p->setPlaceHolder('path', urlencode(FileSystem\getDirectory($path)));
$p->setPlaceHolder('filename', FileSystem\getFileName($path));

$p->echo();

?>
