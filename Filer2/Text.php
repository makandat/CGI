<?php
#   Text.php Version 1.00  2019-03-25
namespace Text;

# Text モジュール

# ブール値を文字列に変換する。
function bool2str(bool $b) {
  if ($b) {
    return "TRUE";
  }
  else {
    return "FALSE";
  }
}

# 文字 c が数字かどうか判別
function isdigit(string $c) : bool {
  $u = ord($c);
  if ($u >= 0x30 && $u <= 0x39) {
    return TRUE;
  }
  else {
    return FALSE;
  }
}

# 文字 c が英字かどうか判別
function isalpha(string $c) : bool {
  $u = ord($c);
  if (($u >= ord('A') && $u <= ord('Z')) ||($u >= ord('a') && $u <= ord('z'))) {
    return TRUE;
  }
  else {
    return FALSE;
  }
}

# 文字 c が区切りかどうか判別
function isdelim(string $c) : bool {
  if (isalpha($c)) {
    return FALSE;
  }
  else if (isdigit($c)) {
    return FALSE;
  }
  else if (ord($c) >= 0x20 && ord($c) <= 0x7f) {
    return TRUE;
  }
  else {
    return FALSE;
  }
}

# 文字 c が表示可能かどうか判別
function isprint(string $c) : bool {
  $u = ord($c);
  if ($u < 0x20) {
    return TRUE;
  }
  else {
    return FALSE;
  }
}

# 英小文字を大文字に変換する。
function tolower(string $text) : string {
  return strtolower($text);
}

# 英大文字を小文字に変換する。
function toupper(string $text) : string {
  return strtoupper($text);
}

# ASCII 文字列の長さを返す。
function len(string $text) : int {
  return strlen($text);
}

# 変数の型が文字列かどうか判別する。
function isstr($v) : bool {
  return is_string($v);
}

# 変数の型が整数かどうか判別する。
function isint($v) : bool {
  return is_int($v);
}

# 変数の型が数値かどうか判別する。
function isnum($v) : bool {
  return is_numeric($v);
}

# 文字列１の後に文字列２を追加する。
function append(string $text1, string $text2) : string {
  return $text1.$text2;
}

# ASCII 文字列 text の位置 start から長さ len の部分文字列を返す。
function substring(string $text, int $start, int $len) : string {
  return substr($text, $start, $len);
}

# ASCII 文字列 text の位置 start から位置 end までの部分文字列を返す。
function slice(string $text, int $start, int $end) : string {
  $len = $end - $start + 1;
  return substr($text, $start, $len);
}

# ASCII 文字列 text の長さ len の左側の部分文字列を返す。
function left(string $text, int $len) : string {
  return substr($text, 0, $len);
}

# ASCII 文字列 text の長さ len の右側の部分文字列を返す。
function right(string $text, int $len) : string {
  $start = strlen($text) - $len;
  return substr($text, $start, $len);
}

# 文字 c を n 回繰り返した文字列を返す。
function times(string $c, int $n) : string {
  $buff = '';
  for ($i = 0; $i < $n; $i++) {
    $buff .= $c;
  }
  return $buff;
}

# 引数を書式化した文字列を返す。
function format(string $fmt, ...$vars) : string {
  return sprintf($fmt, ...$vars);
}

# 引数を金額とし３桁おきにカンマを挿入した文字列を返す。
function money(float $val) : string {
  return number_format($val);
}

# 文字列 text に部分文字列 pat が含まれていれば TRUE, そうでなければ FALSE を返す。
function contains(string $text, string $pat) : bool {
  if (strpos($text, $pat) === FALSE) {
     return FALSE;
  }
  else {
     return TRUE;
  }
}

# 文字列 text に部分文字列 pat が含まれていればその位置を返す。含まれていない場合は負数を返す。
function indexOf(string $text, string $pat) : int {
   if (($p = strpos($text, $pat)) === FALSE) {
     return -1;
   }
   else {
      return $p;
   }
}

# 文字列 text の前後に空白があれば取り除く。
//function trim(string $text) : string {
//  return trim($text);
//}

# 文字列 text に部分文字列 pat が含まれていれば、すべて str に置き換える。
function replace(string $text, string $pat, string $str) : string {
  return str_replace($pat, $str, $text);
}

# 文字列 text に文字列 delim が含まれていれば、delim で区切った文字列に分割し、配列として返す。
function split(string $text, string $delim) : array {
  return explode($delim, $text);
}

# 文字列の配列 arr の要素をすべて文字列 delim で結合した文字列を返す。
//function join(array $arr, string $delim) : string {
//
//}

?>
