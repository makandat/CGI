# coding: utf-8
require "matrix"
require "complex"

$result = "<pre>"

def put(v)
  $result += v.to_s
  $result += "\n" 
end

a = Vector[Complex(0.0, 1.0), Complex(1.0, 0.0)]
b = Vector[Complex(-1.0, 1.0), Complex(1.0, -1.0)]

put a.r
put a.inner_product(b)

th = 30.0 * Math::PI / 180.0
m = Matrix[[Complex(Math.cos(th), -Math.sin(th)), Complex(Math.sin(th), Math.cos(th))], 
           [Complex(1.0, 0.0), Complex(0.0, 1.0)]]

c = m * b
put c

$result + "</pre>"
