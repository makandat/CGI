# coding: utf-8

if n.nil? then
  return 'error! parameter n must be specified.<br />'
end

html = "<span style='color:green;'>"
n.times do |i|
  html += i.to_s
  html += "<br />"
end
html += "</span>Done.<br />"
html

