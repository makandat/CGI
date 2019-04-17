<?php
namespace OOPHPLib;
include "OOLib0.php";  // ネット環境に依存しないクラス
define("VERSION", "1.1");
define("INIFILE", "AppConf.ini");

// Web ページクラス
class WebPage {
  protected $htm;    // HTML
  public $v;       // 埋め込み変数のディクショナリ
  public $conf;    // コンフィギュレーション

  // コンストラクタ
  public function __construct(string $filePath) {
    if (isset($filePath))
      $this->htm = File::readAllText($filePath);
    $this->v = array();
    // INI ファイルを読んで $conf に格納する。
    $inifile = Directory::getCurrentDirectory() . "/" . INIFILE;
    $this->conf = $this->readIniFile($inifile);
  }

  // HTML 文字列を返す。
  public function toString() : string {
    foreach (array_keys($this->v ) as $key) {
       $this->htm = str_replace('(*'.$key.'*)', $this->v[$key], $this->htm);
    }
    return $this->htm;
  }

  // HTML を出力する。
  public function echo() {
    echo $this->toString();
  }

  // パラメータがあれば true,　なければ false
  public function isPostback() {
    return (count($_POST) + count($_GET) > 0);
  }

  // 生のヘッダーを送る。
  public static function sendHttpHeader(string $header) : void {
     header($header);
  }

  // リダイレクト
  public static function redirect(string $loc) : void {
    header('Location: ' . $loc);
  }

  // 画像ヘッダーを送る。
  public static function sendImageHeader(string $img) {
     $img = strtolower($img);
     if ($img == 'jpg')
       $img = 'jpeg';
     header("Content-Type: image/" . $img);
  }

  // INI ファイルを読む。
  public static function readIniFile(string $inifile) {
    if (File::exists($inifile))
      return parse_ini_file($inifile);
    else
      return false;
  }
}





// タグ作成関連関数

// タグを作る。
function tag($tagname, $value, $style=null) : string {
  $s = "<" . $tagname ;
  if (isset($style)) {
    $s .= " " . $style;
  }
  $s .= ">";
  $s .= $value;
  $s .= "</" . $tagname . ">\n";
  return $s;
}


// Anchor タグ
function anchor($href, $text, $target="") {
  $s = "<a href=\"" . $href . "\">";
  if ($target != "") {
    $s = "<a href=\"" . $href . "\" target=\"" . $target . "\">";
  }
  $s .= $text;
  $s .= "</a>\n";
  return $s;
}



// HTML テーブル行
function HtmlTableRow(array $arr, string $tr = null, string $td = null) : string {
  $s = "<tr";
  if (isset($tr)) {
     $s .= " " . $tr . ">";
  }
  else {
     $s .= ">";
  }

  foreach ($arr as $c) {
    if (isset($td)) {
      $s .= "<td " . $td . ">";
    }
    else {
       $s .= "<td>";
    }
    $s .= $c;
    $s .= "</td>";
  }
  $s .= "</tr>\n";
  return $s;
}


// HTMLテーブルを作る。
function HtmlTable(array $arr, string $tab = null, string $td = null, string $th = null) : string {
  $s = "<table>\n";
  if (isset($tag)) {
    $s = "<table ".$tab.">\n";
  }

  $i = 0;
  foreach ($arr as $row) {
    $s .= "<tr>";
    foreach ($row as $c) {
      if ($i == 0) {
        if (isset($th)) {
          $s .= "<th " . $th . ">" . $c . "</th>";
        }
        else {
          $s .= "<th>" . $c . "</th>";
        }
      }
      else {
        if (isset($td)) {
          $s .= "<td " . $td . ">" . $c . "</td>";
        }
        else {
          $s .= "<td>" . $c . "</td>";
        }
      }
    }
    $s .= "</tr>\n";
    $i += 1;
  }
  $s .= "<table>\n";
  return $s;
}

// HTMLリストを作る。
function HtmlList(array $arr, bool $ol = false, string $style1 = null, string $style2 = null) {
  if ($ol) {
    if (isset($style1)) {
      $s = "<ol " . $style1 . ">\n";
    }
    else {
      $s = "<ol>\n";
    }
  }
  else {
    if (isset($style1)) {
      $s = "<ul " . $style1 . ">\n";
    }
    else {
      $s = "<ul>\n";
    }
  }

  foreach ($arr as $it) {
    if (isset($style2)) {
      $s .= "<li " . $style2 . ">" . $it . "</li>\n";
    }
    else {
      $s .= "<li>" . $it . "</li>\n";
    }
  }

  if ($ol)
    $s .= "</ol>\n";
  else
    $s .= "</ul>\n";
  return $s;
}

// 定義を作る。
function HtmlDefine(array $titles, array $defs, string $style1 = null, string $style2 = null) : string {
  $s = "";
  for ($i = 0; $i < count($titles); $i++) {
    $s .= "<dl>\n";
    if (isset($style1)) {
      $s .= "<dt " . $style1 . ">" . $titles[$i] . "</dt>\n";
    }
    else {
      $s .= "<dt>" . $titles[$i] . "</dt>\n";
    }
    if (isset($style2)) {
      $s .= "<dd " . $style2 . ">" . $defs[$i] . "</dd>\n";
    }
    else {
      $s .= "<dd>" . $defs[$i] . "</dd>\n";
    }
    $s .= "</dl>\n";
  }
  return $s;
}

?>
