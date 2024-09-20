#!C:/Apps/Python3/python.exe
#  fetch_json.cgi
import for_cgi as cgi
import math

HTML_BODY = '''<script>
async function button1_click() {
  const URL = "http://localhost/cgi-bin/test/fetch_json.cgi?value=";
  const value_element = document.getElementById("value");
  const resp = await fetch(URL + value_element.value);
  const data = await resp.json();
  const message_element = document.getElementById("message");
  message_element.innerText = JSON.stringify(data);
}
</script>

<h1>fetch_json.cgi</h1>
<p style="padding:10px;"><a href="/cgi-bin/for_cgi/index.cgi">index.cgi へもどる</a></p>
<br />
<section style="margin-left:10%">
 <div>
  <label>Value (float) <input type="text" name="value" id="value" /></label>
 <div>
 <div style="margin-top:20px">
   <button type="button" id="button1" onclick="button1_click()">Query</button>
 </div>
</section>
<p id="message" class="message"></p>
'''

if cgi.qs_exists():
  params = cgi.get_params()
  x = float(params["value"])
  result = dict()
  result["round"] = round(x)
  result["floor"] = math.floor(x)
  result["ceil"] = math.ceil(x)
  result["fabs"] = math.fabs(x)
  cgi.send_json(result)
else:
  cgi.send_html(cgi.HTML_HEAD.format("fetch_json") + HTML_BODY + cgi.HTML_TAIL)
