#!/bin/env python

import math
from cp3_llbb.Calculators42HDM.Calc2HDM import *
import json

# Alex's PhD thesis parameters
#mode = 'H'
sqrts = 13000
type = 2
mh = 125
tb = 1.5
cba = 0.01
sba = math.sqrt(1 - pow(cba, 2))
mZ = 91.1876
outputFile = "out.dat"
ZtollBR =  3.3658 * 2 / 100. # no taus

process = 'ggH'
mb = 4.92 # mb(OS) pole mass
mb__tilde__ = 4.92 # mb~
MZ= 9.118760e+01

results = {
    'mH': [],
    'mA': [],
    'sigma': [],
    'sigma_errIntegration': [],
    'sigma_err_muRm': [],
    'sigma_err_muRp': [],
    'BR': []
    }

def float_to_str(x, digits=2):
    tmp = ':.{:d}f'.format(digits)
    tmp = ('{' + tmp + '}').format(x)
    return tmp.replace('.', 'p')

for mH in xrange(125, 1010, 10):
    for mA in xrange(30, 1010, 10):
        if mA >= mH:
            mode = 'A'
        else:
            mode = 'H'
        mhc = max(mH, mA)
        m12 = math.sqrt(pow(mhc, 2) * tb / (1 + pow(tb, 2)))
        
        if process =='ggH':
            muR = mH/2
            muF = muR
        elif process == 'bbH':
            muR = (mA + MZ + mb + mb__tilde__ )
            muF =muR
        
        print mode
        x = Calc2HDM(mode = mode, sqrts = sqrts, type = type, tb = tb, m12 = m12, mh = mh, mH = mH, mA = mA, mhc = mhc, sba = sba, outputFile = outputFile, muR = muR, muF = muF)
        x.setpdf('NNPDF31_nnlo_as_0118_nf_4_mc_hessian')
        x.computeBR()
        xsec_ggH, err_integration_ggH, err_muRm_ggH, err_muRp_ggH, xsec_bbH, err_integration_bbH, mb_MSscheme_muR= x.getXsecFromSusHi()
        if mode == 'H':
            #print "xsec, HtoZABR, AtobbBR ", xsec, x.HtoZABR, x.AtobbBR
            sigmaBR = xsec_ggH * x.HtoZABR * x.AtobbBR * ZtollBR 
        else:
            #print "xsec, AtoZHBR, HtobbBR ", xsec, x.AtoZHBR, x.HtobbBR
            sigmaBR = xsec_ggH * x.AtoZHBR * x.HtobbBR * ZtollBR 
        print "# xsec * BR = ", sigmaBR
        results['mH'].append(mH)
        results['mA'].append(mA)
        results['sigma'].append(xsec_ggH)
        results['sigma_errIntegration'].append(err_integration_ggH)
        results['sigma_err_muRm'].append(err_muRm_ggH)
        results['sigma_err_muRp'].append(err_muRp_ggH)
        if mode == 'H':
            results['BR'].append(x.HtoZABR * x.AtobbBR * ZtollBR)
        else:
            results['BR'].append(x.AtoZHBR * x.HtobbBR * ZtollBR)

filename = 'sigmaBR_HZA_type-2_tb-%s_cba-%s_mirroring.json' % (float_to_str(tb, 1), float_to_str(cba, 2))
with open(filename, 'w+') as f:
    json.dump(results, f)
