#!/usr/bin/python
import math
from cp3_llbb.Calculators42HDM.Calc2HDM import *
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np

split_to_subprocesses = True
process = 'bbH'
mode = 'H'
sqrts = 13000
type = 2
tb = 1.5
mh = 125.
mH = 500.
mA = 300.
mZ = 9.118760e+01
mhc = max(mH, mA)
m12 = math.sqrt(pow(mhc, 2) * tb / (1 + pow(tb, 2)))

mb = 4.92
mb__tilde__ = 4.92

if process =='ggH':
    muR = mH/2
    muF = muR
elif process == 'bbH':
    muR = (mA + mZ + mb + mb__tilde__ )
    muF =muR

beta=math.atan(tb)
cba = 0.01
alpha=math.atan(tb)-math.acos(cba)
sba = math.sin(math.atan(tb)-alpha)
# or simply : sba = math.sqrt(1 - pow(cba, 2))
outputFile = "out_mH-{}_mA-{}_tb-{}.dat".format(mH, mA, tb )

test = Calc2HDM(mode = 'H', sqrts = sqrts, type = type, tb = tb, m12 = m12, mh = mh, mH = mH, mA = mA, mhc = mhc, sba = sba, outputFile = outputFile, muR =muR, muF =muF)
test.setpdf('NNPDF31_nnlo_as_0118_nf_4_mc_hessian')
test.computeBR()

xsec_ggh, err_integration_ggh, err_muRm_ggh, err_muRp_ggh, xsec_bbh, err_integration_bbh, mb_MSscheme=  test.getXsecFromSusHi()
xsec_ggh = np.asarray(xsec_ggh)
xsec_bbh = np.asarray(xsec_bbh)

print( "*"*80)
print( 'MH-{} [GeV] , MA-{} [Gev] , tb-{}\n'.format( mH, mA, tb))
print( 'cross- section ggH: {} pb \n'.format(xsec_ggh))
print( 'cross- section bbH: {} pb \n'.format(xsec_bbh))
print( ' BR (H -> ZA): {}\n'.format(test.HtoZABR))
print( ' BR (A -> bb): {}\n'.format(test.AtobbBR))
print( ' BR (A -> bb)* BR (H -> ZA): {}\n'.format(test.AtobbBR*test.HtoZABR))

print( "*"*80)

subprocess_gg_nlo, subprocess_qg_nlo, subprocess_qq_nlo, integerror_gg_nlo, integerror_qg_nlo, integerror_qq_nlo=  test.getXsecFromSusHi(return_xsc_byComputationOrder =True)
print( subprocess_gg_nlo, subprocess_qg_nlo, subprocess_qq_nlo, integerror_gg_nlo, integerror_qg_nlo, integerror_qq_nlo)
subprocess_gg_nlo = np.asarray( subprocess_gg_nlo)
subprocess_qg_nlo = np.asarray( subprocess_qg_nlo)
subprocess_qq_nlo = np.asarray( subprocess_qq_nlo)


mA_list = [] 
xsec_ggh_list = []
xsec_bbh_list = []
subprocess_gg_nlo_list = []
subprocess_qg_nlo_list = []
subprocess_qq_nlo_list = []

HtoZABR_list = []
AtobbBR_list = [] 

fig= plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)

while mA < mH-mZ:
    test.setmA(mA)
    test.computeBR()
    mA_list.append(mA)
    
    xsec_ggh_X_BR = xsec_ggh*test.HtoZABR*test.AtobbBR
    xsec_bbh_X_BR = xsec_bbh*test.HtoZABR*test.AtobbBR
    
    xsec_bbh_list.append(xsec_bbh_X_BR)
    xsec_ggh_list.append(xsec_ggh_X_BR)
    
    subprocess_gg_nlo_X_BR = subprocess_gg_nlo#*test.HtoZABR*test.AtobbBR
    subprocess_qg_nlo_X_BR = subprocess_qg_nlo#*test.HtoZABR*test.AtobbBR
    subprocess_qq_nlo_X_BR = subprocess_qq_nlo#*test.HtoZABR*test.AtobbBR
    
    subprocess_gg_nlo_list.append(subprocess_gg_nlo_X_BR)
    subprocess_qg_nlo_list.append(subprocess_qg_nlo_X_BR)
    subprocess_qq_nlo_list.append(subprocess_qq_nlo_X_BR)
    
    HtoZABR_list.append(test.HtoZABR)
    AtobbBR_list.append(test.AtobbBR)
    
    mA+=2

if split_to_subprocesses :
    #plt.plot(mA_list,subprocess_gg_nlo_list, color='mediumturquoise', marker='o', label= 'gg [NLO]' )
    #plt.plot(mA_list,subprocess_qg_nlo_list, color='indigo', marker='o', label= 'qg [NLO]' )
    #plt.plot(mA_list,subprocess_qq_nlo_list, color='purple', marker='o', label= 'qq [NLO]' )
    plt.plot(mA_list,xsec_ggh_list, color='black', marker='o', label= 'gg-fusion' )
    plt.plot(mA_list,xsec_bbh_list, color='gold', marker='o', label='bb-associated production')
else:
    plt.plot(mA_list,xsec_ggh_list, color='black', marker='o', label= 'gg-fusion from SUSHI' )
    plt.plot(mA_list,xsec_bbh_list, color='gold', marker='o', label='bb-associated production')

plt.plot(mA_list,HtoZABR_list, color='red', linestyle='dashed', linewidth=1.5, label=r'$BR(H\rightarrow ZA)$')
plt.plot(mA_list,AtobbBR_list, color='b', linestyle='dashed', linewidth=1.5, label=r'$BR(A\rightarrow bb)$')
ax.axvspan((172.76- 1)*2 , (172.76+ 1)*2 , alpha=0.5, color='lightgrey', label=r'$2 x Top_{mass} \pm 1\sigma $')
plt.ylabel(r'$\sigma* BR(H\rightarrow ZA)* BR(A\rightarrow bb)[pb]$')
plt.ylabel('cross scetion [pb]')
plt.xlabel(r'$M_{A} [GeV]$')
plt.yscale('log')
plt.title(r'$2HDM-type%s: M_{H}=%s GeV, M_{H^+}=M_{H}, tan\beta= %s, cos(\beta-\alpha)= 0.01, mh= 125. GeV$'%(('I'if type==1 else('II')), mH, tb), fontsize=10.)
plt.xlim(min(mA_list), max(mA_list))
plt.legend()
#plt.grid()
fig.savefig('test_2hdm-type%s_tb-%s_mH-%s_splitProd-%s.png'%(type, tb, mH, split_to_subprocesses))
plt.gcf().clear()
