#!/bin/env python
import os, os.path, sys
import math
import json
import argparse
import numpy as np
from cp3_llbb.Calculators42HDM.Calc2HDM import *



def get_tb_vs_cba_grid(outdir, cmssw, tb, ba, runSushi=True):
    
    results = {
        'tb': [],
        'cba': [],
        'sigma': [],
        'sigma_errIntegration': [],
        'TotBR': []
        }
    
    pwd = os.getcwd() 
    cba = math.cos(ba)
    if ba >= 0 and ba <= math.pi/2:
        sba = math.sin(ba)
    elif ba > math.pi/2 and ba <= math.pi:
        sba = math.sin(ba-math.pi)
    mhc = max(mH, mA)
    m12 = math.sqrt(pow(mhc, 2) * tb / (1 + pow(tb, 2)))
    
    if process =='gg{}'.format(heavy):
        muR = m_heavy/2
        muF = muR
    elif process == 'bb{}'.format(heavy):
        muR = (m_heavy + MZ + mb + mb__tilde__ )
        muF =muR
    
    try:
        stageOutF = os.path.join(cmssw, outdir, 'outputs')
        if not os.path.exists(stageOutF):
            os.makedirs(stageOutF)
    except OSError as err:
        print(err)
    
    File = "out_m{}-{}_m{}-{}_tb-{}_cosba-{}_mode-{}.dat".format(heavy, m_heavy, light, m_light, tb, round(cba, 2), mode)
    outputFile = os.path.join(stageOutF, File)
    x = Calc2HDM(mode = mode, sqrts = sqrts, type = type, tb = tb, m12 = m12, mh = mh, mH = mH, mA = mA, mhc = mhc, sba = sba, outputFile = outputFile, muR = muR, muF = muF)
    x.setpdf('NNPDF31_nnlo_as_0118_nf_4_mc_hessian')
    
    os.chdir(cmssw)
    x.computeBR()
    
    if runSushi:
        cross_sections = calc.getXsecFromSusHi()
                    
        if prod =='gg%s'%heavy:
            xsec = cross_sections['full']['ggh'][0]
            xsec_err = cross_sections['full']['ggh'][1]
                
        elif prod == 'bb%s'%heavy:
            xsec_bbh_lo   = cross_sections['split']['bbh_lo'][0]
            xsec_bbh_nlo  = cross_sections['split']['bbh_lo'][0]
            xsec_bbh_nnlo = cross_sections['split']['bbh_lo'][0]
                        
            err_integration_bbh_lo   =  cross_sections['split']['bbh_lo'][1]
            err_integration_bbh_nlo  =  cross_sections['split']['bbh_nlo'][1]
            err_integration_bbh_nnlo =  cross_sections['split']['bbh_nnlo'][1]
    
            xsec     = xsec_bbh_nlo
            xsec_err = err_integration_bbh_nlo
    
    if mode == 'H':
        TotBR = x.HtoZABR * x.AtobbBR * ZtollBR
    elif mode =='A':
        TotBR = x.AtoZHBR * x.HtobbBR * ZtollBR

    try:
        stageOutJs = os.path.join(cmssw, outdir, 'results')
        if not os.path.exists(stageOutJs):
            os.makedirs(stageOutJs)
    except OSError as err:
        print(err)

    filename  = 'sigmaBR_%sZ%s_type-2_M%s-%s_M%s-%s_tb-%s_cba-%s.json' % (heavy, light, heavy, str(round(m_heavy,2)), light, str(round(m_light,2)), str(round(tb,2)), str(round(cba, 5)))
    
    results['tb'].append(tb)
    results['cba'].append(cba)
    results['sigma'].append(xsec)
    results['sigma_errIntegration'].append(xsec_err)
    results['TotBR'].append(TotBR)
    
    with open(os.path.join(stageOutJs, filename), 'w+') as f:
        json.dump(results, f)
    print('file saved in :::', os.path.join(stageOutJs, filename))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='finner grid', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-o", "--outdir", default='2hdmonslurm', required=True, help="output dir")
    parser.add_argument("-p", "--process", type=str, choices=['ggH', 'ggA', 'bbH', 'bbA'], required=True, 
            help="this will decide the mode and the renormalisation and factorisation scale")
    parser.add_argument("--cmssw", required=True, help="this script need to be run inside cmssw dir")
    parser.add_argument("--tb", type=float, required=True, help="angle tanbeta")
    parser.add_argument("--ba", type=float, required=True, help="angle beta - alpha")
    parser.add_argument('--mH', type=float, default=500., help='mass of the Higgs bosons H')
    parser.add_argument('--mA', type=float, default=300., help='mass of the psuedo-scalar A')

    options = parser.parse_args()

    
    process = options.process
    mH      = options.mH
    mA      = options.mA
    mode    = process[-1]
    # Alex's PhD thesis parameters
    sqrts = 13000
    type  = 2
    mh    = 125

    runSushi=True
    
    if mode == 'H':
        light   = 'A'
        heavy   = 'H'
        m_heavy = mH
        m_light = mA
    elif mode == 'A':
        light   = 'H'
        heavy   = 'A'
        m_heavy = mA
        m_light = mH
    
    ZtollBR =  3.3658 * 2 / 100. # no taus
    mb = 4.92 # mb(OS) pole mass
    mb__tilde__ = 4.92 # mb~
    MZ= 9.118760e+01

    get_tb_vs_cba_grid(outdir=options.outdir, cmssw=options.cmssw, tb=options.tb, ba=options.ba, runSushi=runSushi)
