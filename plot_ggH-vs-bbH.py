#!/usr/bin/python
import math
from cp3_llbb.Calculators42HDM.Calc2HDM import *
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
import argparse

def get_options():
    parser = argparse.ArgumentParser(description='Compare gg fusion and b-associated production xsc as function of tan beta ')
    parser.add_argument('-lazy', '--lazy', action='store_true', required=False, help='This will allow you to do fast test, with few files saved in data/ ')
    options = parser.parse_args()
    return options

def which_points(grid):
    grid['fullsim'] = [
        #( MH, MA )
        #( 800, 140),
        #( 500, 300),
        ( 240, 130)

     #   ( 200, 50), ( 200, 100),
     #   ( 250, 50), ( 250, 100),
     #   ( 300, 50), ( 300, 100),
     #   ( 300, 200),
     #   ( 500, 50), 
     #   ( 500, 100), ( 500, 200), 
     #   ( 500, 300), ( 500, 400),
     #   ( 650, 50),
     #   ( 800, 50), ( 800, 100), 
     #   ( 800, 200),              
     #   ( 800, 400),              
     #   ( 800, 700),
     #   (1000, 50),              (1000, 200),                           (1000, 500),
        ]
    return grid 


grid = {}
grid = which_points(grid)
ToPlotsggfusion= {}
ToPlotsbbproduction ={}

fig= plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)

masspoint = 0
options = get_options()
def ggH_VS_bbH( ):
    with open('inflexionPoints.txt', 'w+') as outf:
        outf.write("Values of tb where xsc[ggfusion] < xsc[b-associated prouction]\n")
        for H, A in (grid['fullsim']):
            outf.write('MH-{}_MA-{}\n'.format(H, A))
            mH = H
            mA = A
            mhc = max(mH, mA)
    
            sqrts = 13000
            type = 2
            tb = 0.5
            mh = 125.
            mZ = 91.1876
            cba = 0.01
            mode = 'H'
            outputFile = "out.dat"
            
            tb_list = [] 
            xsec_ggH_list = []
            xsec_bbH_list = []
            subprocess_gg_nlo_list = []
            subprocess_qg_nlo_list = []
            subprocess_qq_nlo_list = []
            
            HtoZABR_list = []
            AtobbBR_list = [] 
            
            while tb < 20.5:
                m12 = math.sqrt(pow(mhc, 2) * tb / (1 + pow(tb, 2)))
                tb_list.append(tb)
            
                beta=math.atan(tb)
                alpha=math.atan(tb)-math.acos(cba)
                sba = math.sin(math.atan(tb)-alpha)
                
                test = Calc2HDM(mode = 'H', sqrts = sqrts, type = type, tb = tb, m12 = m12, mh = mh, mH = mH, mA = mA, mhc = mhc, sba = sba, outputFile = outputFile)
                
                test.setm12(m12)
                test.settb(tb)
                test.setsba(sba)
                test.setmA(mA)
                test.setmH(mH)
                test.computeBR()
            
                xsec_ggH, err_integration_ggH, err_muRm_ggH, err_muRp_ggH, xsec_bbH, err_integration_bbH, mb_MSscheme_muR =  test.getXsecFromSusHi()
        
                xsec_ggH_X_BR = xsec_ggH*test.HtoZABR*test.AtobbBR
                xsec_bbH_X_BR = xsec_bbH*test.HtoZABR*test.AtobbBR
                
                if xsec_ggH_X_BR < xsec_bbH_X_BR :
                    outf.write("    tb : {}\n".format(tb ))
                    outf.write("    BR(A-> bb ): {}\n".format(test.AtobbBR))
                    outf.write("    BR(H-> ZA ): {}\n".format(test.HtoZABR))
                    outf.write("    cross-section ggH: {} pb\n".format(xsec_ggH))
                    outf.write("    cross-section bbH: {} pb\n".format(xsec_bbH))
                    outf.write("\n")
    
                xsec_bbH_list.append(xsec_bbH_X_BR)
                xsec_ggH_list.append(xsec_ggH_X_BR)
                
                HtoZABR_list.append(test.HtoZABR)
                AtobbBR_list.append(test.AtobbBR)
                
                tb+=0.5
        
            ToPlotsggfusion["MH-%s_MA-%s"%(H, A)] = xsec_ggH_list 
            ToPlotsbbproduction["MH-%s_MA-%s"%(H, A)]= xsec_bbH_list
    np.save('data/ggHxsc_X_BR_21signal_2hdm2_func-tb.npy', ToPlotsggfusion)
    np.save('data/bbHxsc_X_BR_21signal_2hdm2_func-tb.npy', ToPlotsbbproduction)
    return ToPlotsggfusion, ToPlotsbbproduction, tb_list

if options.lazy:
    ToPlotsggfusion= np.load( 'data/ggHxsc_X_BR_21signal_2hdm2_func-tb.npy', allow_pickle=True)
    ToPlotsbbproduction = np.load( 'data/bbHxsc_X_BR_21signal_2hdm2_func-tb.npy', allow_pickle=True)
else:
    ggH_VS_bbH()

type = 2
tb = 10. 
tb_list = []
while tb < 21.:
    tb+=10.
    tb_list.append(tb)

print( ToPlotsggfusion , ToPlotsbbproduction )
Colors=['forestgreen', 'pink', 'crimson', 'magenta', 'indigo', 'limegreen', 'blueviolet', 'plum', 'purple', 'hotpink', 'mediumseagreen', 'springgreen', 'aquamarine', 'turquoise', 'aqua', 'mediumslateblue', 'orchid', 'deeppink', 'darkturquoise', 'teal', 'mediumslateblue']
idx =0
for (k, val),(k2, val2 ) in zip(ToPlotsggfusion.item().items(), ToPlotsbbproduction.item().items()):
    plt.plot(tb_list,val, color=Colors[idx], marker='o', label= '%s'%k)
    plt.plot(tb_list,val2, color=Colors[idx], marker='+')
    idx+=1
    
plt.ylabel(r'$\sigma* BR(H\rightarrow ZA)* BR(A\rightarrow bb)[pb]$')
plt.xlabel(r'$tan\beta$')
plt.yscale('log')
plt.xscale('log')
plt.title(r'$2HDM-type%s: M_{H^\pm}=M_{H}, cos(\beta-\alpha)= 0.01, mh= 125. GeV $'%('I'if type==1 else('II')), fontsize=10.)
plt.xlim(min(tb_list), max(tb_list))
plt.legend()
#plt.grid()
fig.savefig('2hdm-type%s_func-tb_all21Signalpoints.png'%(type))
plt.gcf().clear()
