require "css_maker"

class Css < CSSMaker
  def initialize()
    super()

    new_style({:id=>'top'})
      text_align({:align=>'center'})
      font({:color=>'#004040;'})
    close_style()

    new_style({:tag=>'div', :cls=>'box1'})
      border({:style=>'solid', :color=>'brown', :width=>'1px', :padding=>'5px'})
      background({:color=>'#e0e0ff'})
    close_style()

    new_style({:tag=>'div', :cls=>'box2'})
      border({:style=>'solid', :color=>'gray', :width=>'1px', :padding=>'5px'})
    close_style()

    new_style({:tag=>'span', :cls=>'emp'})
      font({:bold=>true, :color=>'brown'})
    close_style()

    new_style({:tag=>'a:link'})
      literal(" text-decoration:none;\n color:green;")
    close_style()

    new_style({:tag=>'a:visited'})
      literal(" text-decoration:none;\n color:green;")
    close_style()
  end
end

cm = Css.new
css = cm.toString()

<<HTML
<style>
#{css}
</style>

<h1 id="top">CSSMaker</h1>
<a href="javascript:history.back();">[back]</a>
<div class="box1">
color: 文字の色 (例) "red"<br />
    またはパラメータ名のシンボルをキーとするハッシュ。(例) {:color=>"red", :size="larger"}
size: 文字のサイズ (例) "24pt"<br />
bold: 太い文字の指定<br />
italic: 斜体文字の指定<br />
underline: 下線の有無の指定<br />
strike: 打ち消し線の有無の指定<br />
family: 字体の指定 (例) courier, "MS 明朝"<br />
</div>
<br />
<div class="box2">
<span class="emp">align</span>: 整列方法 (left,right,center,justify,inheritなど)<br />
<span class="emp">indent</span>: 字下げ (例) 1em, 10%<br />
<span class="emp">vertical</span>: 縦方向の整列方法 (top,middle,bottomなど)。tdタグなどで利用可能。 <br />
</div>

HTML
