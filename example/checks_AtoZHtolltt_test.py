#!/bin/env python
import math
from cp3_llbb.Calculators42HDM.Calc2HDM import *
import json

mode = 'A' # means A-> ZH  or 'H' means H ->ZA
sqrts = 13000
type = 2
mh = 125
tb = 1.
sba = 0.99 # math.sqrt(1 - pow(cba, 2))
cba = math.sqrt(1 + pow(sba, 2))
mZ = 91.1876
ZtollBR =  3.3658 * 2 / 100. # no taus

mb = 4.92 # mb(OS) pole mass
mb__tilde__ = 4.92 # mb~
MZ= 9.118760e+01

results = {
    'mH': [],
    'mA': [],
    'ggh_sigma': [],
    'ggh_sigma_err': [],
    'BR': []
    }

def float_to_str(x, digits=2):
    tmp = ':.{:d}f'.format(digits)
    tmp = ('{' + tmp + '}').format(x)
    return tmp.replace('.', 'p')

for mA, mH in [
    (1000,600),
 ]:
    
    mhc = max(mH, mA)
    m12 = math.sqrt(pow(mhc, 2) * tb / (1 + pow(tb, 2)))
    
    muR4ggh = mA/2
    muF4ggh = muR4ggh
    print muR4ggh 
    outputFile = "2hdmc_results/2hdmc1.8.0_mA-{}_mH-{}.dat".format(mA, mH)
    x = Calc2HDM(mode = mode, sqrts = sqrts, type = type, tb = tb, m12 = m12, mh = mh, mH = mH, mA = mA, mhc = mhc, sba = sba, outputFile = outputFile, muR4ggh = muR4ggh, muF4ggh = muF4ggh)
    x.setpdf('NNPDF31_nnlo_as_0118_nf_4_mc_hessian')
    x.computeBR()
    xsec = x.getXsecFromSusHi()  
    xsec_ggH =  xsec["full"]['ggh'][0]
    xsec_ggH_err = xsec["full"]['ggh'][1]

    
    results['mH'].append(mH)
    results['mA'].append(mA)
    results['ggh_sigma'].append(xsec_ggH)
    results['ggh_sigma_err'].append(xsec_ggH_err)
    results['BR'].append(x.AtoZHBR * x.HtottBR * ZtollBR)

with open('AToZH_xsc_br_results.json', 'w+') as f:
    json.dump(results, f)
