<?php
/* パラメータで指定された画像をバイナリー値として返す。*/
$filename = $_GET["path"];

# ファイル内容を読む。
$handle = fopen($filename, "r");
$contents = fread($handle, filesize($filename));
fclose($handle);

# ヘッダーを送る。
$ext = strtolower(pathinfo($filename, PATHINFO_EXTENSION));
if ($ext == ".jpg" || $ext == ".jpeg")
  $imgtype = "jpeg";
else if ($ext == ".png")
  $imgtype = "png";
else
  $imgtype = "gif";

header("Content-Type: image/" . $imgtype);

# ファイル内容を送る。
echo $contents;

?>
