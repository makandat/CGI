<?php
require "WebPage.php";
require "FileSystem.php";
define('TITL', 'PHP7-filer v2.11');  // Windows 対応 2021-02-16
$pss = array();
$maxCount = 10000;
$iniFile = "";
$textExt = array();


// ファイル一覧を作成する。
function listFiles($dir, $filter) {
  global $maxCount;
  $dirs = FileSystem\getSubDirectories($dir);
  if (!isset($filter))
    $filter = '';
  $files = FileSystem\getFiles($dir, $filter);
  $tag = "<ul style=\"list-style:none;\">";
  $tag .= "<a href=\"index.php?path=..\">[..]</a>";
  foreach ($dirs as $f) {
    $dir1 = $dir . "/" . $f;
    $tag .= WebPage::tag("li", "<a href=\"index.php?path=" . $dir1 . "\">[".$f."]</a>");
  }
  $i = 0;
  foreach ($files as $f) {
    $path = $dir . "/" . $f;
    // 属性を得る。
    $size = FileSystem\getLength($path);
    $lastModified = FileSystem\getLastModified($path);
    $mode = FileSystem\getMode($path);
    $uid = FileSystem\getOwnerName($path);
    $gid = FileSystem\getGroupName($path);
    // 属性を表示する。
    $str  = "<div style=\"width:50px;float:left;\">" . $uid . "</div>";
    $str .= "<div style=\"width:50px;float:left;\">" . $gid . "</div>";
    $str .= "<div style=\"width:40px;float:left;\">" . $mode . "</div>";
    $str .= "<div style=\"width:100px;float:left;\">" . $size . "</div>";
    $str .= "<div style=\"width:250px;float:left;\">" . $lastModified . "</div>";
    // ファイルのリンクを得る。
    $fn = GetFileLink($path, $f, $i);
    // ファイルを表示する。
    $str .= "<div style=\"width:320px;float:left;\">" . $fn . "</div>";
    $str .= "<div style=\"clear:both;\"></div>";
    $tag .= WebPage::tag("li", $str);
    $i++;
    // 最大表示数をチェックする。
    if ($i >= $maxCount)
      break;
  }
  $tag .= "</ul>";
  return $tag;
}


// ファイル path の a タグを作成する。
function GetFileLink($path, $filename, $i) {
  global $textExt, $imageExt, $objectExt, $videoExt, $audioExt, $archiveExt;
  $ext = FileSystem\getExtension($path);
  $ext0 = substr($ext, 1);
  $ret = "<a href=";

  // テキスト拡張子のチェック
  $exists = in_array($ext0, $textExt);
  if ($exists === true) {
    $ret .= "showText.php?path=" . urlencode($path) . ">";
    $ret .= $filename . "</a>";
    if ($ext == 'html') {
      $ret .= '&nbsp;<a href="showHtml.php?path=' . urlencode($path) . '" target="_blank">@</a>';
    }
    return $ret;
  }

  // 画像拡張子のチェック
  $exists = in_array($ext0, $imageExt);
  if ($exists === true) {
    $ret .= "showImage.php?";
    $ret .= "index=" . (string)$i;
    $ret .= "&path=" . urlencode($path);
    $ret .=  ">";
    $ret .= $filename;
    $ret .= "</a>";
    return $ret;
  }

  // オブジェクト拡張子のチェック
  $exists = in_array($ext0, $objectExt);
  if ($exists === true) {
    $ret .= 'showObject.php?path=' . urlencode($path) . '>';
    $ret .= $filename . "</a>";
    return $ret;
  }

  // アーカイブファイルの拡張子のチェック
  $exists = in_array($ext0, $archiveExt);
  if ($exists === true) {
    $ret .= 'download.php?path=' . urlencode($path) . '>';
    $ret .= $filename . "</a>";
    return $ret;
  }
  // その他の拡張子や拡張子がない場合
  $ret = $filename;
  if (FileSystem\isLink($path))  // リンクの場合
    $ret = "<span style=\"color:seagreen;\">" . urlencode($filename) . "</span>";

  return $ret;
}


// INIファイルの Path を分解してドロップダウンとして返す。
function listConfFolders(string $paths) {
  global $pss;
  if (substr(PHP_OS, 0, 3) == 'WIN') {
    $pss = explode(",", $paths);
  }
  else {
    $pss = explode(":", $paths);
  }
  $tag = "<option>&nbsp;SELECT Bookmark&nbsp;</option>";
  foreach ($pss as $s) {
    $tag .= "<option>" . $s . "</option>";
  }
  return $tag;
}


// 現在の場所(Current)に表示されるディレクトリにリンクを埋め込む。
function linkPath($dir) {
  $ret = "";
  $pp = "";
  $ss = explode('/', $dir);
  if (WebPage::isWindows()) {
    $ss = explode("\\", $dir);
    $pp = $ss[0];
  }
  for ($i = 1; $i < count($ss); $i++) {
    if (WebPage::isWindows() && $i == 0) {
      $pp .= $ss[$i];
    }
    else {
      $pp .= $ss[$i]."/";
    }
  }
  if (WebPage::isWindows() == FALSE) {
    $pp = str_replace("//", "/", "/".$pp);
  }
  $ret .= "<a href=\"index.php?path=" . $pp . "\">" . $pp . "</a>";

  return $ret;
}





//
// メインプログラム
//
$p = new WebPage("templates/index.html");
$p->setPlaceHolder('debug', '');

// 設定フィルの内容
$iniFile = $p->getConf('Path');
$maxCount = $p->getConf('MaxList');
$textExt = preg_split('/:/', $p->getConf('Text'));
$imageExt = preg_split('/:/', $p->getConf('Image'));
$objectExt = preg_split('/:/', $p->getConf('Object'));
$archiveExt = preg_split('/:/', $p->getConf('Archive'));

// 埋め込み変数の設定
$p->setPlaceHolder('title', TITL);
session_start();
if (!isset($_SESSION['path']))
  $_SESSION['path'] = '/';
$p->setPlaceHolder('dirlist', listConfFolders($iniFile));

// $p->v['debug'] = $_SESSION['path'];
if ($p->isPostback()) {
  // パラメータがあるとき
  $dirPath = $p->getParam('path');  // path
  if ($p->isParam('index')) {  // index
    $previous = $p->getParam('index') - 1;
    $next = $p->getParam('index') + 1;
  }
  else {
    $previous = '0';
    $next = '0';
  }

  if ($p->isParam('filter')) {  //filter
    $filter = htmlspecialchars_decode($p->getParam('filter'));
  }
  else {
    $filter = '';
  }

  // 埋め込み変数を作成する。
  //  パスが .. の場合
  if ($dirPath == '..') {
    $dirPath = FileSystem\getParentPath($_SESSION['path']);
  }
  $p->setPlaceHolder('files', listFiles($dirPath, $filter));
  $p->setPlaceHolder('current', linkPath($dirPath));
  $p->setPlaceHolder('path', $dirPath);
  $p->setPlaceHolder('filter', $filter);
  $p->setPlaceHolder('previous', $previous);
  $p->setPlaceHolder('next', $next);
  $_SESSION['path'] = $dirPath;
}
else {
  // パラメータがないとき
  $filter = htmlspecialchars_decode($p->getParam('filter'));
  $p->setPlaceHolder('files', listFiles($pss[1], $filter));
  $p->setPlaceHolder('current', $pss[0]);
  $p->setPlaceHolder('filter', '');
  $p->setPlaceHolder('previous', "0");
  $p->setPlaceHolder('next', "0");
  $_SESSION['path'] = $pss[0];
}

// HTTP Response を返す。
$p->echo();

?>
