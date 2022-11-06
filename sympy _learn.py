from sympy import *
init_printing(use_unicode=True)

x = Symbol('x')

f = (1 + x * 491/200) * exp(-x*(1 + 491/200)) - 0.0156
a = solve(f, x)
# a = -(200 * LambertW(0, -(26949*exp(-691/491))/1227500))/691 - 200/491


print(a[1].evalf())

