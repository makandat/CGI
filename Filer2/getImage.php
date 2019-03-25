<?php
include "WebPage.php";
$path = $_REQUEST['path'];
WebPage::sendImage($path);
?>
