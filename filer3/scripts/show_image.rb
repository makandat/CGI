# 画像を表示する。
if params['path'].nil? then
  return %!<p style="color:red;">no parameter.</p>!
end

require "image_size"

html = ""
begin
  path = params['path']
  img = ImageSize.new(open(path))
  html = %!<img src="/Image/#{path}" alt="img" /><br />\n!
  html += "#{path}<br />\n"
  html += "type=" + img.get_type()
  html += " width=" + img.get_width().to_s
  html += " height=" + img.get_height().to_s
  html += "<br />\n"
rescue
  return %!<p style="color:red;">fatal error.</p>!
end

html
