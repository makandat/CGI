html = <<EOS
<script>
window.onload = function() {
  var canvas = document.getElementById('canvas1');
  var g = canvas.getContext('2d');

  var shape = "#{shape}";

  g.strokeStyle = "#000000";
  g.lineWidth = 2;
  g.beginPath();

  if (shape == "Line") {
    g.moveTo(100, 100);
    g.lineTo(300, 100);
    g.moveTo(150, 50);
    g.lineTo(150, 250);
  }
  else if (shape == "Rect")
    g.rect(50, 60, 260, 150);
  else if (shape == "Circle")
    g.arc(250, 250, 100, 0.0, 2.0 * Math.PI, false);
  else
    g.strokeText("error!", 200, 100);

  g.stroke();
}
</script>

<canvas id="canvas1" width="500" height="500" style="border: solid 1px black;">
canvas
</canvas>
EOS
