# -*- coding: utf-8 -*-
# SVG Library  ver 1.2  2019-08-31

VERSION   = "1.2"

XmlHeader = '<?xml version="1.0" encoding="utf-8" standalone="no" ?>'
SvgSTART  = '<svg width="{0}" height="{1}" version="1.1" xmlns="http://www.w3.org/2000/svg">'
TITLE     = "<title>{0}</title>"

LINE      = '<line x1="{0}" y1="{1}" x2="{2}" y2="{3}" style="fill:{4};stroke:{5};stroke-width:{6};" />'
CIRCLE    = '<circle cx="{0}" cy="{1}" r="{2}" style="fill:{3};stroke:{4};stroke-width:{5};fill-opacity:{6};filter:{7};" />'
ELLIPSE   = '<ellipse cx="{0}" cy="{1}" rx="{2}" ry="{3}" style="fill:{4};stroke:{5};stroke-width:{6};fill-opacity:{7};filter:{8};" />'
RECTANGLE = '<rect x="{0}" y="{1}" width="{2}" height="{3}" style="fill:{4};stroke:{5};stroke-width:{6};fill-opacity:{7};filter:{8}" />'
POLYLINE  = '<polyline points="{0}" style="fill:{1};stroke:{2};stroke-width:{3};fill-opacity:{4};" />'
POLYGON   = '<polygon points="{0}" style="fill:{1};stroke:{2};stroke-width:{3};fill-opacity:{4};filter:{5};" />'
PATH      = '<path d="{0}" style="fill:{1};stroke:{2};stroke-width:{3};fill-opacity:{4};filter:{5};" />'
TEXT      = '<text x="{0}" y="{1}" stroke="{2}" font-family="{3}" font-size="{4}">'
VIEWBOX   = '<svg viewBox="{0} {1} {2} {3}" xmlns="http://www.w3.org/2000/svg">'

FILTER_BLUR = '''<!-- ぼかし -->
  <filter id="blur" x="{0}" y="{1}" width="{2}" height="{3}" filterUnits="userSpaceOnUse">
    <feGaussianBlur stdDeviation="{4}" />
  </filter>
'''

# クラス定義
class SVG :

  # コンストラクタ
  def __init__(self, width:int, height:int, title='Made by the SVG class', xheader=True) :
    self.width = width
    self.height = height
    self.filters = {}
    self.init(width, height, title, xheader)
    self.init_filters()
    return
    
  # 描画色
  @property
  def stroke(self) :
    return self.style["stroke"]

  @stroke.setter
  def stroke(self, value) :
    self.style["stroke"] = value
    return

  # 背景色
  @property
  def fill(self) :
    return self.style["fill"]

  @fill.setter
  def fill(self, value) :
    self.style["fill"] = value
    return

  # 線幅
  @property
  def stroke_width(self) :
    return self.style["stroke-width"]

  @stroke_width.setter
  def stroke_width(self, value) :
    self.style["stroke-width"] = value
    return

  # 透過度
  @property
  def fill_opacity(self) :
    return self.style["fill-opacity"]

  @fill_opacity.setter
  def fill_opacity(self, value) :
    self.style["fill-opacity"] = value
    return

  # フォントサイズ
  @property
  def font_size(self) :
    return self.style["font-size"]

  @font_size.setter
  def font_size(self, value) :
    self.style["font-size"] = value
    return

  # フォント種別
  @property
  def font_family(self) :
    return self.style["font-family"]

  @font_family.setter
  def font_family(self, value) :
    self.style["font-family"] = value
    return

  # フィルタ
  @property
  def filter(self) :
    return self.style["filter"]

  @filter.setter
  def filter(self, value) :
    self.style["filter"] = value
    return


  # SVG データをクリアして新しく作り直せるようにする。
  def init(self, width:int, height:int, title:str, xheader:bool) -> None :
    self.style = {"stroke":"black", "fill":"transparent", "stroke-width":1, "fill-opacity":1, "font-size":16, "font-family":"arial", "filter":"none"}
    svg_begin = SvgSTART.format(width, height)
    self.lines = []
    if xheader :
      self.lines.append(XmlHeader)
    self.lines.append(svg_begin)
    self.lines.append(TITLE.format(title))
    return

  # フィルタ初期化 (フィルタを使う場合は、通常オーバーライドが必要)
  def init_filters(self) :
    self.filters['blur'] = FILTER_BLUR.format(0, 0, 640, 480, 5)
    return
    
  # ファイル保存
  def save(self, filePath: str, usefilter=False) -> None:
    svg = self.toXml()
    with open(filePath, "w", encoding="utf-8") as f :
      f.write(svg)
    return

  # XML 文字列に変換
  def toXml(self, usefilter=False) :
    if usefilter :
      self.lines.append('<defs>')
      for key in self.filters.keys() :
        self.lines.append(self.filters[key])
      self.lines.append('</defs>')
    svg = ""
    for line in self.lines :
      svg += line + "\n"
    svg += "</svg>\n"
    return svg

  # 他の SVG オブジェクトを結合する。
  def append(self, svg) :
    i = 0
    for line in svg.lines :
      if i < 3 :
        pass
      else :
        self.lines.append(line)  
      i += 1
    return

  # svg タグ (HTML 直接埋め込み用) 作成
  def svgtag(self, usefilter=False) :
    tag = f'<svg x="0px" y="0px" width="{self.width}px" height="{self.height}px" viewBox="{0} {0} {self.width} {self.height}">'
    if usefilter :
      self.lines.append('<defs>')
      for key in self.filters.keys() :
        self.lines.append(self.filters[key])
      self.lines.append('</defs>')
    for i in range(len(self.lines) -2) :
      tag += self.lines[i + 2] + "\n"
    tag += "</svg>\n"
    return tag
    
  # 直線
  def line(self, x1:float, y1:float, x2:float, y2:float) -> str:
    shape = LINE.format(x1, y1, x2, y2, self.fill, self.stroke, self.stroke_width)
    self.lines.append(shape)
    return shape

  # 破線
  def dashline(self, x1:float, y1:float, x2:float, y2:float, dasharray="4") -> str:
    DASHLINE = '<line x1="{0}" y1="{1}" x2="{2}" y2="{3}" style="fill:{4};stroke:{5};stroke-width:{6};stroke-dasharray:{7}" />'
    shape = DASHLINE.format(x1, y1, x2, y2, self.fill, self.stroke, self.stroke_width, dasharray)
    self.lines.append(shape)
    return shape
    
  # 円
  def circle(self, cx:float, cy:float, r:float) -> str :
    shape = CIRCLE.format(cx, cy, r, self.fill, self.stroke, self.stroke_width, self.fill_opacity, self.filter)
    self.lines.append(shape)
    return shape
    
  # 楕円
  def ellipse(self, cx:float, cy:float, rx:float, ry:float) -> str :
    shape = ELLIPSE.format(cx, cy, rx, ry, self.fill, self.stroke, self.stroke_width, self.fill_opacity, self.filter)
    self.lines.append(shape)
    return shape

  # 矩形
  def rectangle(self, x:float, y:float, width:float, height:float) -> str:
    shape = RECTANGLE.format(x, y, width, height, self.fill, self.stroke, self.stroke_width, self.fill_opacity, self.filter)
    self.lines.append(shape)
    return shape

  # 折れ線
  def polyline(self, points) -> str:
    pv = SVG.pointsToString(points)
    shape = POLYLINE.format(pv, self.fill, self.stroke, self.stroke_width, self.fill_opacity, self.filter)
    self.lines.append(shape)
    return shape
    
  # 多角形
  def polygon(self, points) -> str:
    pv = SVG.pointsToString(points)
    shape = POLYGON.format(pv, self.fill, self.stroke, self.stroke_width, self.fill_opacity, self.filter)
    self.lines.append(shape)
    return shape
    
  # 経路
  def path(self, directives) -> str :
    pv = ""
    for cmd in directives :
      pv += (cmd + " ")
    pv += "Z"
    shape = PATH.format(pv, self.fill, self.stroke, self.stroke_width, self.fill_opacity, self.filter)
    self.lines.append(shape)
    return shape

  # テキスト
  def drawtext(self, x:float, y:float, text:str) -> str :
    stext = TEXT.format(x, y, self.stroke, self.font_family, self.font_size)
    stext += text
    stext += "</text>"
    self.lines.append(stext)
    return stext

  # ビューポートを開始
  def viewport(self, x:int, y:int, width:int, height:int) -> str :
    shape = VIEWBOX.format(x, y, width, height)
    self.lines.append(shape)
    return shape

  # ビューポートを終了
  def close_viewport(self) :
    shape = "</svg>"
    self.lines.append(shape)
    return shape
    

  # 点のリストを文字列に変換する。
  @staticmethod
  def pointsToString(points) :
    pv = ""
    for point in points :
      pv += "{0} {1} ".format(point[0], point[1])
    pv = pv.strip()
    return pv
    
  
