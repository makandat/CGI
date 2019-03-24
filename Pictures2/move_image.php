<?php
/* 画像表示とナビゲーション */
include "WebPage.php";
include "FileSystem.php";

class MoveImage extends WebPage {
    // コンストラクタ
    public function __construct($template) {
        parent::__construct($template);

        // 画像指定があるか？
        if ($this->isParam('path') == false) {
            $this->setPlaceHolder("message", "エラー：パスの指定がありません。");
        }
        else {
            $this->DirName = FileSystem\getDirectory($this->getParam('path'));
            $this->setPlaceHolder('path', $this->getParam('path'));
            $this->setPlaceHolder('filename', FileSystem\getFileName($this->getParam('path')));
            $this->setPlaceHolder('dirname', $this->DirName);
            // first, previous, next を求める。
            $files = FileSystem\getFiles($this->DirName);
            $filename = FileSystem\getFileName($this->getParam('path'));
            $k = array_search($filename, $files);
            if ($k === FALSE) {
                $this->setPlaceHolder('message', "エラー：パスがこのディレクトリのファイル一覧に見つからない。");
                $this->setPlaceHolder('first',  $files[0]);
                $this->setPlaceHolder('previous', $this->DirName . "/" . $filename);
                $this->setPlaceHolder('next', $this->DirName . "/" . $filename);
                return;
            }

            $this->setPlaceHolder('first', $this->DirName . "/" . $files[0]);
            $this->setPlaceHolder('message', "#1" . " / " .strval(count($files)));

            if ($k > 0) {
                $this->setPlaceHolder('previous', $this->DirName . "/" . $files[$k - 1]);
                $this->setPlaceHolder('message', "#" . strval($k - 1) . " / " .strval(count($files)));
            }
            else {
                $this->setPlaceHolder('previous', $this->DirName . "/" . $files[0]);
                $this->setPlaceHolder('message', "先頭の画像です。");
            }
            if ($k < count($files)-1) {
                $this->setPlaceHolder('next', $this->DirName . "/" . $files[$k + 1]);
                $this->setPlaceHolder('message', "#" . strval($k + 1) . " / " .strval(count($files)));
            }
            else {
                $this->setPlaceHolder('next', $this->DirName . "/" . $files[count($files)-1]);
                $this->setPlaceHolder('message', "最後の画像です。");
            }
        }
    }
}

/* 応答を返す。*/
$p = new MoveImage('templates/move_image.html');
$p->echo();
?>
