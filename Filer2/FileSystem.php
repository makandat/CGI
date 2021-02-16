<?php
#  FileSystem.php Version 1.02  2019-03-25
#  FileSystem.php Version 1.10  2021-02-16  Windows 対応
namespace FileSystem;

//  ファイル,ディレクトリの存在確認
function exists(string $filePath): bool {
  return file_exists($filePath);
}

// ファイルサイズを返す。
function getLength(string $filePath) : int {
  return filesize($filePath);
}

// ファイルモードを８進数文字列で得る。
function getMode(string $filePath) : string {
  return sprintf("%o", 0777 & stat($filePath)["mode"]);
}

// ファイルモードを変更する。
function setMode(string $filePath, int $mode) : void {
  chmod($filePath, $mode);
}

// パスがディレクトリなら true を返す。
function isDirectory(string $filePath) : bool {
  return is_dir($filePath);
}

// パスがファイルなら true を返す。
function isFile(string $filePath) : bool {
  return is_file($filePath);
}

// パスがシンボリックリンクなら true を返す。
function isLink(string $filePath) : bool {
  return is_link($filePath);
}

// ファイルが書き込み禁止なら true を返す。
function isReadOnly(string $filePath) : bool {
  return is_writable($filePath);
}

// ファイルの最終更新日時を得る。
function getLastModified(string $filePath) : string {
  return strftime("%Y-%m-%d %H:%M:%S", filemtime($filePath));
}

// ファイルの所有者を得る。
function getOwnerName(string $filePath) : string {
  $a = array("name"=>"undef");
  if (substr(PHP_OS, 0, 3) != 'WIN') {
    $a = posix_getpwuid(fileowner($filePath));
  }
  return $a["name"];
}

// ファイルの所有者グループを得る。
function getGroupName(string $filePath) : string {
  $a = array("name"=>"undef");
  if (substr(PHP_OS, 0, 3) != 'WIN') {
    $a = posix_getgrgid(filegroup($filePath));
  }
  return $a["name"];
}

// ファイルを読み込んで文字列として返す。
function readAllText(string $filePath) : string {
  return file_get_contents($filePath);
}

// ファイルを読み込んで文字列の配列として返す。
function readAllLines(string $filePath) : array {
  $sa = array();
  $fp = fopen($filePath, 'r');
  while (($s = fgets($fp)) != null) {
    $s = chop($s);
    array_push($sa, $s);
  }
  fclose($fp);
  return $sa;
}

// 文字列をファイルに書く。
function writeAllText(string $filePath, string $str) {
  file_put_contents($filePath, $str);
}


// バイナリーデータをファイルから読む。
function readBinary(string $filePath) : string {
  $fp = fopen($filePath, "rb");
  $content = fread($fp, filesize($filePath));
  fclose($fp);
  return $content;
}

// バイナリーデータをファイルに書く。
function writeBinary(string $filePath, string $data) : void {
  $fp = fopen($filePath, "wb");
  fwrite($fp, $data);
  fclose($fp);
}



// 文字列をファイルに追加する。
function appendText(string $filePath, string $str) : void  {
  $fp = fopen($filePath, "a");
  fputs($fp, $str);
  fclose($fp);
}

// 文字列の配列をファイルに書く。
function writeAllLines(string $filePath, array $sa) : void {
  $fp = fopen($filePath, 'w');
  for ($i = 0; $i < count($sa); $i++) {
    fputs($fp, $sa[$i]);
  }
  fclose($fp);
}

// 物理パスを得る。
function getPhysicalPath(string $path) : string {
  return realpath($path);
}

// 拡張子を返す。("." を含む)
function getExtension(string $path) : string {
  $arr = pathinfo($path);
  if (isset($arr['extension']))
    return ".".$arr['extension'];
  else
    return "";
}

// ファイル名を返す。(拡張子を含む)
function getFileName(string $path) : string {
  $arr = pathinfo($path);
  return $arr['basename'];
}

// ファイル名を返す。(拡張子を含まない)
function getFileNameBody(string $path) : string {
  $arr = pathinfo($path);
  return $arr['filename'];
}

// ディレクトリを返す。
function getDirectory(string $path) : string {
  $arr = pathinfo($path);
  return $arr['dirname'];
}

// ファイルを削除する。
function fdelete(string $path) : bool {
  return unlink($path);
}

// ファイルを移動する。
function fmove(string $srcpath, $destpath) : bool {
  return rename($srcpath, $destpath);
}

// ファイルをコピーする。
function fcopy(string $srcpath, $destpath) : bool {
  return copy($srcpath, $destpath);
}

// シンボリックリンクを作成する。
function createSymlink($target, $name) : bool {
  return symlink($target, $name);
}

// 現在のディレクトリを得る。
function getCurrentDirectory() : string {
  return getcwd();
}


// 現在のディレクトリを変更する。
function setCurrentDirectory(string $dirPath) : void {
  chdir($dirPath);
}

// ディレクトリを作成する。
function createDirectory(string $dirPath) : void {
  mkdir($dirPath, 0755);
}

// ディレクトリを削除する。
function removeDirectory(string $dirPath) : void {
  rmdir($dirPath);
}

// ファイル一覧を得る。
function getFiles($dirPath, string $filter = "", bool $full=false) : array {
  $exts = array();
  $b = array();
  if (!isset($dirPath))
     return $b;

  // 拡張子フィルタか判別
  if (strpos($filter, ':') === false) {
    if ($filter <> '') {
      // 通常のフィルタ
      $a = glob($dirPath . "/" . $filter);
    }
    else {
      // フィルタがない場合は dirPath に "/*" を追加
      $a = glob($dirPath . "/*");
    }
  }
  else {
    // 拡張子フィルタ
    $exts = preg_split('/:/', $filter);
    $a = glob($dirPath . "/*");
  }

  $extmatch = false;
  $n = count($exts);
  foreach ($a as $f) {
    if (!is_file($f))  // ファイル以外は処理をスキップ
      continue;
    if ($n > 0) {
       // 拡張子フィルタの場合
       for ($i = 0; $i < $n; $i++) {
         if (preg_match('/\.'.$exts[$i].'$/', $f) === 1) {
           $extmatch = true;
           break;
         }
       }
    }
    if ($full == false)
      $f1 = getFileName($f);
    else
      $f1 = $f;
    if ($n == 0 || ($n > 0 && $extmatch)) {
      array_push($b, htmlspecialchars($f1));
    }
  }
  natcasesort($b);  // ソート
  return $b;
}

// サブディレクトリ一覧を得る。
function getSubDirectories($dirPath, $full=false) : array {
  $b = array();
  if (!isset($dirPath))
    return $b;
  $a = glob($dirPath . "/*");
  foreach ($a as $f) {
    if (is_dir($f) && ! ($f == "." || $f == "..")) {
      if ($full == false) {
        $ss = preg_split('/\//', $f);
        $f1 = $ss[count($ss) - 1];
        array_push($b, htmlspecialchars($f1));
      }
      else
        array_push($b, htmlspecialchars($f));
    }
  }
  natcasesort($b);
  return $b;
}

// 親のディレクトリを返す。
function getParentPath(string $dirPath) : string {
  return dirname($dirPath);
}

?>

