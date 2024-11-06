# HtmlTable.py HTMLテーブルを作成する。
from typing import Union

# HTMLテーブルクラス
class Table:
  VERSION = "1.0.0"
  CLASS_TABLE = "table { border:solid 2px gray;border-collapse:collapse; }"
  CLASS_TH = "th { border:solid thin silver;border-collapse:collapse;background-color:gainsboro;padding:4px; }"
  CLASS_TD = "td { border:solid thin silver;;border-collapse:collapse;padding:3px; }"
  
  # コンストラクタ
  def __init__(self):
    self.__width = 0
    self.__height = 0
    self.__header = []
    self.__caption = ""
    self.class_table = ""
    self.class_th = ""
    self.class_tr_even = ""
    self.class_tr_odd = ""
    self.class_td = ""
    self.class_caption = ""
    self.__rows = list()
    return

  # 列数
  @property
  def width(self) -> int:
    return self.__width
  @width.setter
  def width(self, value:int):
    self.__width = value
    return
    
  # 行数  
  @property
  def height(self) -> int:
    return self.__height

  # ヘッダ行
  @property
  def header(self) -> list[str]:
    return self.__header
  @header.setter
  def header(self, value:list[str]):
    self.__header = value
    self.__width = len(self.__header)
    return

  # キャプション(表題)
  @property
  def caption(self) -> str:
    return self.__caption
  @caption.setter
  def caption(self, value):
    self.__caption = value
    return

  # データ行を追加する。
  def add_row(self, row:Union[list, tuple]) -> int:
    if self.__width == 0:
      self.__width = len(row)
    self.__rows.append(row)
    return len(self.__rows)

  # データ行を完全な HTML 文字列として追加する。
  def add_literal(self, row:str) -> int:
    self.__rows.append(row)
    return len(self.__rows)
   
  
  # セルの値を変更する。
  def change_value(self, row, col, value) -> None:
    self.__rows[row][col] = value
    return
  
  # 行を削除する。  
  def delete_row(self, row) -> None:
    del self.__rows[row]
    return
  
  # 文字列化する。
  def __str__(self):
    table = "<table>\n"
    if self.class_table != "":
      table = f'<table class="{self.class_table}">\n'
    # 表題 (キャプション)
    if self.caption != "":
      if self.class_caption == "":
        table += f'<caption>{self.cation}</caption>\n'
      else:
        table += f'<caption class="{self.class_caption}">{self.cation}</caption>\n'      
    # ヘッダ行
    if len(self.header) > 0:
      _header = "<tr>"
      if self.class_tr_even != "":
        _header = f'<td class="{self.class_tr}">'
      for item in self.header:
        if self.class_th == "":
          _header += Table.tag("th", item)
        else:
          _header += Table.tag("th", item, classname=self.class_th)
      _header += "</tr>\n"
      table += _header
    # データ行
    for i, row in enumerate(self.__rows):
      _row = "<tr>\n"
      if self.class_tr_even != "":
        _row = f'<tr class="{self.class_tr_even}">'
      for col in row:
        if self.class_td == "":
          table += Table.tag("td", col)
        else:
          if (i % 2) == 0:
            table += Table.tag("td", col, classname=self.class_tr_even)
          elif class_tr_odd != "":
            table += Table.tag("td", col, classname=self.class_tr_odd)
          else:
            table += Table.tag("td", col, classname=self.class_tr_even)
      _row += "</tr>\n"
      table += _row
    table += "</table>\n"
    return table

  # ファイル保存。as_html=True にするとブラウザ HTML として表示できるようにする。
  def save(self, path:str, as_html = False) -> None:
    htm = """<!DOCTYPE html">
 <html>
  <head>
   <title>{0}</title>
   <style>
    {2}
   </style>
  </head>
  <body style="margin-left:5%;margin-top:50px;">
    {1}
  </body>
 </html>"""
    with open(path, "wt", encoding="utf-8") as f:
      table = str(self)
      if as_html:
        css = Table.CLASS_TABLE + "\n" + Table.CLASS_TD + "\n" + Table.CLASS_TH
        htm = htm.format(path, table, css)
        f.write(htm)
      else:
        f.write(table)
    return

  # HTML タグを作る。
  @staticmethod
  def tag(tagname, text="", /, classname="", close=True, escape=True):
    html = f"<{tagname}>"
    if classname != "":
      html = f'<{tagname} class="{classname}">'
    s = text
    if type(text) is bytes:
      s = text.decode()
    if escape:
      s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    html += str(s)
    if close:
      html += f"</{tagname}>"
    return html

# テスト
if __name__ == "__main__":
  table = Table()
  table.header = ["A", "B", "C", "D"]
  table.add_row([1, 0, 0, "D1"])
  table.add_row([2, 10, 0, "D2"])
  table.add_row([3, 0, 20, "D3"])
  table.save("./table.html", True)
  print(table)
