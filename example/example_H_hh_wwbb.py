#!/usr/bin/python


import math
from cp3_llbb.Calculators42HDM.Calc2HDM import *
import matplotlib.pyplot as plt

mode = 'H'
sqrts = 13000
type = 2
tb = 1
m12 = 0
mh = 125
mH = 200
mA = 200
mhc = mH

beta=math.atan(tb)
cba = 0.1
alpha=math.atan(tb)-math.acos(cba)
sba = math.sin(math.atan(tb)-alpha)

print 'sba : ', sba

outputFile = "out.dat"


test = Calc2HDM(mode = 'H', sqrts = sqrts, type = type, tb = tb, m12 = m12, mh = mh, mH = mH, mA = mA, mhc = mhc, sba = sba, outputFile = outputFile)

mH_list = [] 
xsectot_list = []
HtohhBR_list = []
htobbBR_list = [] 
htowwBR_list = []

while  mH < 900:
    test.setmH(mH)
    test.setmA(mH)
    test.mhc = mH
    xsec = test.getXsecFromSusHi()
    test.computeBR()
    mH_list.append(mH)
    xsectot_list.append(xsec*test.HtohhBR*test.htobbBR*test.htoWWBR)
    mH+=10

plt.plot(mH_list,xsectot_list, color='black')

plt.ylabel(r'$\sigma$ ($pp \rightarrow H$) $\times$ BR($H \rightarrow hh \rightarrow bbWW$)')
plt.xlabel(r'$m_H$ [GeV]')

plt.savefig('test_hh.png')
