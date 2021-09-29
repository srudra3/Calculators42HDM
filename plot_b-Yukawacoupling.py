#!/usr/bin/python
import math
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
import argparse
import glob
import os.path, os
from cp3_llbb.Calculators42HDM.Calc2HDM import *
from cp3_llbb.Calculators42HDM.labellines import *

def mass_to_string(x, digits=2):
    tmp = ':.{:d}f'.format(digits)
    tmp = ('{' + tmp + '}').format(x)
    return tmp.replace('.', 'p')

def Block_YUKAWA_ver2(tanbeta=None, sinbma=None, g_b=None):
    # https://arxiv.org/pdf/hep-ph/0611353.pdf
    #muR= MH
    #muF= MH/4.
    
    MB = 4.75 # mb pole mass
    aEWM1= 127.9
    aEW = 1./aEWM1
    Gf = 1.166390e-05
    MZ= 9.118760e+01
    MW= math.sqrt(MZ**2/2. + math.sqrt(MZ**4/4. - (aEW*math.pi*MZ**2)/(Gf*math.sqrt(2))))
    ee = 2*math.sqrt(aEW)*math.sqrt(math.pi)
    sw2 = 1 - MW**2/MZ**2
    sw = math.sqrt(sw2)
    vev = (2*MW*sw)/ee

    mb_OS = MB
    #g_b = (1.+ C* delta_b)/(1. + delta_b)
    ymb_A = mb_OS*g_b 
    gf_A = tanbeta 
    yb_A = ((ymb_A*math.sqrt(2))/vev)

    return yb_A

def Block_YUKAWA(mh1=None, mh2=None, mh3=None, tanbeta=None, sinbma=None, wh2tobb=None, wh3tobb=None):
    
    MB = 4.75 # mb pole mass
    aEWM1= 127.9
    aEW = 1./aEWM1
    Gf = 1.166390e-05
    MZ= 9.118760e+01
    MW= math.sqrt(MZ**2/2. + math.sqrt(MZ**4/4. - (aEW*math.pi*MZ**2)/(Gf*math.sqrt(2))))
    ee = 2*math.sqrt(aEW)*math.sqrt(math.pi)
    sw2 = 1 - MW**2/MZ**2
    sw = math.sqrt(sw2)
    vev = (2*MW*sw)/ee
    TH1x1 = sinbma
    TH1x2 = math.sqrt(1 - sinbma**2)
    TH2x1 = -math.sqrt(1 - sinbma**2)
    TH2x2 = sinbma
    TH3x3 = 1.
    
    #PartialDecay(h2 > bb~ ) = ((-12*MB**2*TH1x2**2*yb**2 + 3*mh2**2*TH1x2**2*yb**2 - (24*MB**2*tanbeta**2*TH2x2**2*ymb**2)/vev**2 + (6*mh2**2*tanbeta**2*TH2x2**2*ymb**2)/vev**2 - (24*MB**2*tanbeta*TH1x2*TH2x2*yb*ymb*math.sqrt(2))/vev + (6*mh2**2*tanbeta*TH1x2*TH2x2*yb*ymb*math.sqrt(2))/vev)*math.sqrt(-4*MB**2*mh2**2 + mh2**4))/(16.*math.pi*abs(mh2)**3)
    #PartialDecay(h2 > bb~ ) = (ymb**2*(const1_H - const2_H + const3_H - const4_H + const5_H )*const6_H )/const7_H
    
    #ymb2_X_const1_H = -12*MB**2*TH1x2**2*yb**2 + 3*mh2**2*TH1x2**2*yb**2 = yb**2 *(-12*MB**2*TH1x2**2*yb**2 + 3*mh2**2*TH1x2**2)
    #                                                                     = ((2*ymb**2)/(vev**2)) * (-12*MB**2*TH1x2**2 + 3*mh2**2*TH1x2**2)
    #                                                                     = ymb**2 *(2*(-12*MB**2*TH1x2**2 + 3*mh2**2*TH1x2**2)/(vev**2))
    const1_H = (2*(-12*MB**2*TH1x2**2 + 3*mh2**2*TH1x2**2)/(vev**2))
    #ymb2_X_const2_H = (24*MB**2*tanbeta**2*TH2x2**2*ymb**2)/vev**2       = ymb**2 *((24*MB**2*tanbeta**2*TH2x2**2)/vev**2)
    const2_H = ((24*MB**2*tanbeta**2*TH2x2**2)/vev**2)
    #ymb2_X_const3_H = (6*mh2**2*tanbeta**2*TH2x2**2*ymb**2)/vev**2       = ymb**2 *((6*mh2**2*tanbeta**2*TH2x2**2)/vev**2)
    const3_H = ((6*mh2**2*tanbeta**2*TH2x2**2)/vev**2)
    #ymb2_X_const4_H = (24*MB**2*tanbeta*TH1x2*TH2x2*yb*ymb*math.sqrt(2))/vev  = yb*ymb * ((24*MB**2*tanbeta*TH1x2*TH2x2*math.sqrt(2))/vev )
    #                                                                          = ((ymb*math.sqrt(2))/vev)*ymb * ((24*MB**2*tanbeta*TH1x2*TH2x2*math.sqrt(2))/vev )
    #                                                                          = ymb**2 *(((math.sqrt(2))/vev )*((24*MB**2*tanbeta*TH1x2*TH2x2*math.sqrt(2))/vev))
    const4_H = (((math.sqrt(2))/vev )*((24*MB**2*tanbeta*TH1x2*TH2x2*math.sqrt(2))/vev))
    #ymb2_X_const5_H = (6*mh2**2*tanbeta*TH1x2*TH2x2*yb*ymb*math.sqrt(2))/vev  = yb*ymb * ((6*mh2**2*tanbeta*TH1x2*TH2x2*math.sqrt(2))/vev )
    #                                                                          = ((ymb*math.sqrt(2))/vev)*ymb * ( (6*mh2**2*tanbeta*TH1x2*TH2x2*math.sqrt(2))/vev )
    #                                                                          = ymb**2 * ((math.sqrt(2))/vev ) * ( (6*mh2**2*tanbeta*TH1x2*TH2x2*math.sqrt(2))/vev )
    const5_H = (((math.sqrt(2))/vev)*((6*mh2**2*tanbeta*TH1x2*TH2x2*math.sqrt(2))/vev ))
    const6_H = math.sqrt(-4*MB**2*mh2**2 + mh2**4)
    const7_H = (16.*math.pi*abs(mh2)**3)
    
    ymb_H= math.sqrt(((const7_H * wh2tobb ) /(const6_H *(const1_H - const2_H + const3_H - const4_H + const5_H))))
    yb_H = ((ymb_H*math.sqrt(2))/vev)
    
    # PartialDecay(h3 > bb~ ) = (3*mh3**2*tanbeta**2*TH3x3**2*ymb**2*math.sqrt(-4*MB**2*mh3**2 + mh3**4))/(8.*math.pi*vev**2*abs(mh3)**3)
    const1_A = (3*mh3**2*tanbeta**2*TH3x3**2*math.sqrt(-4*MB**2*mh3**2 + mh3**4))
    const2_A = (8.*math.pi*vev**2*abs(mh3)**3)
    ymb_A = math.sqrt((const2_A * wh3tobb)/const1_A)
    yb_A = ((ymb_A*math.sqrt(2))/vev)
    
    #wh1tobb=((-12*MB**2*TH1x1**2*yb**2 + 3*mh1**2*TH1x1**2*yb**2 - (24*MB**2*tanbeta**2*TH2x1**2*ymb**2)/vev**2 + (6*mh1**2*tanbeta**2*TH2x1**2*ymb**2)/vev**2 - (24*MB**2*tanbeta*TH1x1*TH2x1*yb*ymb*math.sqrt(2))/vev + (6*mh1**2*tanbeta*TH1x1*TH2x1*yb*ymb*math.sqrt(2))/vev)*math.sqrt(-4*MB**2*mh1**2 + mh1**4))/(16.*math.pi*abs(mh1)**3)
    
    return yb_H, ymb_H, yb_A, ymb_A#, wh1tobb

def plot2HDM_bottomYukawa_coupling(masstoscan=None, tanbeta=None, fullresummation=False):
    fig= plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111)
    Colors=['forestgreen', 'pink', 'crimson', 'indigo', 'limegreen', 'blueviolet', 'plum', 'magenta','purple', 'hotpink', 'mediumseagreen', 'springgreen', 'aquamarine', 'turquoise', 'aqua', 'mediumslateblue', 'orchid', 'deeppink', 'darkturquoise', 'teal', 'mediumslateblue']
    
    for idx, tb in enumerate(tanbeta):    
        masses = []
        yb_Acouplings = []
        yb_Hcouplings = []
        ymb_Acouplings = []
        ymb_Hcouplings = []
        
        yb_Acouplings_ver2 = []
        Partialwidth_h1tobb = []
        m = 125.
        while m < 1500.:
            type = 2
            sqrts = 13000
            
            muR = 9.118800e+01
            muF = 9.118800e+01

            cba = 0.01  #  cos( beta -alpha) " should not be changed: that's the alignement limit 
            alpha=math.atan(tb)-math.acos(cba)
            sinbma = math.sin(math.atan(tb)-alpha) # OR sinbma = math.sqrt(1 - pow(cba, 2))
            beta = math.atan(tb)
            
            mZ= 9.118760e+01
            mH= (m if masstoscan=='h2' else (m+mZ))
            mA= (m if masstoscan=='h3' else (m-mZ))
            mh=125.
            if mA > mH:
                mode='A'
            elif mH >= mA and mH> 125.:
                mode='H'
            elif mH >= mA and mH <= 125.:
                mode='h'
            mhc = max(mH, mA)
            m12 = math.sqrt(pow(mhc, 2) * tb / (1 + pow(tb, 2)))
            
            outputFile = 'out.dat'
            
            res = Calc2HDM(mode = mode, sqrts = sqrts, type = type,
                           tb = tb, m12 = m12, mh = mh, mH = mH, mA = mA, mhc = mhc, sba = sinbma,
                           outputFile = outputFile, muR = muR, muF = muF)
            res.setpdf('NNPDF31_nnlo_as_0118_nf_4_mc_hessian')
            res.computeBR()
            
            #xsec_ggH, err_integration_ggH, err_muRm_ggH, err_muRp_ggH, xsec_bbH, err_integration_bbH =  res.getXsecFromSusHi()
            with open ('./Scan/NNPDF31_nnlo_as_0118_nf_4_mc_hessian/{}_{}_{}_{}_{}_{}.out'.format(str(mH).replace('.', 'p'), str(mA).replace('.', 'p'), mass_to_string(muR,digits=3), mass_to_string(muF, digits=3), mass_to_string(tb, digits=1), '0p999'), 'r') as sushi_outFile:
                for line in sushi_outFile:
                    if '# g_b' in line:
                        g_b = float(line.split()[1])

            wh3tobb = res.wh3tobb
            wh2tobb = res.wh2tobb
            
            yb_H, ymb_H, yb_A, ymb_A = Block_YUKAWA(mh1=mh, mh2=mH, mh3=mA, tanbeta=tb, sinbma=sinbma, wh2tobb=wh2tobb, wh3tobb=wh3tobb)
            yb_A_ver2  = Block_YUKAWA_ver2(tanbeta=tb, sinbma=sinbma, g_b=g_b)
            
            print( (math.cos(alpha)/math.cos(beta)), tb, tb/(math.cos(alpha)/math.cos(beta)), 'okaaaaaaaaa')
            yb_Hcouplings.append(yb_H*(math.cos(alpha)/math.cos(beta)))
            yb_Acouplings.append(yb_A*tb)
            
            ymb_Hcouplings.append(ymb_H)
            ymb_Acouplings.append(ymb_A)
            
            #yb_Acouplings_ver2.append(yb_A_ver2)
            #Partialwidth_h1tobb.append(wh1tobb)
            
            masses.append(m)
            m += 50.
    
        print( yb_Acouplings , ymb_Acouplings)
        print( yb_Hcouplings , ymb_Hcouplings)
        print( masses )
        if fullresummation:
            plt.plot(masses,ymb_Acouplings, color=Colors[idx], linewidth=3.5, marker='o', label=r'$m^{Y, A}_{b}: tan\beta = %s$'%tb)
            plt.plot(masses,ymb_Hcouplings, color=Colors[idx+2], linewidth=2., marker='s', label=r'$m^{Y, H}_{b}: tan\beta = %s$'%tb)
        else:
            plt.plot(masses,yb_Acouplings, color=Colors[idx], linewidth=3.5, marker='o', label=r'$Y^{A}_{b}: tan\beta = %s$'%tb)
            plt.plot(masses,yb_Hcouplings, color=Colors[idx+2], linewidth=2., marker='s', label=r'$Y^{H}_{b}: tan\beta = %s$'%tb)

        #plt.plot(masses,yb_Acouplings_ver2, color=Colors[idx+5], marker='<', label=r'$Y^{A}_{b} ver2: tan\beta = %s$'%tb)
        #ax.axhspan((4.088E-03- 0.73*4.088E-03/100.) , (4.088E-03+ 0.73*4.088E-03/100.), color=Colors[idx+4], label='r$\Gamma(h_{SM}=125'))
        #plt.plot(masses,Partialwidth_h1tobb, color=Colors[idx], marker='o', label=r'$\Gamma(h_{SM}=125 \rightarrow bb), tan\beta = {}$'.format(tb))
    
    ylabel =  ('m^{ Y,\phi}_{b}'if fullresummation else('Y^{\phi}_{b} =  \sqrt{2}  m^{ Y,\phi}_{b}g^{ \phi }_{f}/vev' ))
    plt.ylabel(r'Bottom-Yukawa  coupling $%s$'%ylabel, fontsize=12.)
    plt.xlabel(r'$M_{} [GeV]$'.format('A' if masstoscan=='h3' else 'H'), fontsize=12.)
    #plt.yscale('log')
    plt.title(r'$2HDM-typeII: M_{H^\pm}=M_{H}, M_{H}=M_{A}+M_{Z}, cos(\beta-\alpha)= 0.01, mh= 125. GeV $', fontsize=10.)
    plt.xlim(min(masses), max(masses))
    plt.legend()
    fig.savefig('PLOTS/bottomyukawa_coupling_{}_func_{}mass.png'.format(('ymb' if fullresummation else('yb')), masstoscan))
    plt.gcf().clear()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot bottom Yukawa coupling as function of h3 and h2 masses')
    parser.add_argument('-s', '--scan', action='store', default='h3', choices=['h2','h3'], help='mass to scan ?')
    parser.add_argument('--fullresummation', action='store_true', default=False, help=' PLease read page10 of this paper so that you undrestand what I mean :) : https://sushi.hepforge.org/manual/SusHi150.pdf !! ')
    options = parser.parse_args()

    plot2HDM_bottomYukawa_coupling(masstoscan=options.scan, tanbeta=[1.5, 20.0], fullresummation=options.fullresummation)
