<?php
include "FileSystem";
# ダウンロード
$fpath = $_GET['path'];
$fname = FileSystem\getFileName($fpath);
header('Content-Type: application/force-download');
header('Content-Length: '.FileSystem\getLength($fpath));
header('Content-disposition: attachment; filename="'.$fname.'"');
readfile($fpath);
?>
