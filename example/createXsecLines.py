#!/usr/bin/python


import math
from cp3_llbb.Calculators42HDM.Calc2HDM import *
from ROOT import *

def ScanPlane(mHinit,mHend,mAinit,mAend,tag, tb, muR=0.5, muF=0.5) :
    mH=mHinit
    Xsec_Gr2D = TGraph2D(1000)
    Xsec_Gr2D.SetName("Xsec_Scan_"+tag)
    n=0
    while mH < mHend:
        print "mH is ",mH
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
           print "--> mA is ",mA
           test.setmH(mH)
           test.setmHc(mH)
           test.settb(tb)
           test.setm12(math.sqrt(test.mhc*test.mhc*test.tb/(1+test.tb)))
           test.setm122(mH*mH*tb/(1+tb))
           test.setmuR(muR)
           test.setmuF(muF)
           test.setmA(mA) 
           test.computeBR()  
           Xsec_Gr2D.SetPoint(n,mA,mH,1000*xsec*test.HtoZABR*test.AtobbBR*0.067) 
           mA+=5
           n+=1
        mH+=5 
    Xsec_Gr2D.Write()

def DrawXsecLine(mH,mAinit,tag, tb, muR=0.5, muF=0.5) :
 
    test.setmH(mH)
    test.setmHc(mH)
    test.settb(tb)
    test.setm12(math.sqrt(test.mhc*test.mhc*test.tb/(1+test.tb)))
    test.setm122(mH*mH*tb/(1+tb))
    test.setmuR(muR)
    test.setmuF(muF)
    test.setmA(mAinit)
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
#        Xsec_Gr.SetPoint(n,mA,1000*xsec)
#        Xsec_Gr.SetPoint(n,mA,test.HtoZABR)
#        Xsec_Gr.SetPoint(n,mA,test.AtobbBR)
        mA+=2
        n+=1
    Xsec_Gr.Write()
    


mode = 'H'
sqrts = 13000
type = 2
tb = 1
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

ScanPlane(300,800,50,700,"test", 1,muR = 1, muF = 1)

'''
DrawXsecLine(300,50,"05_05", 1, muR = 0.5, muF = 0.5)
DrawXsecLine(300,50,"05_1", 1, muR = 0.5, muF = 1)

DrawXsecLine(300,50,"1_05", 1, muR = 1, muF = 0.5)
DrawXsecLine(300,50,"1_1", 1, muR = 1, muF = 1)
DrawXsecLine(300,50,"1_2", 1, muR = 1, muF = 2)

DrawXsecLine(300,50,"2_1", 1, muR = 2, muF = 1)
DrawXsecLine(300,50,"2_2", 1, muR = 2, muF = 2)

DrawXsecLine(500,50,"05_05", 1, muR = 0.5, muF = 0.5)
DrawXsecLine(500,50,"05_1", 1, muR = 0.5, muF = 1)

DrawXsecLine(500,50,"1_05", 1, muR = 1, muF = 0.5)
DrawXsecLine(500,50,"1_1", 1, muR = 1, muF = 1)
DrawXsecLine(500,50,"1_2", 1, muR = 1, muF = 2)

DrawXsecLine(500,50,"2_1", 1, muR = 2, muF = 1)
DrawXsecLine(500,50,"2_2", 1, muR = 2, muF = 2)

DrawXsecLine(800,50,"05_05", 1, muR = 0.5, muF = 0.5)
DrawXsecLine(800,50,"05_1", 1, muR = 0.5, muF = 1)

DrawXsecLine(800,50,"1_05", 1, muR = 1, muF = 0.5)
DrawXsecLine(800,50,"1_1", 1, muR = 1, muF = 1)
DrawXsecLine(800,50,"1_2", 1, muR = 1, muF = 2)

DrawXsecLine(800,50,"2_1", 1, muR = 2, muF = 1)
DrawXsecLine(800,50,"2_2", 1, muR = 2, muF = 2)
'''
