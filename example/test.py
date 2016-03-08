#!/usr/bin/python


from cp3_llbb.Calculators42HDM.Calc2HDM import *


test = Calc2HDM()
test.computeBR()

print "ZZ BR", test.HtoZZBR

print "xsec : ",  test.getXsecFromSusHi()



