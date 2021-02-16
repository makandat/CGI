<?php
//
// メインプログラム
//
$path = $_GET['path'];
$html = file_get_contents($path);
echo $html;
?>
