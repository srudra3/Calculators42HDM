#!/usr/bin/python

import sys
import math
from cp3_llbb.Calculators42HDM.Calc2HDM import *
from ROOT import *

def ScanPlane(mHinit,mHend,mAinit,mAend,tag, tb, muR=0.5, muF=0.5) :
    mH=mHinit
    nIterParAxis=200
    binsizeX=(mAend-mAinit)/(nIterParAxis-1)
    binsizeY=(mHend-mHinit)/(nIterParAxis-1)
    Xsec_TH2F = TH2F("h","h",nIterParAxis,mAinit-binsizeX/2,mAend+binsizeX/2,nIterParAxis,mHinit-binsizeY/2,mHend+binsizeY/2)
    Xsec_TH2F.SetName("Xsec_Scan_"+tag)
    n=0
    while mH < mHend:
        mA=mAinit
        test.setmH(mH)
        test.setmHc(mH)
        test.settb(tb)
        test.setm12(math.sqrt(test.mhc*test.mhc*test.tb/(1+test.tb)))
        test.setm122(mH*mH*tb/(1+tb))
        test.setmuR(muR)
        test.setmuF(muF)
        test.setmA(mAinit)
        xsec =  test.getXsecFromSusHi()
        while mA < test.mH-90:
           test.setmA(mA) 
           test.computeBR()  
           Xsec_TH2F.Fill(mA,mH,1000*xsec*test.HtoZABR*test.AtobbBR*0.067) 
           mA+=binsizeX
           n+=1
        mH+=binsizeY 
    Xsec_TH2F.Write()

def DrawXsecLine(mH,mAinit,tag, tb,pdf, muR=0.5, muF=0.5) :
 
    test.setmH(mH)
    test.setmHc(mH)
    test.settb(tb)
    test.setm12(math.sqrt(test.mhc*test.mhc*test.tb/(1+test.tb)))
    test.setm122(mH*mH*tb/(1+tb))
    test.setmuR(muR)
    test.setmuF(muF)
    test.setmA(mAinit)
    test.setpdf(pdf)
    xsec =  test.getXsecFromSusHi()
    Xsec_Gr = TGraph(50)
    Xsec_Gr.SetName("Xsec_mH"+str(test.mH)+"_tb"+str(test.tb)+"_"+tag)
    n=0
    mA=mAinit
    while mA < test.mH-90:
        test.setmA(mA)
        test.computeBR()
        print "ZA BR", test.HtoZABR
        Xsec_Gr.SetPoint(n,mA,1000*xsec*test.HtoZABR*test.AtobbBR*0.067)
        mA+=2
        n+=1
    Xsec_Gr.Write()
    


mode = 'H'
sqrts = 13000
type = 2
tb = 1.5
m12 = 0
mh = 125
mH = 300
mA = 50
mhc = 800

beta=math.atan(tb)
cba = 0.01
alpha=math.atan(tb)-math.acos(cba)
sba = math.sin(math.atan(tb)-alpha)

print 'sba : ', sba

outputFile = "out.dat"


test = Calc2HDM(mode = 'H', sqrts = sqrts, type = type, tb = tb, m12 = m12, mh = mh, mH = mH, mA = mA, mhc = mhc, sba = sba, outputFile = outputFile)

file_out = TFile("xsec.root","RECREATE")

#ScanPlane(300.0,800.0,50.0,722.0,"test", 1,muR = 1, muF = 1)

for mH in [300,500,800]:

	for tgbeta in [0.5,1,1.5]:
	        tgbetaS="init"
	        if tgbeta==0.5 :
	 		tbetaS="tgbeta05"
		if tgbeta==1 :
			tbetaS="tgbeta1"
		if tgbeta==1.5 :
			tbetaS="tgbeta15"
	 
		DrawXsecLine(mH,50,"1_1_"+tbetaS+"_CT10nnlo", tgbeta,'CT10nnlo.LHgrid', muR = 1, muF = 1)
	        DrawXsecLine(mH,50,"1_1_"+tbetaS+"MMHT2014nnlo68cl", tgbeta,'MMHT2014nnlo68cl.LHgrid', muR = 1, muF = 1)
		DrawXsecLine(mH,50,"1_1_"+tbetaS+"NNPDF30_nnlo", tgbeta,'NNPDF30_nnlo_as_0118', muR = 1, muF = 1)
	    
		DrawXsecLine(300,50,"05_05_"+tbetaS+"_CT10nnlo", tgbeta, 'CT10nnlo.LHgrid',muR = 0.5, muF = 0.5)
		DrawXsecLine(300,50,"05_1_"+tbetaS+"_CT10nnlo", tgbeta,'CT10nnlo.LHgrid', muR = 0.5, muF = 1)
		
		DrawXsecLine(300,50,"1_05_"+tbetaS+"_CT10nnlo", tgbeta,'CT10nnlo.LHgrid', muR = 1, muF = 0.5)
		DrawXsecLine(300,50,"1_1_"+tbetaS+"_CT10nnlo", tgbeta,'CT10nnlo.LHgrid', muR = 1, muF = 1)
		DrawXsecLine(300,50,"1_2_"+tbetaS+"_CT10nnlo", tgbeta,'CT10nnlo.LHgrid', muR = 1, muF = 2)
		
		DrawXsecLine(300,50,"2_1_"+tbetaS+"_CT10nnlo", tgbeta,'CT10nnlo.LHgrid', muR = 2, muF = 1)
		DrawXsecLine(300,50,"2_2_"+tbetaS+"_CT10nnlo", tgbeta,'CT10nnlo.LHgrid', muR = 2, muF = 2)
