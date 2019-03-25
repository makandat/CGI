#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
require "./WebPage.pm";
require "./MySQL.pm";

use constant TEMPLATE => "./templates";

our $cgi = WebPage->new(TEMPLATE . "/Colors.html");
our $client = MySQL->new;

# 表を作成
sub showColors {
  my @rows = $client->query("SELECT * FROM colors ORDER BY color");
  my $table_rows = "";
  my $color;
  foreach my $row (@rows) {
    $table_rows .= "<tr><td>";
    $table_rows .= $row->[0];
    $table_rows .= "</td><td>";
    $color = $row->[1];
    $table_rows .= $color;
    $table_rows .= "</td><td style=\"background-color:$color\">";
    $table_rows .= "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
    $table_rows .= "</td></tr>\n";
  }
  $cgi->setPlaceHolder('COLORS', $table_rows);
}

# 表に追加
sub addNew {
  my $code = $cgi->getParam('code');
  my $name = $cgi->getParam('name');
  my $b = 1;
  my $sql = "INSERT INTO colors VALUES('$code', '$name')";
  $client->execute($sql) or $b = 0;
  if ($b) {
    $cgi->setPlaceHolder('message', $name . " was added.");
  }
  else {
    $cgi->setPlaceHolder('message', "Error: " . $name . " was NOT added.");
  }
}

#  メイン
$cgi->setPlaceHolder('message', '');
if ($cgi->isPostback('code')) {
  addNew();
}
showColors();
$cgi->echo();
