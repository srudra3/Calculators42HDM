#!/usr/bin/python
import sys
import math
import yaml 

import numpy as np

from cp3_llbb.Calculators42HDM.Calc2HDM import *


mTofix = 997.14

extra  = [] #200., 50., 400., 300., 100., 1000.] # masses that are generated in madgraph
extra += [55.16, 566.51, 160.17, 87.1, 298.97, 186.51, 118.11, 137.54, 40.68, 47.37, 779.83, 350.77, 664.66, 74.8, 34.93, 254.82, 101.43, 217.19, 482.85, 411.54, 64.24, 30.0]

runSushi =True

sqrts= 13000
type = 2
cba  = 0.01
mh   = 125.
mb   = 4.92
mZ   = 9.118760e+01
mb__tilde__ = 4.92

dict_   = {}
dict_['cos(b-a)']= cba
dict_['type']=type
dict_['model']='2HDM'
dict_['HToZA']= {}
dict_['AToZH']= {}


for fix, pave in {"mH": "mA", "mA": "mH"}.items():
    
    masses_to_pave  = extra #+ np.arange(10., 1000., 100.).tolist()
    
    for tb in np.arange(0.05, 50.5, 20.): 
        for mTopave in sorted(list(masses_to_pave)):
            
            if mTopave < mTofix:
                heavy   = fix[-1]
                light   = pave[-1]
                m_heavy = mTofix
                m_light = mTopave
            else:
                heavy   = pave[-1]
                light   = fix[-1]
                m_heavy = mTopave
                m_light = mTofix
            
            decay = '{}ToZ{}'.format(heavy, light)
            mode  = decay[0]
            
            if decay=='AToZH' and m_light < 125.:
                    continue
            if not 'M{}_{}_M{}_{}_tb_{}'.format(heavy, m_heavy, light, m_light, tb) in dict_[decay].keys():
                dict_[decay]['M{}_{}_M{}_{}_tb_{}'.format(heavy, m_heavy, light, m_light, tb)] = {}
                    
            for process in ['bb_associated_production', 'gg_fusion']:
                prod = 'gg%s'%mode if process == 'gg_fusion' else 'bb%s'%mode
                mhc  = max(m_heavy, m_light)
                m12  = math.sqrt(pow(mhc, 2) * tb / (1 + pow(tb, 2)))
                        
                muR4ggh = m_heavy/2
                muF4ggh = muR4ggh
                muR4bbh = (m_light + mZ + mb + mb__tilde__ )
                muF4bbh = muR4bbh
    
                if mode == 'H':
                    mH = m_heavy 
                    mA = m_light
                else:
                    mH = m_light
                    mA = m_heavy
                
                print( m_heavy, m_light, mode, decay, prod)
                beta  = math.atan(tb)
                alpha = math.atan(tb)-math.acos(cba)
                sba   = math.sin(math.atan(tb)-alpha)
                # or simply : sba = math.sqrt(1 - pow(cba, 2))
                
                try:
                    stageOutF = os.path.join('Scan/2hdmclogs', 'mAorH-{}_func_tb'.format(mTofix))
                    if not os.path.exists(stageOutF):
                        os.makedirs(stageOutF)
                except OSError as err:
                    print(err)

                outputFile = os.path.join(stageOutF, "out_mH-{}_mA-{}_tb-{}_mode-{}.dat".format(mH, mA, tb, mode))
                
                calc = Calc2HDM( mode  = mode, 
                                 sqrts = sqrts, 
                                 type  = type, 
                                 tb    = tb, 
                                 m12   = m12, 
                                 mh    = mh, 
                                 mH    = mH, 
                                 mA    = mA, 
                                 mhc   = mhc, 
                                 sba   = sba, 
                                 outputFile = outputFile,
                                 muR4ggh   = muR4ggh, 
                                 muF4ggh   = muF4ggh,
                                 muR4bbh   = muR4bbh, 
                                 muF4bbh   = muF4bbh
                                 )
                
                calc.setpdf('NNPDF31_nnlo_as_0118_nf_4_mc_hessian')
                
                cmssw = os.path.dirname(os.path.abspath(__file__)).split('example')[0]
                os.chdir(cmssw)
                pwd = os.getcwd()
                
                calc.computeBR()  # br is independent of renormalisation / factorisation scales
                    
                if mode =='H':
                    dict_[decay]['M{}_{}_M{}_{}_tb_{}'.format(heavy, m_heavy, light, m_light, tb)]['branching-ratio']={ 
                        'HToZA': calc.HtoZABR, 
                        'ATobb': calc.AtobbBR}
                
                elif mode =='A':
                    dict_[decay]['M{}_{}_M{}_{}_tb_{}'.format(heavy, m_heavy, light, m_light, tb)]['branching-ratio']={ 
                        'AToZH': calc.AtoZHBR, 
                        'HTobb': calc.HtobbBR}
                        
                if runSushi:
                    xsec_ggh = cross_sections['full']['ggh'][0]
                    err_integration_ggh = cross_sections['full']['ggh'][1]
                
                    xsec_bbh_lo   = cross_sections['split']['bbh_lo'][0]
                    xsec_bbh_nlo  = cross_sections['split']['bbh_lo'][0]
                    xsec_bbh_nnlo = cross_sections['split']['bbh_lo'][0]
                            
                    err_integration_bbh_lo   =  cross_sections['split']['bbh_lo'][1]
                    err_integration_bbh_nlo  =  cross_sections['split']['bbh_nlo'][1]
                    err_integration_bbh_nnlo =  cross_sections['split']['bbh_nnlo'][1]
                            
            dict_[decay]['M{}_{}_M{}_{}_tb_{}'.format(heavy, m_heavy, light, m_light, tb)]['cross-section']= { 
                'gg%s'%mode: '{}  +/-  {}  pb'.format(xsec_ggh, err_integration_ggh), 
                'bb%s'%mode: 
                    { 'LO'   : '{}  +/-  {}  pb'.format(xsec_bbh_lo, err_integration_bbh_lo),
                      'NLO'  : '{}  +/-  {}  pb'.format(xsec_bbh_nlo, err_integration_bbh_nlo),
                      'NNLO' : '{}  +/-  {}  pb'.format(xsec_bbh_nnlo, err_integration_bbh_nnlo)
                    }
                } 

print( dict_)

inPath = '/home/ucl/cp3/kjaffel/bamboodev/ZA_FullAnalysis/ZAStatAnalysis'
inFile = os.path.join(inPath, "data/2hdmc1.8.0-br_cba-{}_mAorH-{}_2hdm-type{}__test.yml".format(cba, mTofix, type))
with open(inFile, 'w') as _f:
    yaml.dump(dict_, _f, default_flow_style=False)

print( 'sushi file saved in :', inFile)   
