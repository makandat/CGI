<?php
require "OOLib1.php";
/*
    PHP7.0では動作せず。

*/
define("MAXLENGTH", 1000000);
$path = $_GET['path'];

// path から拡張子を得る。
$ext = strtolower(OOPHPLib\File::getExtension($path));

// HTTP ヘッダーを送る。
if ($ext == 'jpg')
  $ext = 'jpeg';
/*
OOPHPLib\WebPage::sendImageHeader($ext);

// 拡張子から画像種別を判断

switch ($ext) {
  case 'jpeg':
   $im = imagecreatefromjpeg($path);
   imagejpeg($im);
   break;
  case 'png':
   $im = imagecreatefrompng($path);
   imagepng($im);
   break;
  case 'gif':
   $im = imagecreatefromgif($path);
   imagegif($im);
   break;
  default:
}

imagedestroy($im);
*/

header("Content-Type: image/" . $ext);
header("Content-Length: " . filesize($path));
readfile($path);


?>
