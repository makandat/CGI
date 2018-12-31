f = 2.0
array = "["
720.times do |i|
  x = Math::PI * i / 180.0
  y = Math.sin(f * x)
#  printf("%f, %f\n", x, y)
  array << y.to_s << ","
end
array.chop!
array << "]\n"
#puts array

<<HTML
<script>
window.onload = function() {
  var canvas1 = document.getElementById('canvas1');
  var g = canvas1.getContext('2d');
  var data = #{array};
  var x, y;

  g.strokeStyle = "#004040";
  g.lineWidth = 2;
  g.beginPath();
  for (x = 0; x < 720; x++) {
    y = -data[x] * 200 + 200;
    if (x == 0)
      g.moveTo(x, y);
    else
      g.lineTo(x, y);
  }
  g.stroke();
}
</script>
<p>
<canvas id="canvas1" width="720" height="400" style="border:solid 1px black">canvas</canvas>
</p>
HTML
