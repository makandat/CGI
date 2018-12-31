require "rubygems"
require "image_size"

html = ""
img = nil
begin
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
