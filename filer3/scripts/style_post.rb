begin
  config = "/home/user/workspace/sinatra/filer2/config.ini"
  f = open(config)
  str = ""
  while s = f.gets do
    if s =~ /stylesheet=/ then
      s = s1 = "stylesheet=/#{style}\n"
    end
    str += s
  end
  f.close

  f = open(config, "w")
  f.write(str)
  f.close
  message = 'OK. Please reload the page.<br /><p style="color:green;">' + s1 + '</p>'
rescue => e
  message = '<p style="color:red;">' + e.message + '</p>'
end
message
