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

def BottomYukawacoupling_widthPrecision():
    # https://arxiv.org/pdf/hep-ph/0611353.pdf
    muR= MH
    muF= MH/4.









    return ymb
def BottomYukawacoupling(mh1=None, mh2=None, mh3=None, tanbeta=None, sinbma=None, wh2tobb=None, wh3tobb=None):
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

    return ymb_H, ymb_A #, wh1tobb

def plot2HDM_bottomYukawa_coupling(masstoscan=None, tanbeta=None):
    fig= plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111)
    Colors=['forestgreen', 'pink', 'crimson', 'indigo', 'limegreen', 'blueviolet', 'plum', 'magenta','purple', 'hotpink', 'mediumseagreen', 'springgreen', 'aquamarine', 'turquoise', 'aqua', 'mediumslateblue', 'orchid', 'deeppink', 'darkturquoise', 'teal', 'mediumslateblue']
    
    for idx, tb in enumerate(tanbeta):    
        masses = []
        ymb_Acouplings = []
        ymb_Hcouplings = []
        Partialwidth_h1tobb = []
        m = 125.
        while m < 1500.:
            sqrts = 13000
            type = 2
            mZ= 9.118760e+01
            cba = 0.01  #  cos( beta -alpha) " should not be changed: that's the alignement limit 
            alpha=math.atan(tb)-math.acos(cba)
            sinbma = math.sin(math.atan(tb)-alpha)
            #sinbma = math.sqrt(1 - pow(cba, 2))
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
                                                            outputFile = outputFile, muR = 9.118800e+01, muF = 9.118800e+01)
            res.setpdf('NNPDF31_nnlo_as_0118_nf_4_mc_hessian')
            res.computeBR()
            wh3tobb = res.wh3tobb
            wh2tobb = res.wh2tobb
            print( wh3tobb , wh2tobb )
            ymb_H, ymb_A = BottomYukawacoupling(mh1=mh, mh2=mH, mh3=mA, tanbeta=tb, sinbma=sinbma, wh2tobb=wh2tobb, wh3tobb=wh3tobb)
            ymb_Hcouplings.append(ymb_H)
            ymb_Acouplings.append(ymb_A)
            #Partialwidth_h1tobb.append(wh1tobb)
            masses.append(m)
            m += 50.
    
        print( ymb_Acouplings )
        print( masses )
        plt.plot(masses,ymb_Acouplings, color=Colors[idx], marker='o', label=r'$Y^{A}_{b}: tan\beta = %s$'%tb)
        plt.plot(masses,ymb_Hcouplings, color=Colors[idx+2], marker='s', label=r'$Y^{H}_{b}: tan\beta = %s$'%tb)
        # 4.088E-03     +0.73   -0.73   +0.99   -0.98   +0.61   -0.63 
        #ax.axhspan((4.088E-03- 0.73*4.088E-03/100.) , (4.088E-03+ 0.73*4.088E-03/100.), color=Colors[idx+4], label='r$\Gamma(h_{SM}=125'))
        #plt.plot(masses,Partialwidth_h1tobb, color=Colors[idx], marker='o', label=r'$\Gamma(h_{SM}=125 \rightarrow bb), tan\beta = {}$'.format(tb))
    #labelLines(plt.gca().get_lines(),align=True,fontsize=10)
    plt.ylabel(r'Bottom-Yukawa  coupling $Y_{mb} [GeV] $', fontsize=12.)
    plt.xlabel(r'$M_{} [GeV]$'.format('A' if masstoscan=='h3' else 'H'), fontsize=12.)
    #plt.yscale('log')
    plt.title(r'$2HDM-typeII: M_{H^\pm}=M_{H}, M_{H}=M_{A}+M_{Z}, cos(\beta-\alpha)= 0.01, mh= 125. GeV $', fontsize=10.)
    plt.xlim(min(masses), max(masses))
    #plt.xlim(min(ymb_couplings), max(ymb_couplings))
    #plt.ylim(0e+00, 4.75e+00)
    plt.legend()
    #plt.grid()
    fig.savefig('PLOTS/bottomyukawa_coupling_func_{}mass.png'.format(masstoscan))
    plt.gcf().clear()
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Plot bottom Yukawa coupling as function of h3 and h2 masses')
    parser.add_argument('-s', '--scan', action='store', choices=['h2','h3'], help='mass to scan ?')
    options = parser.parse_args()

    plot2HDM_bottomYukawa_coupling(masstoscan=options.scan, tanbeta=[1.5, 20.])
