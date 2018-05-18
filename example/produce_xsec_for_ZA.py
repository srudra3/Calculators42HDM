#!/bin/env python

import math
from cp3_llbb.Calculators42HDM.Calc2HDM import *
import json

# Alex's PhD thesis parameters
mode = 'H'
sqrts = 13000
type = 2
mh = 125
tb = 0.5
cba = 0.01
sba = math.sqrt(1 - pow(cba, 2))
outputFile = "out.dat"
ZtollBR =  3.3658 * 2 / 100. # no taus

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

for mH10 in xrange(1250, 10100, 50):
    mH = mH10 / 10.
    for mA10 in xrange(300, 10100, 100):
        mA = mA10 / 10.
        if mA >= mH:
            continue
        mhc = max(mH, mA)
        m12 = math.sqrt(pow(mhc, 2) * tb / (1 + pow(tb, 2)))
        x = Calc2HDM(mode = 'H', sqrts = sqrts, type = type, tb = tb, m12 = m12, mh = mh, mH = mH, mA = mA, mhc = mhc, sba = sba, outputFile = outputFile, muR = 1., muF = 1.)
        x.setpdf('NNPDF30_lo_as_0130_nf_4')
        x.computeBR()
        xsec, err_integration, err_muRm, err_muRp = x.getXsecFromSusHi()
   #     print "xsec, HtoZABR, AtobbBR ", xsec, x.HtoZABR, x.AtobbBR
        sigmaBR = xsec * x.HtoZABR * x.AtobbBR * ZtollBR 
        print "# xsec * BR = ", sigmaBR
        results['mH'].append(mH)
        results['mA'].append(mA)
        results['sigma'].append(xsec)
        results['sigma_errIntegration'].append(err_integration)
        results['sigma_err_muRm'].append(err_muRm)
        results['sigma_err_muRp'].append(err_muRp)
        results['BR'].append(x.HtoZABR * x.AtobbBR * ZtollBR)

filename = 'sigmaBR_HZA_type-2_tb-%s_cba-%s.json' % (float_to_str(tb, 1), float_to_str(cba, 2))
with open(filename, 'w+') as f:
    json.dump(results, f)
