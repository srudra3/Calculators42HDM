#!/bin/env python

import math
from cp3_llbb.Calculators42HDM.Calc2HDM import *
import numpy as np
import json
import math

# Alex's PhD thesis parameters
mode = 'H'
sqrts = 13000
type = 2
mh = 125
MH = 500 
MA = 200
outputFile = "out_tb_cba.dat"
ZtollBR =  3.3658 * 2 / 100. # no taus

results = {
    'tb': [],
    'cba': [],
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

#for tb in xrange(0, 50, 1):
#    for cba in xrange(-1, 1, 5):
for tb in np.arange(0.01, 10, 0.05):
    for cba in np.arange(-0.99, 0.99, 0.02):
        ta = math.tan(math.atan(tb) - math.acos(cba))
        if ta < 0:
            continue
        sba = math.sqrt(1 - pow(cba, 2))
        mhc = max(MH, MA)
        m12 = math.sqrt(pow(mhc, 2) * tb / (1 + pow(tb, 2)))
        x = Calc2HDM(mode = 'H', sqrts = sqrts, type = type, tb = tb, m12 = m12, mh = mh, mH = MH, mA = MA, mhc = mhc, sba = sba, outputFile = outputFile, muR = 1., muF = 1.)
        x.setpdf('NNPDF30_lo_as_0130_nf_4')
        x.computeBR()
        xsec, err_integration, err_muRm, err_muRp = x.getXsecFromSusHi()
        print "xsec, HtoZABR, AtobbBR ", xsec, x.HtoZABR, x.AtobbBR
        sigmaBR = xsec * x.HtoZABR * x.AtobbBR * ZtollBR 
        print "# xsec * BR = ", sigmaBR
        results['tb'].append(tb)
        results['cba'].append(cba)
        results['sigma'].append(xsec)
        results['sigma_errIntegration'].append(err_integration)
        results['sigma_err_muRm'].append(err_muRm)
        results['sigma_err_muRp'].append(err_muRp)
        results['BR'].append(x.HtoZABR * x.AtobbBR * ZtollBR)

filename = 'sigmaBR_HZA_type-2_MH-%s_MA-%s.json' % (float_to_str(MH, 1), float_to_str(MA, 2))
with open(filename, 'w+') as f:
    json.dump(results, f)
