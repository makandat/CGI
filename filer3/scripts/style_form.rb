option = ""
Dir.glob("/home/user/workspace/sinatra/filer2/public/*.css") do |css|
  option << "<option>" << File.basename(css) << "</option>\n"
end

form = <<EOS
<!DOCTYPE html>
<html>
<head>
<title>Change theme</title>
</head>
<body>
<h2>Change theme</h2>
<form name="form1" method="post" action="/script_window/">
<input type="hidden" name="path" value="/home/user/workspace/sinatra/filer2/scripts/style_post.rb" />
style: <select name="style">
%option%
</select><br />
<input type="submit" value="set" /><br />
</form>
</body>
</html>
EOS

form.gsub!('%option%', option)
form
