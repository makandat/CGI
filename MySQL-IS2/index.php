<?php
include "OOLib1.php";
include "MySQLInfo.php";

//
//  ページクラス
//  =============
class MyPage extends OOPHPLib\WebPage {
  private $mysqlInfo;

  // コンストラクタ
  public function __construct(string $filePath = null) {
    parent::__construct($filePath);
    $this->mysqlInfo = new OOPHPLib\MySQLInfo("AppConf.ini");
  }

  // デストラクタ
  public function __destruct() {
    $this->mysqlInfo->close();
  }

  // コンテンツを作成する。
  public function getContent() : string {
    $cc = 'databases';
    if (isset($_GET['view'])) {
      $cc = $_GET['view'];
    }

    $content = '';

    switch ($cc) {
      case 'users':
        // ユーザ一覧
        $content = $this->listUsers();
        break;

      case 'tables':
        // テーブル一覧
        if (isset($_GET['database'])) {
          $content = $this->listTables($_GET['database']);
        }
        else {
          $content = $this->selectDatabase('tables');
        }
        break;

      case 'views':
        // ビュー一覧
        if (isset($_GET['database'])) {
          $content = $this->listViews($_GET['database']);
        }
        else {
          $content = $this->selectDatabase('views');
        }
        break;

      case 'indexes':
        // インデックス一覧
        if (isset($_GET['database'])) {
          $content = $this->listIndexes($_GET['database']);
        }
        else {
          $content = $this->selectDatabase('indexes');
        }
        break;

      case 'routines':
        // ルーチン一覧
        if (isset($_GET['database'])) {
          $content = $this->listRoutines($_GET['database']);
        }
        else {
          $content = $this->selectDatabase('routines');
        }
        break;

      case 'triggers':
        // トリガ一覧
        if (isset($_GET['database'])) {
          $content = $this->listTriggers($_GET['database']);
        }
        else {
          $content = $this->selectDatabase('triggers');
        }
        break;

      case 'charsets':
        // 文字コード一覧
        $content = $this->listCharsets();
        break;

      case 'collations':
        // 並び替え順序一覧
        $content = $this->listCollations();
        break;

      case 'columns':
        // テーブルのカラム定義
        $content = $this->listColumns($_GET['database'], $_GET['table']);
        break;

      case 'viewdef':
        // ビュー定義
        $content = $this->getViewDef($_GET['database'], $_GET['table']);
        break;

      case 'routinedef':
        // ルーチン定義
        $content = $this->getRoutineDef($_GET['database'], $_GET['routine']);
        break;

      case 'triggerdef':
        // トリガ定義
        $content = $this->getTriggerDef($_GET['database'], $_GET['trigger']);
        break;

      default:
        // データベース一覧
        $content = $this->listDatabases();
        break;
    }

    return $content;
  }


  // データベース選択表示
  private function selectDatabase($view) {
    $dataTable = $this->mysqlInfo->getDatabases();
    $content = '<div style="margin-left:30px;margin-top:20px;"><h2 style="color:magenta;text-decoration:underline;">Select a database for ' . $view . '</h2>';
    $content .= '<ol>';
    foreach ($dataTable as $row) {
      $content .= '<li style="font-size:large;">';
      $content .= OOPHPLib\anchor('index.php?view=' . $view . '&amp;database=' . $row['SCHEMA_NAME'], $row['SCHEMA_NAME']);
      $content .= '</li>';
    }
    $content .= '</ol></div>';
    return $content;
  }

  // データベース一覧
  private function listDatabases() {
     $dataTable = $this->mysqlInfo->getDatabases();
     $buff = '<h2 style="margin-left:10%;">Databases</h2>';
     $buff .= '<table style="margin-left:10px;margin-bottom:30px;width:90%;">';
     $buff .= '<tr><th>SCHEMA_NAME</th><th>DEFAULT_CHARACTER_SET_NAME</th><th>DEFAULT_COLLATION_NAME</th></tr>';

     foreach ($dataTable as $row) {
       $buff .= '<tr>';
       $anchor = OOPHPLib\anchor("index.php?view=tables&amp;database=" . $row['SCHEMA_NAME'], $row['SCHEMA_NAME']);
       $buff .= "<td>".$anchor."</td>";
       $buff .= "<td>".$row['DEFAULT_CHARACTER_SET_NAME']."</td>";
       $buff .= "<td>".$row['DEFAULT_COLLATION_NAME']."</td>";
       $buff .= '</tr>';
     }

     $buff .= '</table>';
     return $buff;
  }


  // ユーザ一覧
  private function listUsers() {
    $dataTable = $this->mysqlInfo->getUsers();

     $buff = '<h2 style="margin-left:10%;">Users</h2>';
     $buff .= '<table style="margin-left:10px;margin-bottom:30px;width:90%;">';
     $buff .= '<tr><th>USER</th></tr>';

     foreach ($dataTable as $row) {
       $buff .= '<tr><td>';
       $buff .= $row['GRANTEE'];
       $buff .= '</td></tr>';
     }

     $buff .= '</table>';
     return $buff;
  }


  // テーブル一覧
  private function listTables($database) {
     $dataTable = $this->mysqlInfo->getTables($database);
     $buff = '<h2 style="margin-left:10%;">Tables of "'. $database.'"</h2>';
     $buff .= '<table style="margin-left:10px;margin-bottom:30px;width:90%;">';
     $buff .= '<tr><th>TABLE_NAME</th><th>DATA_LENGTH</th><th>AUTO_INCREMENT</th><th>CREATE_TIME</th><th>UPDATE_TIME</th></tr>';
     foreach ($dataTable as $row) {
       $buff .= '<tr>';
       $buff .= '<td>'.OOPHPLib\anchor('index.php?view=columns&amp;database=' . $database . '&amp;table=' . $row['TABLE_NAME'], $row['TABLE_NAME']).'</td>';
       $buff .= '<td>'.$row['DATA_LENGTH'].'</td>';
       $buff .= '<td>'.$row['AUTO_INCREMENT'].'</td>';
       $buff .= '<td>'.$row['CREATE_TIME'].'</td>';
       $buff .= '<td>'.$row['UPDATE_TIME'].'</td>';
       $buff .= '</td>';
     }

     $buff .= '</table>';
     return $buff;
  }


  // ビュー一覧
  private function listViews($database) {
     $dataTable = $this->mysqlInfo->getViews($database);
     $buff = '<h2 style="margin-left:10%;">Views of "'. $database.'"</h2>';
     $buff .= '<table style="margin-left:10px;margin-bottom:30px;width:90%;">';
     $buff .= '<tr><th>TABLE_NAME</th></tr>';
     foreach ($dataTable as $row) {
       $buff .= '<tr>';
       $buff .= '<td>' . OOPHPLib\anchor('index.php?view=viewdef&amp;database=' . $database . '&amp;table=' . $row['TABLE_NAME'], $row['TABLE_NAME']) .'</td>';
       $buff .= '</td>';
     }

     $buff .= '</table>';
     return $buff;
  }

  // ビューの定義を得る。
  private function getViewDef($database, $view) {
    $viewbody = $this->mysqlInfo->getViewDef($database, $view);
    $buff = '<h2 style="margin-left:10%;">View Definition of "'. $database . '.' . $view. '"</h2>';
    $buff .= '<pre style="padding:4px;font-size:small;">';
    $buff .= htmlspecialchars($this->wrapSpace($viewbody));
    $buff .= '</pre>';
    return $buff;
  }

  // ルーチン一覧
  private function listRoutines($database) {
     $dataTable = $this->mysqlInfo->getRoutines($database);
     $buff = '<h2 style="margin-left:10%;">Routines of "'. $database.'"</h2>';
     $buff .= '<table style="margin-left:10px;margin-bottom:30px;width:90%;">';
     $buff .= '<tr><th>ROUTINE_NAME</th><th>ROUTINE_TYPE</th><th>DATA_TYPE</th></tr>';
     foreach ($dataTable as $row) {
       $buff .= '<tr>';
       $buff .= '<td>' . OOPHPLib\anchor('index.php?view=routinedef&amp;database=' . $database . '&amp;routine=' . $row['ROUTINE_NAME'], $row['ROUTINE_NAME']) .'</td>';
       $buff .= '<td>'.$row['PARAM_LIST'].'</td>';
       $buff .= '<td>'.$row['RETURNS'].'</td>';
       $buff .= '<td>'.substr($row['BODY'], 0, 100) .' ... </td>';
       $buff .= '</td>';
     }

     $buff .= '</table>';
     return $buff;
  }


  // トリガ一覧
  private function listTriggers($database) {
     $dataTable = $this->mysqlInfo->getTriggers($database);
     $buff = '<h2 style="margin-left:10%;">Triggers of "'. $database.'"</h2>';
     $buff .= '<table style="margin-left:10px;margin-bottom:30px;width:90%;">';
     $buff .= '<tr><th>TRIGGER_NAME</th><th>EVENT_MANIPULATION</th><th>ACTION_TIMING</th></tr>';
     foreach ($dataTable as $row) {
       $buff .= '<tr>';
       $buff .= '<td>' . OOPHPLib\anchor('index.php?view=triggerdef&amp;database=' . $database . '&amp;trigger=' . $row['TRIGGER_NAME'], $row['TRIGGER_NAME']) .'</td>';
       $buff .= '<td>'.$row['EVENT_MANIPULATION'].'</td>';
       $buff .= '<td>'.$row['ACTION_TIMING'].'</td>';
       $buff .= '</td>';
     }

     $buff .= '</table>';
     return $buff;
  }


  // 文字コード一覧
  private function listCharsets() {
     $dataTable = $this->mysqlInfo->getCharacterSets();
     $buff = '<h2 style="margin-left:10%;">CharacterSets</h2>';
     $buff .= '<table style="margin-left:10px;margin-bottom:30px;width:90%;">';
     $buff .= '<tr><th>CHARACTER_SET_NAME</th><th>DEFAULT_COLLATE_NAME</th><th>DESCRIPTION</th><th>MAXLEN</th></tr>';
     foreach ($dataTable as $row) {
       $buff .= '<tr>';
       $buff .= '<td>' . $row['CHARACTER_SET_NAME'] .'</td>';
       $buff .= '<td>' . $row['DEFAULT_COLLATE_NAME'] . '</td>';
       $buff .= '<td>' . $row['DESCRIPTION'] . '</td>';
       $buff .= '<td>' . $row['MAXLEN'] . '</td>';
       $buff .= '</td>';
     }

     $buff .= '</table>';
     return $buff;
  }


  // 並び替え順序一覧
  private function listCollations() {
     $dataTable = $this->mysqlInfo->getCollations();
     $buff = '<h2 style="margin-left:10%;">Collations</h2>';
     $buff .= '<table style="margin-left:10px;margin-bottom:30px;width:90%;">';
     $buff .= '<tr><th>COLLATION_NAME</th><th>CHARACTER_SET_NAME</th><th>ID</th><th>IS_DEFAULT</th></tr>';
     foreach ($dataTable as $row) {
       $buff .= '<tr>';
       $buff .= '<td>' . $row['COLLATION_NAME'] .'</td>';
       $buff .= '<td>' . $row['CHARACTER_SET_NAME'] . '</td>';
       $buff .= '<td>' . $row['ID'] . '</td>';
       $buff .= '<td>' . $row['IS_DEFAULT'] . '</td>';
       $buff .= '</td>';
     }

     $buff .= '</table>';
     return $buff;
  }

  // ルーチンの定義情報を得る。
  private function getRoutineDef($database, $routine) {
    $dataTable = $this->mysqlInfo->getRoutineDef($database, $routine);
    if (count($dataTable) == 0) {
      $buff = '<h2 style="margin-left:10%;">Error: No routine definitions found of ' . $database . '.' . $routine . '</h2>';
    }
    else {
      $row = $dataTable[0];
      $buff = '<h2 style="margin-left:10%;">Routine Definition of ' . $database . '.' .$routine . '</h2>';
      $buff .= '<table style="margin-left:10px;margin-bottom:30px;width:90%;">';
      $buff .= '<tr><td class="tdleft" style="border-top:solid thin silver;">NAME</td><td style="border-top:solid thin silver;">' . $routine . '</td></tr>';
      $buff .= '<tr><td class="tdleft">PARAM_LIST</td><td><pre>' . $row['param_list'] . '</pre></td></tr>';
      $buff .= '<tr><td class="tdleft">RETURNS</td><td><pre>' . $row['returns'] . '</pre></td></tr>';
      $buff .= '<tr><td class="tdleft">BODY</td><td><pre>' . htmlspecialchars($this->insertLf($row['body'])) . '</pre></td></tr>';
      $buff .= '</table>';
    }
    return $buff;
  }


  // トリガの定義情報を得る。
  private function getTriggerDef($database, $trigger) {
    $action = $this->mysqlInfo->getTriggerDef($database, $trigger);
    if (!isset($action)) {
      $buff = '<h2 style="margin-left:10%;">Trigger statement is NULL. (' . $database . '.' . $trigger . ')</h2>';
    }
    else {
      $buff = '<h2 style="margin-left:10%;">Trigger Definition of ' . $database . '.' .$trigger . '</h2>';
      $buff .= '<pre style="padding:4px;font-size:small;">' . htmlspecialchars($this->insertLf($action)) . '</pre>';
    }
    return $buff;
  }

  // テーブルのカラム定義を得る。
  private function listColumns($database, $table) {
    $dataTable = $this->mysqlInfo->getColumns($database, $table);
    $buff = '<h2 style="margin-left:10%;">Columns of ' . $database . '.' .$table . '</h2>';
    $buff .= '<table style="margin-left:10px;margin-bottom:30px;width:90%;">';
    $buff .= '<tr><th style="font-size:small;">ORDINAL_POSITION</th><th style="font-size:small;">COLUMN_NAME</th><th style="font-size:small;">COLUMN_DEFAULT</th><th style="font-size:small;">IS_NULLABLE</th><th style="font-size:small;">COLUMN_TYPE</th><th style="font-size:small;">COLUMN_KEY</th><th style="font-size:small;">EXTRA</th></tr>';
    foreach ($dataTable as $row) {
       $buff .= "<tr>";
       $buff .= '<td>' . $row['ORDINAL_POSITION'] . '</td>';
       $buff .= '<td>' . $row['COLUMN_NAME'] . '</td>';
       $buff .= '<td>' . $row['COLUMN_DEFAULT'] . '</td>';
       $buff .= '<td>' . $row['IS_NULLABLE'] . '</td>';
       $buff .= '<td>' . $row['COLUMN_TYPE'] . '</td>';
       $buff .= '<td>' . $row['COLUMN_KEY'] . '</td>';
       $buff .= '<td>' . $row['EXTRA'] . '</td>';
       $buff .= "</tr>";
    }
    $buff .= "</table>";
    return $buff;
  }


  // インデックス一覧を得る。
  private function listIndexes($database) {
    $dataTable = $this->mysqlInfo->getIndexes($database);
    $buff = '<h2 style="margin-left:10%;">Indexes of ' . $database . '</h2>';
    $buff .= '<table style="margin-left:10px;margin-bottom:30px;width:90%;">';
    $buff .= '<tr><th style="font-size:small;">INDEX_NAME</th><th style="font-size:small;">TABLE_NAME</th><th style="font-size:small;">COLUMN_NAME</th><th style="font-size:small;">SEQ_IN_INDEX</th></tr>';
    foreach ($dataTable as $row) {
       $buff .= "<tr>";
       $buff .= '<td>' . $row['INDEX_NAME'] . '</td>';
       $buff .= '<td>' . $row['TABLE_NAME'] . '</td>';
       $buff .= '<td>' . $row['COLUMN_NAME'] . '</td>';
       $buff .= '<td>' . $row['SEQ_IN_INDEX'] . '</td>';
       $buff .= "</tr>";
    }
    $buff .= "</table>";
    return $buff;
  }


  // ; の後に改行を追加する。
  private function insertLf(string $str) : string {
     $result = str_replace(";", ";".chr(10), $str);
     $result .= chr(10);
     return $result;
  }

  // 折り返す。(Lfを挿入)
  private function wrapSpace(string $str) : string {
     $n = 120;
     $str1 = $str;
     $buff = '';
     $i = 0;
     $j = 0;
     while ($j < 1000) {
        $buff .= substr($str1, 0, $n);
        $buff .= chr(10);
        $str1 = substr($str1, $n);
        if (strlen($str1) == 0)
           break;
        $j++;
     }
     return $buff;
  }
}



//
//  メインプログラム
//  ==================
$p = new MyPage('MySQL-IS2.html');
$p->v['content'] = $p->getContent();
$p->v['title'] = 'MySQL-IS2';
$p->echo();

?>
