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
tb = 1.5
mh = 125.
mH = 500.
mA = 300.
mZ = 91.1876
mhc = max(mH, mA)
m12 = math.sqrt(pow(mhc, 2) * tb / (1 + pow(tb, 2)))

beta=math.atan(tb)
cba = 0.01
alpha=math.atan(tb)-math.acos(cba)
sba = math.sin(math.atan(tb)-alpha)
# orsimply : sba = math.sqrt(1 - pow(cba, 2))
outputFile = "out.dat"

test = Calc2HDM(mode = 'H', sqrts = sqrts, type = type, tb = tb, m12 = m12, mh = mh, mH = mH, mA = mA, mhc = mhc, sba = sba, outputFile = outputFile)
test.computeBR()

xsec_ggh, err_integration_ggh, err_muRm_ggh, err_muRp_ggh, xsec_bbh, err_integration_bbh =  test.getXsecFromSusHi()
xsec_ggh = np.asarray(xsec_ggh)
xsec_bbh = np.asarray(xsec_bbh)

mA_list = [] 
xsec_ggh_list = []
xsec_bbh_list = []
HtoZABR_list = []
AtobbBR_list = [] 

while mA < mH-mZ:
    test.setmA(mA)
    test.computeBR()
    mA_list.append(mA)
    xsec_ggh_X_BR = xsec_ggh*test.HtoZABR*test.AtobbBR
    xsec_bbh_X_BR = xsec_bbh*test.HtoZABR*test.AtobbBR
    xsec_bbh_list.append(xsec_bbh_X_BR)
    xsec_ggh_list.append(xsec_ggh_X_BR)
    HtoZABR_list.append(test.HtoZABR)
    AtobbBR_list.append(test.AtobbBR)
    mA+=2

plt.plot(mA_list,xsec_ggh_list, color='black', marker='o', label= 'gg-fusion' )
plt.plot(mA_list,xsec_bbh_list, color='gold', marker='o', label='bb-associated production')
plt.plot(mA_list,HtoZABR_list, color='red', linestyle='dashed', linewidth=1.5, label=r'$BR(H\rightarrow ZA)$')
plt.plot(mA_list,AtobbBR_list, color='b', linestyle='dashed', linewidth=1.5, label=r'$BR(A\rightarrow bb)$')
plt.ylabel(r'$\sigma* BR(H\rightarrow ZA)* BR(A\rightarrow bb)[pb]$')
plt.xlabel(r'$M_{A} [GeV]$')
plt.yscale('log')
plt.title(r'$2HDM-typeII: M_{H}=M_{A}+M{Z}, M_{H^+}=M_{H}, tan\beta= 1.5, cos(\beta-\alpha)= 0.01, mh= 125. GeV$', fontsize=10.)
plt.xlim(min(mA_list), max(mA_list))
plt.legend()
plt.grid()
plt.savefig('test.png')
