# coding: utf-8
require "graph"

# Graphオブジェクトを作成する。
gra = Graph.new(700, 500, 0.0, 0.0, 64.0, 480.0)

# マージン設定
gra.margin_left = 5
gra.margin_bottom = 20
gra.margin_right = 55

# グラフデータを作成
points = Array.new
for x in 0..63 do
  xr = Float(x)
  points.push [xr, xr * xr / 2.0]
end

# 折れ線グラフを太さ２、青色で描画する。
gra.attributes(2, "blue", nil, nil)
gra.drawLines(points)

# 枠と目盛りを描画
gra.attributes(1, "black", nil, nil)
gra.drawFrame()
gra.drawText("(0, 0)", 5, 499)
gra.drawText("(64, 0)", 640, 499)
gra.drawText("(64, 480)", 620, 30)
gra.drawLine(634, 240, 644, 240)
gra.drawLine(325, 480, 325, 471)

# 結果をファイル保存
gra.save("/home/user/workspace/sinatra/filer2/public/svg/graph1a.svg")

<<HTML
<object type="image/svg+xml" data="/svg/graph1a.svg" width="700" height="500">graph</object>
HTML
