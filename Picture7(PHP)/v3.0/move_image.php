<?php
/* 画像表示とナビゲーション */
include "OOLib1.php";

class MoveImage extends OOPHPLib\WebPage {
    // コンストラクタ
    public function __construct($template) {
        parent::__construct($template);

        // 画像指定があるか？
        if ($_GET['path'] == "") {
            $this->v["message"] = "エラー：パスの指定がありません。";
        }
        else {
            $this->DirName = OOPHPLib\File::getDirectory($_GET['path']);
            $this->v['path'] = $_GET['path'];
            $this->v['dirname'] = $this->DirName;
            // first, previous, next を求める。
            $files = OOPHPLib\Directory::getFiles($this->DirName);
            $filename = OOPHPLib\File::getFileName($_GET['path']);
            $k = array_search($filename, $files);
            if ($k === FALSE) {
                $this->v['message'] = "エラー：パスがこのディレクトリのファイル一覧に見つからない。";
                $this->v['first'] = $files[0];
                $this->v['previous'] = $this->DirName . "/" . $filename;
                $this->v['next'] = $this->DirName . "/" . $filename;
                return;
            }

            $this->v['first'] = $this->DirName . "/" . $files[0];
            $this->v['message'] = "#1" . " / " .strval(count($files));

            if ($k > 0) {
                $this->v['previous'] = $this->DirName . "/" . $files[$k - 1];
                $this->v['message'] = "#" . strval($k - 1) . " / " .strval(count($files));
            }
            else {
                $this->v['previous'] = $this->DirName . "/" . $files[0];
                $this->v['message'] = "先頭の画像です。";
            }
            if ($k < count($files)-1) {
                $this->v['next'] = $this->DirName . "/" . $files[$k + 1];
                $this->v['message'] = "#" . strval($k + 1) . " / " .strval(count($files));
            }
            else {
                $this->v['next'] = $this->DirName . "/" . $files[count($files)-1];
                $this->v['message'] = "最後の画像です。";
            }
        }
    }
}

/* 応答を返す。*/
$p = new MoveImage('move_image.html');
$p->echo();
?>
