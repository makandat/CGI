<?php
/* 作者一覧表示 */
include "OOLib1.php";
include "MySQL.php";

class ListCreators extends OOPHPLib\WebPage {
    // コンストラクタ
    public function __construct($template) {
        parent::__construct($template);
        $this->v['creators'] = "";
        // 作者リストを作成する。
        $conn = new OOPHPLib\MySQL('AppConf.ini');
        $sql = "SELECT DISTINCT CREATOR FROM Pictures ORDER BY CREATOR";
        $data = $conn->query($sql);
        foreach ($data as $row) {
            $this->v['creators'] .= "<li>";
            $this->v['creators'] .= "<a href='index.php?creator=".$row["CREATOR"]."'>".$row["CREATOR"]."</a>";
            $this->v['creators'] .= "</li>";
        }
    }
}

/* 応答を返す。*/
$p = new ListCreators("listCreators.html");
$p->echo();
?>
