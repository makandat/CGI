<?php
/* 作者一覧表示 */
include "WebPage.php";
include "MySQL.php";

class ListCreators extends WebPage {
    // コンストラクタ
    public function __construct($template) {
        parent::__construct($template);
        $this->v['creators'] = "";
        // 作者リストを作成する。
        $conn = new MySQL();
        $sql = "SELECT DISTINCT CREATOR FROM Pictures ORDER BY CREATOR";
        if ($this->isParam('filter')) {
          $filter = $this->getparam('filter');
          if ($filter == 'MANGA') {
            $sql = "SELECT DISTINCT CREATOR FROM Pictures WHERE MARK='MANGA' ORDER BY CREATOR";
          }
          else if ($filter == 'HCG') {
            $sql = "SELECT DISTINCT CREATOR FROM Pictures WHERE MARK='HCG' ORDER BY CREATOR";
          }
          else if ($filter == 'Others') {
            $sql = "SELECT DISTINCT CREATOR FROM Pictures WHERE NOT (MARK='HCG' AND MARK='MANGA') ORDER BY CREATOR";
          }
          else {
            $sql = "SELECT DISTINCT CREATOR FROM Pictures ORDER BY CREATOR";
          }
        }
        $data = $conn->query($sql);

        foreach ($data as $row) {
            $this->vars['creators'] .= "<tr>";
            $this->vars['creators'] .= "<td><a href='index.php?creator=".$row["CREATOR"]."'>".$row["CREATOR"]."</a></td>";
            $n = $this->getItemCount($row["CREATOR"], $conn);
            $this->vars['creators'] .= "<td>$n</td>";
            $mark = $this->getMark($row["CREATOR"], $conn);
            $this->vars['creators'] .= "<td>$mark</td>";
            $favs = $this->getFavCount($row["CREATOR"], $conn);
            $this->vars['creators'] .= "<td>$favs</td>";
            $views = $this->getViewCount($row["CREATOR"], $conn);
            $this->vars['creators'] .= "<td>$views</td>";
            $this->vars['creators'] .= "</tr>\n";
        }
    }

    // 作者の作品数を得る。
    private function getItemCount($creator, $conn) {
        $sql = "SELECT count(*) FROM Pictures WHERE creator='$creator'";
        $n = $conn->getValue($sql);  // 作品数
        return $n;
    }

    // 作者の種別を得る。
    private function getMark($creator, $conn) {
        $sql = "SELECT DISTINCT mark FROM Pictures WHERE creator='$creator'";
        $mark = $conn->getValue($sql);  // 種別
        return $mark;
    }

    // 作者のお気に入り合計を得る。
    private function getFavCount($creator, $conn) {
        $sql = "SELECT sum(fav) FROM Pictures WHERE creator='$creator'";
        $fav = $conn->getValue($sql);  // 種別
        return $fav;
    }

    // 作者の閲覧合計を得る。
    private function getViewCount($creator, $conn) {
        $sql = "SELECT sum(count) FROM Pictures WHERE creator='$creator'";
        $count = $conn->getValue($sql);  // 種別
        return $count;
    }
}

/* 応答を返す。*/
$p = new ListCreators("templates/listCreators.html");
$p->echo();
?>
