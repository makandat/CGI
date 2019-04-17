<?php
/* フォルダ内の画像一括表示 */
include "OOLib1.php";

class ShowImage extends OOPHPLib\WebPage {
    // コンストラクタ
    public function __construct($template) {
        parent::__construct($template);
        $dirname = $_GET['dirname'];
        $buff = "";
        // 画像ファイル一覧を得る。
        $files = OOPHPLib\Directory::getFiles($dirname);
        $i = 0;
        foreach ($files as $fn) {
            $ext = strtolower(OOPHPLib\File::getExtension($fn));
            if ($ext == "jpg" || $ext == "png" || $ext == "gif") {
                $i++;
                $path = $dirname . "/" . $fn;
                $img = "<img src='get_image.php?path=$path' style='padding:6px;' /><br />$i $path<br /><br />\n";
                $buff .= $img;
            }
        }

        $this->v['images'] = $buff;
        $this->v['dirname'] = $dirname;
        $this->v['message'] = '';
    }
}

/* 応答を返す。*/
$p = new ShowImage('showImages.html');
$p->echo();
?>
