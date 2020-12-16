#!/usr/bin/python
import os
import math
import datetime
import scipy 
import argparse
from scipy import interpolate
from cp3_llbb.Calculators42HDM.Calc2HDM import *
import CMSStyle
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt 

CMSSW_Calculators42HDM = '/home/ucl/cp3/kjaffel/ZAPrivateProduction/CMSSW_10_2_22/src/cp3_llbb/Calculators42HDM'

def get_options():
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    runtime = 'run_' + current_time
    #if not os.path.exists(runtime):
    #    os.makedirs(runtime)
    parser = argparse.ArgumentParser(description='Create Validation Plots: tanb, xsc, BR, widths ...')
    parser.add_argument('-lazy', '--lazy', action='store_true', required=False, help='This will allow you to do fast test, with few files saved in lazy_defaults/ ')
    parser.add_argument('-mH', '--mH', action='store', type=int, default=800 , help='Fix Heavy bosons mass  [GeV]')
    parser.add_argument('-mA', '--mA', action='store', type=int, default= None , help='Fix Pseudo-scalar bosons mass  [GeV]')
    parser.add_argument('-o', '--output', action='store', type=str, dest='runtime', default=runtime, help='Fix Pseudo-scalar bosons mass  [GeV]')
    options = parser.parse_args()
    return options

def mass_to_string(m):
    r = '{:.2f}'.format(m)
    r = r.replace('.', 'p')
    return r

def Calculators42HDM(list_mA, list_tb, output, proc=None):
    
    sqrts = 13000
    type = 2
    mh = 125
    cba = 0.01
    mH = options.mH 
    
    list_xsc = np.array([])
    list_xsc = np.zeros((len(list_tb),len(list_mA)))
    for j, (vec_tb, vec_mA) in enumerate(zip(list_tb,list_mA )):
        for i in range(len( vec_tb )-1 ):
            tb = vec_tb [i]
            mA = vec_mA [i]
            
            if mA >= mH:
                mode = 'A'
            else:
                mode = 'H'
            mhc = max(mH, mA)
            m12= math.sqrt(pow(mhc, 2) * tb / (1 + pow(tb, 2)))
            
            beta=math.atan(tb)
            alpha=math.atan(tb)-math.acos(cba)
            sba = math.sin(math.atan(tb)-alpha)
            outputFile = 'out_mH-{}_mA-{}_tb-{}.dat'.format(mass_to_string(mH), mass_to_string(mA), mass_to_string(tb))
            
            cwd = os.getcwd()
            os.chdir(CMSSW_Calculators42HDM)
            
            res = Calc2HDM(mode = mode, sqrts = sqrts, type = type, tb = tb, m12 = m12, mh = mh, mH = mH, mA = mA, mhc = mhc, sba = sba, outputFile = outputFile, muR = 1., muF = 1.)
            res.setpdf('NNPDF31_nnlo_as_0118_mc_hessian_pdfas')
            res.settb(tb)
            res.setmA(mA)
            res.setmH(mH)
            res.computeBR()
            
            os.chdir(CMSSW_Calculators42HDM) 
            xsec_ggh, err_integration_ggh, err_muRm_ggh, err_muRp_ggh, xsec_bbh, err_integration_bbh, err_muRm_bbh, err_muRp_bbh = res.getXsecFromSusHi()
            
            xsec_times_BR={}
            if mode =='H':
                xsec_times_BR['gg'] = xsec_ggh*res.HtoZABR*res.AtobbBR
                xsec_times_BR['bb'] = xsec_bbh*res.HtoZABR*res.AtobbBR
            elif mode == 'A':
                xsec_times_BR['gg'] = xsec_ggh*res.AtoZHBR*res.HtobbBR
                xsec_times_BR['bb'] = xsec_bbh*res.AtoZHBR*res.HtobbBR
            
            print( xsec_times_BR , i, j )
            list_xsc[j][i]= xsec_times_BR [proc]
            os.chdir(cwd)
        print (80*'*')
    print ( list_xsc )
    return list_xsc

def main():
    global options
    options = get_options()
    
    runtime = options.runtime
    
    tb = np.arange(1.,11.,1. )
    mA = np.arange(100.,1100.,100. )
    print (len(tb) , len(mA))
    
    MA, TANbeta = np.meshgrid(mA, tb)
    
    if options.lazy: 
        dict_xsc = {'gg': np.load('defaults_xsc/ggxsc_2HDMII_MH-800_tb1to10_cosbeta-alpha0p01_sqrts1300_mh125_m12zero.npy'), 
                    'bb': np.load('defaults_xsc/bbxsc_2HDMII_MH-800_tb1to10_cosbeta-alpha0p01_sqrts1300_mh125_m12zero.npy')
                    }
    else:
        dict_xsc = {'gg': Calculators42HDM(MA, TANbeta, runtime, proc ='gg' ),
                    'bb': Calculators42HDM(MA, TANbeta, runtime, proc ='bb' )
                    }
        if not os.path.exists('defaults_xsc'):
            os.makedirs('defaults_xsc')
        np.save('defaults_xsc/ggxsc_2HDMII_MH-800_tb1to10_cosbeta-alpha0p01_sqrts1300_mh125_m12zero.npy', dict_xsc['gg'])
        np.save('defaults_xsc/bbxsc_2HDMII_MH-800_tb1to10_cosbeta-alpha0p01_sqrts1300_mh125_m12zero.npy', dict_xsc['bb'])
        print("The computed xsc have been saved successfully in defaults_xsc !")
   
    x = np.asarray(mA)
    new_x = np.arange(x.min(), x.max(), 1)
    
    y = np.asarray(tb)
    new_y = np.arange(y.min(), y.max(), 0.1)
    
    for proc, XSC in dict_xsc.items():
        
        z = np.asarray(XSC)
        # interpolation using interp2d
        fun = interpolate.interp2d(x, y, z, kind='cubic')
        new_z = fun(new_x, new_y)
        
        fig= plt.figure(figsize=(8,6))
        ax = fig.add_subplot(111)
        
        CMSStyle.changeFont()
        ax.set_xlim([100.,1000.])
        ax.set_ylim([1.,10.])
        plt.xticks(mA)
        plt.yticks(tb)
        plt.title(r'$2HDM-TypeII: cos(\beta-\alpha) = 0.01, MH= 800GeV, m12= 0, mh = 125 GeV$', fontsize=12)
        plt.xlabel('MA [GeV]', horizontalalignment='right', x=1.0)
        plt.ylabel( r'$tan\beta$', horizontalalignment='right', y=1.0)
    
        #cmap = 'inferno'
        cmap = 'plasma'
        print( "process :", proc )
        print( new_z )       
        print ( "min xsc :", new_z.min(), "pb", "max xsc :", new_z.max(), "pb" )
        print( 80* "**" )
        im = plt.pcolormesh( new_x, new_y, new_z, cmap=cmap, vmin = new_z.min(), vmax = new_z.max())
        ax.grid()

        cbar = plt.colorbar(im)
        cbar.set_label(r'$\sigma* BR(H->ZA)* BR(A->bb) [pb]$')
        
        fig.tight_layout()
        fig.savefig("proc{}_mA_vs_tanbeta.png".format(proc))

    
if __name__ == '__main__':
    main()
