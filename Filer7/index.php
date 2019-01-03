<?php
require "OOLib1.php";
define('TITL', 'PHP7-filer v1.20');
$pss = array();
$maxCount = 10000;
$iniFile = "";
$textExt = array();


// ファイル一覧を作成する。
function listFiles($dir, $filter) {
  global $maxCount;
  $dirs = OOPHPLib\Directory::getSubDirectories($dir);
  if (!isset($filter))
    $filter = '';
  $files = OOPHPLib\Directory::getFiles($dir, $filter);
  $tag = "<ul style=\"list-style:none;\">";
  $tag .= "<a href=\"index.php?path=..\">[..]</a>";
  foreach ($dirs as $f) {
    $dir1 = $dir . "/" . $f;
    $tag .= OOPHPLib\tag("li", "<a href=\"index.php?path=" . $dir1 . "\">[".$f."]</a>");
  }
  $i = 0;
  foreach ($files as $f) {
    $path = $dir . "/" . $f;
    // 属性を得る。
    $size = OOPHPLib\File::getLength($path);
    $lastModified = OOPHPLib\File::getLastModified($path);
    $mode = OOPHPLib\File::getMode($path);
    $uid = OOPHPLib\File::getUserName($path);
    $gid = OOPHPLib\File::getGroupName($path);
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
    $tag .= OOPHPLib\tag("li", $str);
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
  global $textExt, $imageExt, $objectExt, $videoExt, $audioExt;
  $ext = OOPHPLib\File::getExtension($path);
  $ret = "<a href=";

  // テキスト拡張子のチェック
  $exists = in_array($ext, $textExt);
  if ($exists === true) {
    $ret .= "showText.php?path=" . urlencode($path) . ">";
    $ret .= $filename . "</a>";
    if ($ext == 'html') {
      $ret .= '&nbsp;<a href="showHtml.php?path=' . urlencode($path) . '" target="_blank">@</a>';
    }
    return $ret;
  }

  // 画像拡張子のチェック
  $exists = in_array($ext, $imageExt);
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
  $exists = in_array($ext, $objectExt);
  if ($exists === true) {
    $ret .= 'showObject.php?path=' . urlencode($path) . '>';
    $ret .= $filename . "</a>";
    return $ret;
  }

  // その他の拡張子や拡張子がない場合
  $ret = $filename;
  if (OOPHPLib\File::isLink($path))  // リンクの場合
    $ret = "<span style=\"color:seagreen;\">" . urlencode($filename) . "</span>";

  return $ret;
}


// INIファイルの Path を分解してドロップダウンとして返す。
function listConfFolders(string $paths) {
  global $pss;
  $pss = preg_split("/:/", $paths);
  $tag = "";
  foreach ($pss as $s) {
    $tag .= "<option>" . $s . "</option>";
  }
  return $tag;
}


// 現在の場所(Current)に表示されるディレクトリにリンクを埋め込む。
function linkPath($dir) {
  $ret = "";
  $pp = "";
  $ss = preg_split('/\//', $dir);

  for ($i = 1; $i < count($ss); $i++) {
    $pp .= "/" . $ss[$i];
    $ret .= "/<a href=\"index.php?path=" . $pp . "\">" . $ss[$i] . "</a>";
  }

  return $ret;
}





//
// メインプログラム
//
$p = new OOPHPLib\WebPage("index.htmp");
$p->v['debug'] = '';

// 設定フィルの内容
$iniFile = $p->conf['Path'];
$maxCount = $p->conf['MaxList'];
$textExt = preg_split('/:/', $p->conf['Text']);
$imageExt = preg_split('/:/', $p->conf['Image']);
$objectExt = preg_split('/:/', $p->conf['Object']);

// 埋め込み変数の設定
$p->v['title'] = TITL;
session_start();
if (!isset($_SESSION['path']))
  $_SESSION['path'] = '/';
$p->v['dirlist'] = listConfFolders($iniFile);

// $p->v['debug'] = $_SESSION['path'];
if ($p->isPostback()) {
  // パラメータがあるとき
  $dirPath = $_GET['path'];  // path
  if (isset($_GET['index'])) {  // index
    $previous = $_GET['index'] - 1;
    $next = $_GET['index'] + 1;
  }
  else {
    $previous = '0';
    $next = '0';
  }

  if (isset($_GET['filter'])) {  //filter
    $filter = htmlspecialchars_decode($_GET['filter']);
  }
  else {
    $filter = '';
  }

  // 埋め込み変数を作成する。
  //  パスが .. の場合
  if ($dirPath == '..')
    $dirPath = OOPHPLib\Directory::getParentPath($_SESSION['path']);
  $p->v['files'] = listFiles($dirPath, $filter);
  $p->v['current'] = linkPath($dirPath);
  $p->v['path'] = $dirPath;
  $p->v['filter'] = $filter;
  $p->v['previous'] = $previous;
  $p->v['next'] = $next;
  $_SESSION['path'] = $dirPath;
}
else {
  // パラメータがないとき
  $filter = htmlspecialchars_decode($_GET['filter']);
  $p->v['files'] = listFiles($pss[1], $filter);
  $p->v['current'] = $pss[0];
  $p->v['filter'] = '';
  $p->v['previous'] = "0";
  $p->v['next'] = "0";
  $_SESSION['path'] = $pss[0];
}

// HTTP Response を返す。
$p->echo();

?>
