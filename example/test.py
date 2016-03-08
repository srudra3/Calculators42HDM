#!/usr/bin/python


from cp3_llbb.Calculators42HDM.Calc2HDM import *


mode = 'H'
sqrts = 13000
type = 2
tb = 1
m12 = 0
mh = 125
mH = 350
mA = 400
mhc = 420
sba = 0.99
outputFile = "out.dat"


test = Calc2HDM(mode = 'H', sqrts = sqrts, type = type, tb = tb, m12 = m12, mh = mh, mH = mH, mA = mA, mhc = mhc, sba = sba, outputFile = outputFile)
test.computeBR()


print "ZZ BR", test.HtoZZBR

print "xsec : ",  test.getXsecFromSusHi()


test.setmA(200)
test.computeBR()
print "ZZ BR", test.HtoZZBR
