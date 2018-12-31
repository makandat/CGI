<?php
namespace OOPHPLib;

const VERSION = "1.0.0";
const CONFIG = "config.ini";


// ファイルクラス
class File {
  // コンストラクタ
  public function __construct(string $filePath) {

  }


  // メソッド

  //  ファイルの存在確認
  public static function exists(string $filePath): bool {
    return is_file($filePath);
  }

  // ファイルサイズを返す。
  public static function getLength(string $filePath) : int {
    return filesize($filePath);
  }

  // ファイルモードを８進数文字列で得る。
  public static function getMode(string $filePath) : string {
    return sprintf("%o", 0777 & stat($filePath)["mode"]);
  }

  // ファイルモードを変更する。
  public static function setMode(string $filePath, string $mode) : void {
    $m = sscanf("%o", $mode);
    chmod($filePath, $m);
  }

  // パスがディレクトリなら true を返す。
  public static function isDirectory(string $filePath) : bool {
    return is_dir($filePath);
  }

  // パスがシンボリックリンクなら true を返す。
  public static function isLink(string $filePath) : bool {
    return is_link($filePath);
  }

  // ファイルが書き込み禁止なら true を返す。
  public static function isReadOnly(string $filePath) : bool {
    return is_writable($filePath);
  }

  // ファイルの最終更新日時を得る。
  public static function getLastModified(string $filePath) : string {
    return strftime("%Y-%m-%d %H:%M:%S", filemtime($filePath));
  }

  // ファイルの所有者を得る。
  public static function getUserName(string $filePath) : string {
    $a = posix_getpwuid(fileowner($filePath));
    return $a["name"];
  }

  // ファイルの所有者グループを得る。
  public static function getGroupName(string $filePath) : string {
    $a = posix_getgrgid(filegroup($filePath));
    return $a["name"];
  }

  // ファイルを読み込んで文字列として返す。
  public static function readAllText(string $filePath) : string {
    return file_get_contents($filePath);
  }

  // ファイルを読み込んで文字列の配列として返す。
  public static function readAllLines(string $filePath) : array {
    $sa = array();
    $fp = fopen($filePath, 'r');
    while (($s = fgets($fp)) != null) {
      $sa.push($s);
    }
    fclose($fp);
    return $sa;
  }

  // 文字列をファイルに書く。
  public static function writeAllText(string $filePath, string $str) : void {
    file_put_contents($filePath, $str);
  }

  // 文字列の配列をファイルに書く。
  public static function writeAllLines(string $filePath, array $sa) : void {
    $fp = fopen($filePath, 'w');
    for ($i = 0; $i < count($sa); $i++) {
      fputs($sa[$i], $fp);
    }
    fclose($fp);
  }

  // 物理パスを得る。
  public static function getPhysicalPath(string $path) : string {
    return realpath($path);
  }

  // 拡張子を返す。("." を含まない)
  public static function getExtension(string $path) : string {
    $arr = pathinfo($path);
    if (isset($arr['extension']))
      return $arr['extension'];
    else
      return "";
  }

  // ファイル名を返す。(拡張子を含む)
  public static function getFileName(string $path) : string {
    $arr = pathinfo($path);
    return $arr['basename'];
  }

  // ファイル名を返す。(拡張子を含まない)
  public static function getFileNameBody(string $path) : string {
    $arr = pathinfo($path);
    return $arr['filename'];
  }

  // ディレクトリを返す。
  public static function getDirectory(string $path) : string {
    $arr = pathinfo($path);
    return $arr['dirname'];
  }

  // ファイルを削除する。
  public static function delete(string $path) : bool {
    return unlink($path);
  }

  // ファイルを移動する。
  public static function move(string $srcpath, $destpath) : bool {
    return rename($srcpath, $destpath);
  }

  // ファイルをコピーする。
  public static function copy(string $srcpath, $destpath) : bool {
    return copy($srcpath, $destpath);
  }

  // シンボリックリンクを作成する。
  public static function createSymlink($target, $name) : bool {
    return symlink($target, $name);
  }
};


// ディレクトリクラス
class Directory {

  // 現在のディレクトリを得る。
  public static function getCurrentDirectory() : string {
    return getcwd();
  }

  // ディレクトリの更新日時を得る。
  public static function getLastModified(string $dirPath) : string {
    return strftime("%Y-%m-%d %H:%M:%S", filemtime($dirPath));
  }

  // 現在のディレクトリを変更する。
  public static function setCurrentDirectory(string $dirPath) : void {
    chdir(dirPath);
  }

  // ディレクトリが存在するかチェックする。
  public static function exists(string $dirPath) : bool {
    return is_dir($dirPath);
  }

  // ディレクトリを作成する。
  public static function createDirectory(string $dirPath) : void {
    mkdir($dirPath, 0755);
  }

  // ディレクトリを削除する。
  public static function removeDirectory(string $dirPath) : void {
    rmdir($dirPath);
  }

  // ファイル一覧を得る。
  public static function getFiles($dirPath, string $filter = "", bool $full=false) : array {
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
        $f1 = File::getFileName($f);
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
  public static function getSubDirectories($dirPath, $full=false) : array {
    $b = array();
    if (!isset($dirPath))
      return $b;
    $a = glob($dirPath . "/*");
    foreach ($a as $f) {
      if (Directory::exists($f) && ! ($f == "." || $f == "..")) {
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
  public function getParentPath(string $dirPath) : string {
    return dirname($dirPath);
  }
}
?>

