require "html5_maker"

class Canvas1 < CanvasMaker
  def initialize()
    super('canvas1', 600, 400)
    @code = "<script>\nwindow.onload = function() {\n"
    @html = ""
  end

  def get_code()
    @code << init_canvas2d()
    @code << set_attr(2, '#008040', "rgb(0xe0, 0xe0, 0xf8)")
    @code << rectangle(200, 200, 200, 150)
    @code << set_attr(2, '#004000', "rgb(0x70, 0xe0, 0xf8)")
    @code << circle(200, 200, 120)
    @code << set_attr(2, '#000040', "rgb(0xf0, 0x90, 0xf8)")
    @code << ellipse(100, 80, 70, 120)
    @code << "}\n"
    @code << "</script>\n"
    return @code
  end

  def get_html()
    @html << canvas()
    return @html
  end

  def to_s()
    get_code() + get_html()
  end
end


can1 = Canvas1.new
can1.to_s()
