#!/usr/bin/python
import os
import json
import math
import datetime
import scipy 
from scipy import interpolate
from scipy.interpolate import griddata
from cp3_llbb.Calculators42HDM.Calc2HDM import *
import CMSStyle
from cp3_llbb.Calculators42HDM.labellines import *
import numpy as np
import shutil
import collections
params = {
    #'text.latex.preamble': ['\\usepackage{gensymb}'],
    'image.origin': 'lower',
    'image.interpolation': 'nearest',
    'image.cmap': 'gist_rainbow',
    'axes.grid': True,
    'savefig.dpi': 300,  # to adjust notebook inline plot size
    'axes.labelsize': 14, # fontsize for x and y labels (was 10)
    'axes.titlesize': 14,
    'font.size': 14, # was 10
    'legend.fontsize': 14, # was 10
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'text.usetex': True,
    'figure.figsize': [23, 15],
    'font.family': 'serif',
    }
import matplotlib
#matplotlib.rcParams.update(params)
import matplotlib.pyplot as plt 
import matplotlib.mlab as mlab

LOG_LEVEL = logging.DEBUG
LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
import colorlog
import logging
logging.root.setLevel(LOG_LEVEL)
formatter = colorlog.ColoredFormatter(LOGFORMAT)
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
logger = logging.getLogger("Calculators42HDM")
logger.setLevel(LOG_LEVEL)
logger.addHandler(stream)

CMSSW_Calculators42HDM = '/home/ucl/cp3/kjaffel/ZAPrivateProduction/CMSSW_10_2_22/src/cp3_llbb/Calculators42HDM'

import argparse
def get_options():
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    runtime = 'run_' + current_time
    parser = argparse.ArgumentParser(description='Create Validation Plots: tanb, xsc, BR, widths ...')
    parser.add_argument('-lazy', '--lazy', action='store_true', required=False, help='This will allow you to do fast test, with few files saved in lazy_defaults/ ')
    parser.add_argument('-d', '--debug', action='store_true', required=False, help='will not ovwerite out.dat and out.log but instead you will get in format out_mH-{}_mA-{}_tb-{}_cba-{}.dat')
    parser.add_argument('-scale', '--scale', action='store_true', required=False, help='scale xsc *BR ')
    parser.add_argument('-s', '--scan', action='store', type=str, dest='scan', default='mA', choices=['mA', 'mH'], help='Parameter to be sacned being scanned')
    parser.add_argument('-o', '--output', action='store', type=str, dest='output', default=runtime, help='Output directory')
    options = parser.parse_args()
    #if not os.path.exists(options.output):
    #	os.makedirs(options.output)
    return options

def mass_to_string(m):
    r = '{:.2f}'.format(m)
    r = r.replace('.', 'p')
    return r

def float_to_str(x, digits=2):
    tmp = ':.{:d}f'.format(digits)
    tmp = ('{' + tmp + '}').format(x)
    return tmp.replace('.', 'p')

def Calculators42HDM(list_masses, list_tb, return_scaledXSC= False, return_totalwidth = False):
    sqrts = 13000 #center-of-mass energy in GeV
    type = 2
    mh = 125.
    mZ = 91.1876
    cba = 0.01
    
    widths = {}
    xsec_times_BR={}
    xsec={}
    for tb in list_tb:
        results1 = {
            'Hwidth':[],
            'H+width':[],
            'hwidth':[],
            'Awidth':[],
            'mH':[],
            'mA':[]
            }
        results2= {
            'gg-fusion':[],
            'bb-associated_production':[],
            'mH':[],
            'mA':[]
            }
        results3 = {
            'gg-fusion':[],
            'bb-associated_production':[],
            'mH':[],
            'mA':[]
            }

        for m in list_masses:
            if options.scan =="mA":
                mA = m
                mH = mZ + mA
            else:
                mH= m
                mA = mH - mZ
            
            results1['mA'].append(mA)
            results1['mH'].append(mH)
            results2['mA'].append(mA)
            results2['mH'].append(mH)
            results3['mA'].append(mA)
            results3['mH'].append(mH)
             
            if mA > mH:
                logger.info("MA_{} >= MH_{} switching to A->ZH mode!".format(mA, mH))
                mode = 'A'
            elif mH >= mA and mH> 125.:
                logger.info("MA_{} =< MH_{} switching to H->ZA mode!".format(mA, mH))
                mode = 'H'
            elif mH >= mA and mH <= 125.:
                mode ='h'
                logger.info('mode h')
            
            mhc = max(mH, mA)
            m12= math.sqrt(pow(mhc, 2) * tb / (1 + pow(tb, 2)))
            if (pow(mhc, 2) * tb / (1 + pow(tb, 2))) < 0:
                logger.warning( 'm12 is negative ! ' ) 
            sba = math.sqrt(1 - pow(cba, 2))
            if options.debug:
                outputFile = 'out_mH-{}_mA-{}_tb-{}.dat'.format(mass_to_string(mH), mass_to_string(mA), mass_to_string(tb))
            else:
                outputFile='out.dat'

            cwd = os.getcwd()
            os.chdir(CMSSW_Calculators42HDM)
            
            res = Calc2HDM(mode = mode, sqrts = sqrts, type = type, tb = tb, m12 = m12, mh = mh, mH = mH, mA = mA, mhc = mhc, sba = sba, outputFile = outputFile, muR = 1., muF = 1.)
            res.setpdf('NNPDF31_nnlo_as_0118_mc_hessian_pdfas')
            res.settb(tb)
            res.setmA(mA)
            res.setmH(mH)
            res.computeBR()
            
            results1['Hwidth'].append( res.Hwidth)
            results1['H+width'].append( res.chargedHwidth)
            results1['hwidth'].append( res.hwidth)
            results1['Awidth'].append( res.Awidth)

            os.chdir(CMSSW_Calculators42HDM) 
            xsec_ggh, err_integration_ggh, err_muRm_ggh, err_muRp_ggh, xsec_bbh, err_integration_bbh= res.getXsecFromSusHi()
            
            if mode =='H': # H->ZA
            	BR = res.HtoZABR* res.AtobbBR
            elif mode == 'A': # A->ZH
                BR = res.AtoZHBR* res.HtobbBR
            elif mode == 'h': # A->Zh
                BR = res.AtoZhBR* res.htobbBR
            
            results2['gg-fusion'].append(xsec_ggh*BR)
            results2['bb-associated_production'].append(xsec_bbh*BR)
            
            results3['gg-fusion'].append(xsec_ggh)
            results3['bb-associated_production'].append(xsec_bbh)

        widths[tb]= results1
        xsec_times_BR[tb]= results2
        xsec[tb]= results3
        print (80*'*')
    mass_rng = 'from{}to{}'.format( float_to_str(list_masses.min(), 2), float_to_str(list_masses.max(), 2))
    tb_rng = 'from{}to{}'.format( float_to_str(list_tb.min(), 2), float_to_str(list_tb.max(), 2))
    json_Totalwidth='data/totalwidth_2HDM-type{}_cosbeta-alpha-{}_func_of_tb-{}_{}-{}.json'.format(type, float_to_str(cba, 2), tb_rng, options.scan.upper(), mass_rng)
    json_Totalxsc='data/totalxsc_2HDM-type{}_cosbeta-alpha-{}_func_of_tb-{}_{}-{}.json'.format(type, float_to_str(cba, 2), tb_rng, options.scan.upper(), mass_rng)
    json_TotalxscXbr='data/totalxscXbr_2HDM-type{}_cosbeta-alpha-{}_func_of_tb-{}_{}-{}.json'.format(type, float_to_str(cba, 2), tb_rng, options.scan.upper(), mass_rng)
    with open(json_Totalwidth, 'w+') as f:
        json.dump(widths, f)
    with open(json_TotalxscXbr, 'w+') as f:
        json.dump(xsec_times_BR, f)
    with open(json_Totalxsc, 'w+') as f:
        json.dump(xsec, f)
    
    return ((json_TotalxscXbr if return_scaledXSC else( json_Totalxsc) )if not return_totalwidth else (json_Totalwidth))

def MakeWidthPLots(M, TANbeta, LookatNWA = False):
    fig, ax = plt.subplots(figsize=(8, 6))
    if options.lazy:
        jsonfile='data/totalwidth_2HDM-type2_cosbeta-alpha-0p01_func_of_tb.json'
    else:
        jsonfile= Calculators42HDM(M, TANbeta, return_scaledXSC= False, return_totalwidth= True)

    with open(jsonfile) as f:
        data = json.load(f)
    tb_toplot = ["1.0", "1.5", "3.0", "10.0", "19.0"]
    colors = ["#CD5C5C", "#0e6655", "darkred", "#85c1e9", "#8e44ad", "#d4ac0d" , "aqua", "#273746"]
    from matplotlib import colors as mcolors
    for idx, beta in enumerate(tb_toplot):
       
        x= data[beta][options.scan]
        
        SM_M = [125.]*len(data[beta]['hwidth']) if LookatNWA else (1.)
        Heavy_M = data[beta]["mH"] if LookatNWA else(1.)
        Pseudo_M = data[beta]["mA"] if LookatNWA else(1.)

        if LookatNWA:
            y_hwidth = [i / j for i, j in zip(data[beta]['hwidth'], SM_M)]
            y_Hwidth = [i / j for i, j in zip(data[beta]['Hwidth'], Heavy_M)]
            y_Awidth = [i / j for i, j in zip(data[beta]['Awidth'], Pseudo_M)]
            
            Hwidth_dev_mass = [(i / j)*100 for i, j in zip(data[beta]['Hwidth'], Heavy_M)]
            Awidth_dev_mass = [(i / j)*100 for i, j in zip(data[beta]['Awidth'], Pseudo_M)]
            print( ' Gamma/mass_A: ', Awidth_dev_mass, ' Gamma/mass_H: ', Hwidth_dev_mass)
        else:
            y_hwidth =data[beta]['hwidth']     
            y_Hwidth =data[beta]['Hwidth']  
            y_Awidth =data[beta]['Awidth']     
            #y_Hcwidth =data[beta]['H+width']

        plt.plot(x, y_hwidth, color=colors[idx+1], linestyle=(0, (3, 1, 1, 1)), linewidth=2, markersize=10)#, alpha = 0.5)#, label='$\Gamma_{SM}$')
        plt.plot(x, y_Hwidth, color=colors[idx+1], linewidth=2.5, markersize=10, label=r'tan$\beta = %s$'%beta.replace('.0','')) 
        plt.plot(x, y_Awidth, color=colors[idx+1], linestyle='dashed', linewidth=2.5, markersize=10)#, label='$\Gamma_{A}$') 
        #plt.plot(x, y_Hcwidth, color=colors[i+1], linestyle='dashed', linewidth=2.5, markersize=12)#, label='$\Gamma_{H+}$') 
    title = r'M_{A}= M_{H}-M_{Z}' if options.scan=='mH' else ( r'M_{H}= M_{A}+M_{Z}')
    plt.title(r'$2HDM-typeII: %s, M_{H^\pm}=M_{H}, cos(\beta-\alpha)= 0.01, m12= (M_{H^\pm}^2 *tan\beta )/(1+tan\beta^2), mh= 125. GeV$'%(title), fontsize=10)
    labelLines(plt.gca().get_lines(),align=True,fontsize=10)#, backgroundcolor="#ffffff00")
    
    ax.set_ylabel(r'$\Gamma_{tot} /M [GeV]$', fontsize=18, horizontalalignment='right', y=1.0)
    ax.set_xlabel(r'${}[GeV]$'.format(options.scan.upper()), fontsize=14, horizontalalignment='right', y=1.0)
    xmin= (30. if  options.scan=="mA" else(120.))
    xmax= (1100. if  options.scan=="mA" else(1200.))
    ymin = 1e-5
    ymax = 10e-1
    
    ax.set_xlim(xmin=xmin, xmax=xmax)
    ax.set_ylim(ymin=ymin, ymax=ymax)
    ax.set_yscale('log')
    ax.grid(linestyle='dashed')
    ax.legend([r'$\Gamma_{SM}$', r'$\Gamma_{A}$', r'$\Gamma_{H}$'])

    fig.tight_layout()
    fig.savefig('scan{}_vs_totalwidth{}.png'.format(options.scan, 'DividedMass' if LookatNWA else('')))
    #fig.savefig('scan{}_vs_totalwidth{}.pdf'.format(options.scan))
    plt.gcf().clear()

    return fig

def MakeXSCPLots(M, TANbeta):
    fig= plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111)
    
    #number = 11
    #cmap = plt.get_cmap('gnuplot')
    #colors = [cmap(i) for i in np.linspace(0, 1, number)]
    colors = ["#CD5C5C", "#0e6655", "darkred", "#85c1e9", "#8e44ad", "#d4ac0d" , "aqua", "#273746"]
    CMSStyle.changeFont()
    
    if options.lazy: 
        jsonfile='data/totalxsc_2HDM-type2_cosbeta-alpha-0p01_func_of_tb.json'
    else:
        jsonfile= Calculators42HDM(M, TANbeta, return_scaledXSC= options.scale, return_totalwidth= False)
  
    with open(jsonfile) as f:
        data = json.load(f)
    for k, beta in enumerate(["1.0", "1.5", "3.0", "10.0", "19.0"]):
        x = data[beta][options.scan]
        y_xsc_gg=data[beta]['gg-fusion']
        y_xsc_bb=data[beta]['bb-associated_production']

        print( 'gg->H max:', max(y_xsc_gg),' [pb] bb->H max:', max(y_xsc_bb), '[pb]')
        plt.plot(x, y_xsc_gg, color=colors[k], linewidth=2.0, label=r'tan$\beta = %s$'%beta.replace('.0',''))
        plt.plot(x, y_xsc_bb, color=colors[k],  linewidth=2.0, linestyle='dashed')# label='_nolegend_',
    
    plt.title(r'$2HDM-typeII: M_{A}= M_{H}-M_{Z}, M_{H^+}=M_{H}, cos(\beta-\alpha)= 0.01, m12= 0. GeV, mh= 125. GeV$', fontsize=10)

    xmin= (30. if  options.scan=="mA" else(120.))
    xmax= (1100. if  options.scan=="mA" else(200.))
    ymin = 1e-3
    ymax = 10e2
    ax.set_xlim(xmin=xmin, xmax=xmax)
    ax.set_ylim(ymin=ymin, ymax=ymax)
    
    top_line = [(172.76 *2, ymin), (172.76 *2, ymax)]
    from matplotlib.collections import LineCollection
    lc = LineCollection([top_line], linestyle='dashed', color=["gold"], lw=2.0, label='r$ 2*M_{top}$')

    plt.xlabel(r'{} [GeV]'.format(options.scan.upper()), fontsize=14, horizontalalignment='right', x=1.0)
    plt.ylabel(r'$\sigma [pb]$', fontsize=14, horizontalalignment='right', x=1.0)
    ax.set_yscale('log')
    ax.grid(linestyle='dashed')
    
    leg= plt.legend(labels= ['gg-fusion', 'bb-associated_production'], loc='best')
    plt.gca().add_artist(leg)
    
    plt.gca().add_collection(lc)
    labelLines(plt.gca().get_lines(),align=True,fontsize=10)
    
    fig.savefig('1Dscan_{}_vs_xsc.png'.format(options.scan))
    #fig.savefig('1Dscan_{}_vs_xsc.pdf'.format(options.scan))
    
    plt.gcf().clear()
    return fig

def MakePLotsIn2D(M, TANbeta, interploate=False):
    #import prettyplotlib as plt 
    fig, (axs1, axs2) = plt.subplots(1, 2, figsize=(23, 12), dpi=300)#, gridspec_kw={'height_ratios': [1.3]})
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.27, hspace=None)
    
    if options.lazy:
        #jsonfile=( 'data/totalxscXbr_2HDM-type2_cosbeta-alpha-0p01_func_of_tb.json' if options.scale else('data/totalxsc_2HDM-type2_cosbeta-alpha-0p01_func_of_tb.json'))
        jsonfile=( 'data/totalxscXbr_2HDM-type2_cosbeta-alpha-0p01_func_of_tb-from0p50to59p50_MH-from125p00to1125p00.json' if options.scale else('data/totalxsc_2HDM-type2_cosbeta-alpha-0p01_func_of_tb-from0p50to59p50_MH-from125p00to1125p00.json'))
    else:
        jsonfile= Calculators42HDM(M, TANbeta, return_scaledXSC = options.scale , return_totalwidth= False)

    with open(jsonfile) as f:
        data = json.load(f)
    x_axis =[]
    y_axis =[]
    z1_axis=[]
    z2_axis=[]
    
    for k in sorted( float(k) for k in data.keys()):
        x= data[str(k)][options.scan]
        y = [k]*len(x)
        z1_xsc_gg=data[str(k)]['gg-fusion']
        z2_xsc_bb=data[str(k)]['bb-associated_production']
        x_axis.append( x)
        y_axis.append( y)
        z1_axis.append(z1_xsc_gg)
        z2_axis.append(z2_xsc_bb)
    #print( sorted( float(k) for k in data.keys()) )
    #print( 'y len:', len(y_axis), 'x len:', len(x_axis))     
    #print( max(range(len(z1_axis))), max(range(len(z1_axis)), key=z1_axis.__getitem__))
    
    new_x = np.asarray(x_axis)
    new_y = np.asarray(y_axis)
    
    z1 = np.asarray(z1_axis)
    z2 = np.asarray(z2_axis)
    if interploate:
        interp_x = np.arange(new_x.min(), new_x.max(), 10.)
        interp_y = np.arange(new_y.min(), new_x.max(), 1.)
        #print( len(interp_x), len(interp_y))
        X, Y = np.meshgrid(interp_x, interp_y)
        
        fun1 = interpolate.interp2d(new_x, new_y, z1, kind='cubic')
        fun2 = interpolate.interp2d(new_x, new_y, z2, kind='cubic')
        Z1= fun1( interp_x, interp_y)
        Z2= fun2( interp_x, interp_y)
        #z1_reshape = Z1.reshape(len(interp_x), len(interp_y))
        #z2_reshape = Z2.reshape(len(interp_x), len(interp_y))
    
    xmin = (125. if options.scan=='mH' else (30.))
    xmax = 1000.
    from mpl_toolkits.axes_grid1 import make_axes_locatable    
    from matplotlib.ticker import LogFormatter 
    import matplotlib.colors as colors
   
    optstitle = ('M_{A}= M_{H}-M_{Z}'if options.scan =='mH' else( 'M_{H}= M_{A}+M_{Z}'))
    axs1.title.set_text(r'$2HDM-TypeII: cos(\beta-\alpha)= 0.01, mh = 125., %s, M_{H^+}=M_{H}$'%optstitle)
    axs1.set_xlabel('{} [GeV]'.format(options.scan.upper()), horizontalalignment='center',fontsize=18)
    axs1.set_ylabel( r'$tan\beta$', horizontalalignment='right', fontsize=18)
    #axs1.xaxis.set_ticks(M)
    #axs1.yaxis.set_ticks(TANBETA)
    axs1.set_xlim([xmin, xmax])
    axs1.set_ylim([new_y.min(), new_y.max()])
    #axs1.set_xscale('log')
    #axs1.set_yscale('log')
    
    from matplotlib.colors import BoundaryNorm
    from matplotlib.ticker import MaxNLocator
    cmap = plt.get_cmap('jet')
    levels = MaxNLocator(nbins=15).tick_values(z1.min(), z1.max())
    if interploate :
        im1 = axs1.pcolormesh( interp_x, interp_y, Z1, cmap=cmap, norm=colors.SymLogNorm(linthresh=0.03, linscale=0.03, vmin = z1.min(), vmax = z1.max()))
    else:
        #im1 = axs1.pcolormesh( new_x, new_y, z1, cmap=cmap, norm=BoundaryNorm(levels, ncolors=cmap.N, clip=True) )
        im1 = axs1.pcolormesh( new_x, new_y, z1, cmap=cmap, norm=colors.LogNorm(vmin = z1.min(), vmax = z1.max()))

    divider = make_axes_locatable(axs1)
    cax1 = divider.append_axes("right", size="5%", pad=0.05)
    #cax1.set_xticks(new_x)
    #cax1.set_yticks(new_y)
    cbar1 = plt.colorbar(im1, cax=cax1)
    if options.scale: 
        cbar1.set_label(label=r'$\sigma (gg fusion)* BR(H \rightarrow ZA)* BR(A \rightarrow bb) [pb]$', size=18)
    else:
        cbar1.set_label(label=r'$\sigma$ (gg fusion) [pb]', size=18)
    #cbar.ax.tick_params(labelsize=18)

    axs2.title.set_text(r'$2HDM-TypeII: cos(\beta-\alpha)= 0.01, mh = 125., %s, M_{H^\pm}=M_{H}$'%optstitle)
    axs2.set_xlabel('{} [GeV]'.format(options.scan.upper()), horizontalalignment='center', fontsize=18)
    axs2.set_ylabel( r'$tan\beta$', horizontalalignment='right', fontsize=18)
    axs2.set_xlim([xmin, xmax])
    axs2.set_ylim([new_y.min(), new_y.max()])
    if interploate:
        #im2 = axs2.pcolormesh( interp_x, interp_y, Z2, cmap=cmap, norm=colors.SymLogNorm(linthresh=0.03, linscale=0.03, vmin = z2.min(), vmax = z2.max()))
        im2 = axs2.pcolormesh( interp_x, interp_y, Z2, cmap=cmap, norm=colors.LogNorm(vmin = z2.min(), vmax = z2.max()))
    else:
        #im2 = axs2.pcolormesh( new_x, new_y, z2, cmap=cmap, norm=BoundaryNorm(levels, ncolors=cmap.N, clip=True) )
        im2 = axs2.pcolormesh( new_x, new_y, z2, cmap=cmap, norm=colors.LogNorm(vmin = z2.min(), vmax = z2.max()))

    divider = make_axes_locatable(axs2)
    cax2 = divider.append_axes("right", size="5%", pad=0.05)
    cbar2 = plt.colorbar(im2, cax=cax2)
    if options.scale:
        cbar2.set_label(label =r'$\sigma (bb associated production)* BR(H \rightarrow ZA)* BR(A \rightarrow bb) [pb]$', size=18)
    else:
        cbar2.set_label(label =r'$\sigma$ (bb associated production) [pb]',size=18)
    #cbar.ax.tick_params(labelsize=18)
    
    #plt.tight_layout()
    plt.savefig("2Dscan_totalxsc_func_{}_and_tanbeta.png".format(options.scan))
    plt.savefig("2Dscan_totalxsc_func_{}_and_tanbeta.pdf".format(options.scan))
    #plt.grid()
    plt.gcf().clear()
    return fig

global options
options = get_options()
TANbeta = np.arange(0.5, 60.5, 1. )

if options.scan =="mA":
    M = np.arange(30.,1100.,100. )

elif options.scan =="mH":
    M = np.arange(125.,1190.,100. )

#MakeXSCPLots(M, TANbeta) 
MakeWidthPLots(M, TANbeta, LookatNWA = True)
MakePLotsIn2D(M, TANbeta, interploate=False)
