#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
require "./WebPage.pm";
require "./Common.pm";
require "./FileSystem.pm";
require "./Text.pm";

use constant TEMPLATE => "./templates";
use constant HTDOC => '/var/www/html';

our $cgi = WebPage->new(TEMPLATE . "/ImgDir.html");

my @files = FileSystem::listFiles(HTDOC . "/img");
my $list = "";
my $file = "";
foreach (@files) {
  $list .= "<li>";
  $file = FileSystem::getFileName($_);
  $list .= "<img src=\"/img/$file\" />";
  $list .= "<br />$file";
  $list .= "</li>\n";
}
$cgi->setPlaceHolder('LIST', $list);
$cgi->setPlaceHolder('TITLE', HTDOC."/img");
$cgi->echo();
