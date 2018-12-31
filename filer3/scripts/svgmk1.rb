require "svg_maker"

Path = '/home/user/workspace/sinatra/filer/public/svg/circle.svg'
svg = SVGMaker.new(500, 500)
svg.circle(250, 250, 100)
svg.save(Path)

result = <<EOS
<object type="image/svg+xml" data="/svg/circle.svg" width="500" height="500">
circle
</object>
EOS
result << "<h4>" << Path  << "</h4>"
result

