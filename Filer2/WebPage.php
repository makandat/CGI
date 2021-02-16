<?php
#  WebPage.php  Version 1.01  2019-03-25
#  WebPage.php  Version 1.10  2021-02-16  Windows 対応
define("APPCONF", "AppConf.ini");
if (substr(PHP_OS, 0, 3) == 'WIN') {
  define("UPLOADDIR", "C:/temp");
  define("PHPLOG", "C:/Apache24/logs/PHPWebPage.log");
}
else {
  define("UPLOADDIR", "/var/www/data");
  define("PHPLOG", "/var/www/data/PHPWebPage.log");
}

# Web ページクラス
class WebPage {
  protected $html;    // HTML
  protected $vars;       // 埋め込み変数のディクショナリ
  protected $conf;    // コンフィギュレーション
  protected $headers;  // ヘッダー

  // コンストラクタ
  public function __construct(string $filePath = '') {
    if (is_file($filePath)) {
      $this->html = WebPage::readAllText($filePath);
    }
    else {
      $this->html = "";
    }
    $this->headers = array('Content-Type: text/html; charset=utf-8');
    $this->vars = array();
    // INI ファイルを読んで $conf に格納する。
    $inifile = getcwd() . "/" . APPCONF;
    if (is_file($inifile)) {
      $this->conf = $this->readIniFile($inifile);
    }
    else {
      $this->conf = array();
    }
  }

  // HTML 文字列を返す。
  public function toString() : string {
    foreach (array_keys($this->vars) as $key) {
       $this->html = str_replace('(*'.$key.'*)', $this->vars[$key], $this->html);
    }
    return $this->html;
  }

  // HTML を出力する。
  public function echo() {
    $this->sendHeaders();
    echo $this->toString();
  }

  // パラメータがあれば true,　なければ false
  public function isPostback() : bool {
    return (count($_REQUEST) > 0 || count($_FILES) > 0);
  }

  // プレイスホルダを得る。
  public function getPlaceHolder(string $key) {
    return $this->vars[$key];
  }

  // プレイスホルダを設定する。
  public function setPlaceHolder(string $key, $value) {
    $this->vars[$key] = $value;
  }

  // パラメータがあるかどうかを返す。
  public function isParam(string $key) : bool {
    return array_key_exists($key, $_REQUEST);
  }

  // パラメータを得る。
  public function getParam(string $key) {
    $value = "";
    if (array_key_exists($key, $_REQUEST)) {
      $value = $_REQUEST[$key];
    }
    return $value;
  }

  // 構成ファイルの情報を得る。
  public function getConf(string $key) {
    return $this->conf[$key];
  }

  // チェックボックスがチェックされているかを返す。
  public function isChecked(string $key) {
    return array_key_exists($key, $_REQUEST);
  }

  // クッキーの有無を返す。
  public function isCookie(string $key) : bool {
    return array_key_exists($key, $_COOKIE);
  }

  // クッキーを得る。
  public function getCookie(string $key) {
    $value = "";
    if (array_key_exists($key, $_COOKIE)) {
      $value = $_COOKIE[$key];
    }
    return $value;
  }

  // クッキーを設定する。
  public function setCookie(string $key, $value) : bool {
    return setcookie($key, $value);
  }

  // HTTP ヘッダーを追加する。
  public function appendHeader($header) {
    array_push($this->headers, $header);
  }

  // HTTP ヘッダーをクリアする。
  public function clearHeader() {
     $this->headers = array();
  }

  // HTTP ヘッダーをすべて送信する。
  public function sendHeaders() {
     foreach ($this->headers as $s) {
        header($s);
     }
  }

  // リダイレクト
  public static function redirect(string $loc) : void {
    header('Location: ' . $loc);
  }

  // INI ファイルを読む。
  public static function readIniFile(string $inifile) {
    if (is_file($inifile)) {
      $ret = parse_ini_file($inifile);
      return $ret;
    }
    else
      return false;
  }

  // ファイルアップロード
  public function fileUpload(string $key) : bool {
    $uploadfile = UPLOADDIR . "/" . $this->getUploadFileName($key);
    return move_uploaded_file($_FILES[$key]['tmp_name'], $uploadfile);
  }

  // アップロードされたファイル名を得る。
  public function getUploadFileName(string $key) : string {
    return basename($_FILES[$key]['name']);
  }

  // アップロード先のディレクトリを得る。
  public function getUploadDirectory() : string {
    return UPLOADDIR;
  }

  // 画像を送る。(jpeg, png, gif)
  public static function sendImage(string $filePath) {
     $img = WebPage::getExtension($filePath);
     $img = strtolower($img);
     if ($img == '.jpg')
       $img = 'jpeg';
     else
       $img = substr($img, 1);
     header("Content-Type: image/" . $img);
     readfile($filePath);
  }

  // テキストを送る。
  public static function sendText(string $text) {
     header("Content-Type: text/plain");
     print $text;
  }

  // テキストファイルを送る。
  public static function sendTextFile(string $filePath) {
     header("Content-Type: text/plain");
     // $text = WebPage::readAllText($filePath);
     // print $text;
     readfile($filePath);
  }

  // JSON 文字列を送る。
  public static function sendJson($json) {
    if (gettype($json) == "array") {
      print json_encode($json);
    }
    else {
      header("Content-Type: application/json");
      print $json;
    }
  }

  // バイナリーファイルを送る。
  public static function sendBinaryFile(string $filePath, string $mime) {
     header("Content-Type: $mime");
     $buff = WebPage::readBinary($filePath);
     print $buff;
  }


  # テキストファイルを読んで内容を文字列として返す。
  public static function readAllText(string $filePath) : string {
    return file_get_contents($filePath);
  }

  # バイナリーファイルを読んで内容を文字列として返す。
  public static function readBinary(string $fileName) : string {
     $fp = fopen($fileName, "rb");
     $buff = fread($fp, filesize($fileName));
     fclose($fp);
     return $buff;
  }

  # ファイルの拡張子を得る。
  public static function getExtension(string $path) : string {
    $arr = pathinfo($path);
    if (isset($arr['extension']))
      return ".".$arr['extension'];
    else
      return "";
  }

  # ログを出力する。logfile を省略すると STDOUT に出力する。
  public static function log_output(string $message, string $logfile = NULL) : void {
    $now = strftime('%Y-%m-%d %T')." ";
    if (isset($logfile)) {
      error_log($now.$message."\n", 3, $logfile);
    }
    else {
      error_log($now.$message."\n", 3, PHPLOG);
    }
  }


  # OS が Windows かどうかを判別
  public static function isWindows() {
    $b = FALSE;
    if (substr(PHP_OS, 0, 3) == 'WIN')
      $b = TRUE;
    return $b;
  }



  // タグ作成関連関数

  // タグを作る。
  public static function tag($tagname, $value, $style=null) : string {
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
  public static function anchor($href, $text, $target="") {
    $s = "<a href=\"" . $href . "\">";
    if ($target != "") {
      $s = "<a href=\"" . $href . "\" target=\"" . $target . "\">";
    }
    $s .= $text;
    $s .= "</a>\n";
    return $s;
  }



  // HTML テーブル行
  public static function table_row(array $arr, string $tr = null, string $td = null) : string {
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
  public static function HtmlTable(array $arr, string $tab = null, string $td = null, string $th = null) : string {
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
    $s .= "</table>\n";
    return $s;
  }

  // HTMLリストを作る。
  public static function HtmlList(array $arr, bool $ol = false, string $style1 = null, string $style2 = null) {
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
  public static function HtmlDefine(array $titles, array $defs, string $style1 = null, string $style2 = null) : string {
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
}
?>
