<?php
/* フォルダ内の画像一括表示 */
include "WebPage.php";
include "FileSystem.php";

class ShowImage extends WebPage {
    // コンストラクタ
    public function __construct($template) {
        parent::__construct($template);
        $dirname = $this->getParam('dirname');
        $dirname0 = $this->getDeepest($dirname);
        $this->setPlaceHolder('dirname0', $dirname0);
        $buff = "";
        // 画像ファイル一覧を得る。
        $files = FileSystem\getFiles($dirname);
        $i = 0;
        foreach ($files as $fn) {
            $ext = strtolower(FileSystem\getExtension($fn));
            if ($ext == ".jpg" || $ext == ".png" || $ext == ".gif") {
                $i++;
                $path = $dirname . "/" . $fn;
                $img = "<img src='get_image.php?path=$path' style='padding:6px;' /><br />$i $path<br /><br />\n";
                $buff .= $img;
            }
        }

        $this->setPlaceHolder('images', $buff);
        $this->setPlaceHolder('dirname', $dirname);
        $this->setPlaceHolder('message', '');
    }

    // 一番深いディレクトリを得る。
    private function getDeepest($dir) {
      $p = preg_split('/\//', $dir);
      $n = count($p) - 1;
      if ($n < 0) {
        return "";
      }
      return $p[$n];
    }
}

/* 応答を返す。*/
$p = new ShowImage('templates/showImages.html');
$p->echo();
?>
