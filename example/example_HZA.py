#!/usr/bin/python


import math
from cp3_llbb.Calculators42HDM.Calc2HDM import *
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np

mode = 'H'
sqrts = 13000
type = 2
tb = 1
m12 = 0
mh = 125
mH = 300
mA = 50
mhc = mH

beta=math.atan(tb)
cba = 0.01
alpha=math.atan(tb)-math.acos(cba)
sba = math.sin(math.atan(tb)-alpha)

print 'sba : ', sba

outputFile = "out.dat"


test = Calc2HDM(mode = 'H', sqrts = sqrts, type = type, tb = tb, m12 = m12, mh = mh, mH = mH, mA = mA, mhc = mhc, sba = sba, outputFile = outputFile)
test.computeBR()

xsec =  test.getXsecFromSusHi()

xsec = np.asarray(xsec)

mA_list = [] 
xsectot_list = []
HtoZABR_list = []
AtobbBR_list = [] 

while mA < mH-90:
    test.setmA(mA)
    test.computeBR()
    print "ZA BR", test.HtoZABR
    mA_list.append(mA)
    xsec_times_BR = xsec*test.HtoZABR*test.AtobbBR*0.067
    xsectot_list.append(xsec_times_BR)
    HtoZABR_list.append(test.HtoZABR)
    AtobbBR_list.append(test.AtobbBR)
    mA+=2

plt.plot(mA_list,xsectot_list, color='black')
plt.plot(mA_list,HtoZABR_list, color='red')
plt.plot(mA_list,AtobbBR_list, color='green')

plt.savefig('test.png')
