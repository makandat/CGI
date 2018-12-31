#path = "/home/user/data/files.db"
#sql = "select n,path from info"
require "sqlite3"

db = SQLite3::Database.new(path)
result = ""

if sql =~ /^select\s|^pragma\s/ then
  rows = db.execute2(sql)
  if rows.size == 0 then
    result = "Result is empty!"
  else
    columns = nil
    result = "<table>\n"
    rows.each do |row|
      result += "<tr>"
      if columns.nil? then
        row.each do |col|
          result += ("<th>" + col.to_s + "</th>")
        end
        columns = row
      else
        row.each do |col|
          result += ("<td>" + col.to_s + "</td>")
        end
        result += "</tr>\n"
      end
    end
    result += "</table>\n"
  end
else
  r = db.execute(sql)
  result = "Done. " + r.to_s
end
#puts result
result
