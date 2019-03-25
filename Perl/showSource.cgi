#!/usr/bin/perl
#  ソースプログラムを表示する。showSource.cgi?path=/home/user/workspace/..
use strict;
use warnings;

my $html = <<EOS;
<!doctype html>
<html>
<head>
 <meta charset="utf-8" />
 <title>FILENAME</title>
 <style>
  body {
    margin-left: 5%;
    margin-right: 5%;
    background-color:mintcream;
  }
  h1 {
    text-align:center;
    color:mediumvioletred;
  }
  h3 {
    padding:8px;
    color:palevioletred;
    text-align:center;
  }
  pre {
    border:solid thin silver;
    padding:5px;
    background-color:white;
    font-size:12pt;
  }
 </style>
 <script src="/js/jquery.min.js"></script>
 <link rel="stylesheet" href="/js/highlight/styles/vs.css">
 <script src="/js/highlight/highlight.pack.js"></script>
 <script>hljs.initHighlightingOnLoad();</script>
</head>

<body>
<h1>FILENAME ソース表示</h1>
<h3>PATH</h3>
<pre><code>SOURCE</code></pre>

<p>&nbsp;</p>
<p style="text-align:center;"><a href="#top">TOP</a></p>
<p>&nbsp;</p>
<p>&nbsp;</p>
</body>
</html>
EOS


# メインプログラム

my $q = $ENV{'QUERY_STRING'};
my @qs = split('=', $q);
my $path = $qs[1];
my @path_parts = split('/', $path);
my $filename = $path_parts[$#path_parts];
$html =~ s/PATH/$path/g;
if (-f $path) {
  open(FH, "<", $path);
  my $source = '';
  while (<FH>) {
    $source .= $_;
  }
  close(FH);
  $source =~ s/&/&amp;/g;
  $source =~ s/</&lt;/g;
  $source =~ s/>/&gt;/g;
  $html =~ s/SOURCE/$source/g;
  $html =~ s/FILENAME/$filename/g;
}
else {
  $html =~ s/SOURCE/Not found $path/g;
}

print "Content-Type: text/html\n\n";
print $html;

