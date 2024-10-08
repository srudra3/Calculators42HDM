#!/bin/env python
import math
from cp3_llbb.Calculators42HDM.Calc2HDM import *
import json
import matplotlib.pyplot as plt
import numpy as np
mode = 'A' # means A-> ZH  or 'H' means H ->ZA
sqrts = 13000
type = 2
mh = 125
tb = 1.5 
sba = 0.99995 # math.sqrt(1 - pow(cba, 2))
#cba = math.sqrt(1 + pow(sba, 2))
cba = 0
mZ = 91.1876
ZtollBR =  (3.3632 + 3.3662 + 3.3696)/ 100. #including taus

mb = 4.92 # mb(OS) pole mass
mb__tilde__ = 4.92 # mb~
MZ= 9.118760e+01

#results = {
#    'mH': [],
#    'mA': [],
#    'ggh_sigma': [],
#    'bbh_sigma': [],
#    'bbh_sigma_err': [],
#    'ggh_sigma_err': [],
#    'BR': [],
#    'xsecxBR': []
#    }

results = {}
total_results = {}




def float_to_str(x, digits=2):
    tmp = ':.{:d}f'.format(digits)
    tmp = ('{' + tmp + '}').format(x)
    return tmp.replace('.', 'p')

for mA, mH in [
    (430,330),
    (450,330),
    (450,350),
    (500,330),
    (500,350),
    (500,370),
    (500,400),
    (550,330),
    (550,350),
    (550,400),
    (550,450),
    (600,330),
    (600,350),
    (600,400),
    (600,450),
    (600,500),
    (650,330),
    (650,350),
    (650,400),
    (650,450),
    (650,500),
    (650,550),
    (700,330),
    (700,350),
    (700,370),
    (700,400),
    (700,450),
    (700,500),
    (700,550),
    (700,600),
    (750,330),
    (750,350),
    (750,400),
    (750,450),
    (750,500),
    (750,550),
    (750,600),
    (750,650),
    (800,330),
    (800,350),
    (800,400),
    (800,450),
    (800,500),
    (800,550),
    (800,600),
    (800,650),
    (800,700),
    (850,330),
    (850,350),
    (850,400),
    (850,450),
    (850,500),
    (850,550),
    (850,600),
    (850,650),
    (850,700),
    (850,750),
    (900,330),
    (900,350),
    (900,370),
    (900,400),
    (900,450),
    (900,500),
    (900,550),
    (900,600),
    (900,650),
    (900,700),
    (900,750),
    (900,800),
    (950,330),
    (950,350),
    (950,400),
    (950,450),
    (950,500),
    (950,550),
    (950,600),
    (950,650),
    (950,700),
    (950,750),
    (950,800),
    (950,850),
    (1000,330),
    (1000,350),
    (1000,400),
    (1000,450),
    (1000,500),
    (1000,550),
    (1000,600),
    (1000,650),
    (1000,700),
    (1000,750),
    (1000,800),
    (1000,850),
    (1000,900),
    (1050,330),
    (1050,350),
    (1050,400),
    (1050,450),
    (1050,500),
    (1050,550),
    (1050,600),
    (1050,650),
    (1050,700),
    (1050,750),
    (1050,800),
    (1050,850),
    (1050,900),
    (1050,950),
    (1100,330),
    (1100,350),
    (1100,400),
    (1100,450),
    (1100,500),
    (1100,550),
    (1100,600),
    (1100,650),
    (1100,700),
    (1100,750),
    (1100,800),
    (1100,850),
    (1100,900),
    (1100,950),
    (1100,1000),
    (1150,330),
    (1150,350),
    (1150,450),
    (1150,550),
    (1150,650),
    (1150,750),
    (1150,850),
    (1150,950),
    (1150,1050),
    (1200,330),
    (1200,350),
    (1200,400),
    (1200,500),
    (1200,600),
    (1200,700),
    (1200,800),
    (1200,850),
    (1200,900),
    (1200,1000),
    (1200,1100),
    (1300,350),
    (1300,400),
    (1300,500),
    (1300,600),
    (1300,700),
    (1300,800),
    (1300,900),
    (1300,1000),
    (1300,1100),
    (1300,1200),
    (1400,350),
    (1400,400),
    (1400,500),
    (1400,600),
    (1400,700),
    (1400,800),
    (1400,900),
    (1400,1000),
    (1400,1100),
    (1400,1200),
    (1400,1300),
    (1500,350),
    (1500,400),
    (1500,500),
    (1500,600),
    (1500,700),
    (1500,800),
    (1500,900),
    (1500,1000),
    (1500,1100),
    (1500,1200),
    (1500,1300),
    (1500,1400),
    (1600,350),
    (1600,400),
    (1600,500),
    (1600,600),
    (1600,700),
    (1600,800),
    (1600,900),
    (1600,1000),
    (1600,1100),
    (1600,1200),
    (1600,1300),
    (1600,1400),
    (1600,1500),
    (1700,350),
    (1700,400),
    (1700,500),
    (1700,600),
    (1700,700),
    (1700,800),
    (1700,900),
    (1700,1000),
    (1700,1100),
    (1700,1200),
    (1700,1300),
    (1700,1400),
    (1700,1500),
    (1700,1600),
    (1800,350),
    (1800,400),
    (1800,500),
    (1800,600),
    (1800,700),
    (1800,800),
    (1800,900),
    (1800,1000),
    (1800,1100),
    (1800,1200),
    (1800,1300),
    (1800,1400),
    (1800,1500),
    (1800,1600),
    (1800,1700),
    (1900,350),
    (1900,400),
    (1900,500),
    (1900,600),
    (1900,700),
    (1900,800),
    (1900,900),
    (1900,1000),
    (1900,1100),
    (1900,1200),
    (1900,1300),
    (1900,1400),
    (1900,1500),
    (1900,1600),
    (1900,1700),
    (1900,1800),
    (2000,350),
    (2000,400),
    (2000,500),
    (2000,600),
    (2000,700),
    (2000,800),
    (2000,900),
    (2000,1000),
    (2000,1100),
    (2000,1200),
    (2000,1300),
    (2000,1400),
    (2000,1500),
    (2000,1600),
    (2000,1700),
    (2000,1800),
    (2000,1900),
    (2100,350),
    (2100,400),
    (2100,500),
    (2100,600),
    (2100,700),
    (2100,800),
    (2100,900),
    (2100,1000),
    (2100,1100),
    (2100,1200),
    (2100,1200),
    (2100,1300),
    (2100,1400),
    (2100,1500),
    (2100,1600),
    (2100,1700),
    (2100,1800),
    (2100,1900),
    (2100,2000) ]:
    mhc = max(mH, mA)
    sinb = tb/(math.sqrt(pow(tb,2)+1))
    cosb = 1/(math.sqrt(pow(tb,2)+1))
    m12 = math.sqrt(pow(mH, 2)*sinb*cosb)
    
    muR4ggh = 0.5 
    muF4ggh = muR4ggh
    outputFile = "2hdmc_results/2hdmc1.8.0_mA-{}_mH-{}.dat".format(mA, mH)
    x = Calc2HDM(mode = mode, sqrts = sqrts, type = type, tb = tb, m12 = m12, mh = mh, mH = mH, mA = mA, mhc = mhc, sba = sba, outputFile = outputFile, muR4ggh = muR4ggh, muF4ggh = muF4ggh)
    x.setpdf('NNPDF31_nnlo_as_0118_nf_4_mc_hessian')
    x.computeBR()
    print("Warning: {} not created!".format(outputFile))

    xsec = x.getXsecFromSusHi()
    xsec_ggH =  xsec["full"]['ggh'][0]
    xsec_ggH_err = xsec["full"]['ggh'][1]
    xsec_bbH =  xsec["full"]['bbh'][0]
    xsec_bbH_err =  xsec["full"]['bbh'][1]
#    xsec_ggH, err_integration_ggH, err_muRm_ggH, err_muRp_ggH, xsec_bbH, err_integration_bbH, mb_MSscheme_muR= x.getXsecFromSusHi()
    #print ( " xsec( gg-fusion), AtoZHBR, HtottBR ", xsec_ggH, x.AtoZHBR, x.HtottBR )
    
    results["{mA},{mH}".format(mA=mA,mH=mH)] = {"AtoZHBR":x.AtoZHBR, "HtottBR":x.HtottBR, "xsec_ggH":xsec_ggH}
    
    total_results["{mA},{mH}".format(mA=mA,mH=mH)] = x.AtoZHBR*x.HtottBR*xsec_ggH*ZtollBR
    #results['mH'].append(mH)
    #results['mA'].append(mA)
    #results['ggh_sigma'].append(xsec_ggH)
    #results['bbh_sigma'].append(xsec_bbH)
    #results['ggh_sigma_err'].append(xsec_ggH_err)
    #results['bbh_sigma_err'].append(xsec_bbH_err)
    #results['BR'].append(x.AtoZHBR * x.HtottBR * ZtollBR)
    #results['xsecxBR'].append(xsec_ggH*x.AtoZHBR * x.HtottBR * ZtollBR)
    
#plt.plot(results['mA'], results['ggh_sigma'], color='black', marker='o', label= 'gg-fusion from SUSHI')
#plt.plot(results['mA'], results['bbh_sigma'], color='red', marker='o', label= 'bb-associated production')

#plt.ylabel(r'$\sigma$ ($pp \rightarrow A$) $\times$ BR($A \rightarrow ZH \rightarrow lltt$)')
#plt.ylabel(r'$\sigma$ ($pp \rightarrow A$)')
#plt.xlabel(r'm_A$ [GeV]')
#plt.title(r'$2HDM-typeII:  M_{H^-+}=M_{A}, tan\beta= 1, cos(\beta-\alpha)= 0, mh= 125. GeV$', fontsize=10.)
#plt.yscale('log')
#plt.legend()
#plt.savefig('pptoAxsec.png')
with open('total_xsec_results_tanb1.json', 'w+') as f:
    json.dump(total_results, f)
with open('AToZH_xsc_br_results_tanb1.json', 'w+') as f:
    json.dump(results, f)
