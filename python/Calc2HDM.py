#!/usr/bin/python
import os
import sys
import linecache


class Calc2HDM:
    def __init__(self, mode = 'H', sqrts = 13000,  muR = 0.5, muF = 0.5, type = 2, tb = 1, m12 = 0, mh = 125, mH = 350, mA = 400, mhc = 420, sba = 0.99, outputFile = "out.dat"):

        # 11 = light Higgs (h), 12 = heavy Higgs (H), 21 = pseudoscalar (A)
        if mode == 'h' :
            self.mode = 11
        elif mode == 'H' :
            self.mode = 12
        elif mode == 'A' :
            self.mode = 21
        else :
            print "Wrong mode selected! Please, use h, H or A." 

        self.tb = tb
        self.m12 = m12
        self.m12_2 = m12*m12
        self.mh = mh
        self.mH = mH
        self.mA = mA
        self.mhc = mhc
        self.sba = sba
        self.type = type
        self.outputFile = outputFile
        self.sqrts = sqrts
        self.muR = muR
        self.muF = muF
        self.BRcomputed = 0
        self.pdf = "CT10nnlo.LHgrid" 
        #initializing all BRs
         
        self.HtoZABR = 0
        self.AtoZHBR = 0
        self.HtoAABR = 0
        self.htoAABR = 0
        self.AtoHHBR = 0

        self.HtobbBR = 0
        self.htobbBR = 0
        self.AtobbBR = 0

        self.HtoZhBR = 0
        self.AtoZhBR = 0

        self.HtottBR = 0
        self.htottBR = 0
        self.AtottBR = 0
        
        self.HtotautauBR = 0
        self.htotautauBR = 0
        self.AtotautauBR = 0

        self.HtohhBR = 0
        self.AtohhBR = 0

        self.HtoZZBR = 0
        self.htoZZBR = 0
        self.AtoZZBR = 0
        self.HtoWWBR = 0
        self.htoWWBR = 0
        self.AtoWWBR = 0

        self.HtoglugluBR = 0
        self.htoglugluBR = 0
        self.AtoglugluBR = 0
        self.HtoggBR = 0
        self.htoggBR = 0
        self.AtoggBR = 0

        self.stability = 0
        self.unitarity = 0
        self.perturbativity = 0

    def setmA(self, M) :
        self.mA = M

    def settb(self, tb) :
        self.tb = tb

    def setmH(self, M) :
        self.mH = M

    def setmuF(self, muF) :
        self.muF = muF

    def setmuR(self, muR) :
        self.muR = muR

    def setmHc(self, M) :
        self.mhc = M
   
    def setm12(self, m12) :
        self.m12 = m12     

    def setm122(self, m122) :
        self.m122 = m122

    def setpdf(self,pdf) :
        self.pdf=pdf

    def getXsecFromSusHi(self) :
     
        sushiDefaultCardPath = "default_cards/default_sushi.in"
        sushiCardName = (str(self.mH).replace('.', 'p').replace('-', 'm') +
            "_" + str(self.mA).replace('.', 'p').replace('-', 'm') +
            "_" + str(self.muF).replace('.', 'p').replace('-', 'm') +
            "_" + str(self.muR).replace('.', 'p').replace('-', 'm') + 
            "_" + str(self.tb).replace('.', 'p').replace('-', 'm') +
            "_" + str(self.pdf)) # keep the dots in the pdf name
        sushiInputCardPath = "Scan/" + sushiCardName + ".in"
        sushiOutputCardPath = "Scan/" + sushiCardName + ".out"
     
        # Replacements of variables into the input file
        replacements = {'MODE':str(self.mode),'TANBETA':str(self.tb),'M12':str(self.m12),'MSMH':str(self.mh),'MHEAVYH':str(self.mH), 'MPSA':str(self.mA), 'MCHARGEDH':str(self.mhc), 'SINBA':str(self.sba), 'MUR':str(self.muR), 'MUF':str(self.muF),'TYPE':str(int(self.type)), 'SQRTS':str(self.sqrts),'CUSTOMPDFNNLO':str(self.pdf)}
        sushiDefaultCard = open(sushiDefaultCardPath)
        sushiInputCard = open(sushiInputCardPath, 'w')
        for line in sushiDefaultCard:
            for src, target in replacements.iteritems():
                line = line.replace(src, target)
            sushiInputCard.write(line)
        sushiDefaultCard.close()
        sushiInputCard.close()
     
        #running SusHi
        print "Running SusHi with command : ",
        run_sushi="./SusHi-1.5.0/bin/sushi "+sushiInputCardPath+" "+sushiOutputCardPath+" "
        print run_sushi
        os.system(run_sushi)
     
     
        # extracting xsec from the output file
        sushiOutputCard = open(sushiOutputCardPath,'r')
        XsecLine = linecache.getline(sushiOutputCardPath,16)
        XsecLine2 = XsecLine.replace("         1     ","")
        XsecLine3 = XsecLine2.replace("   # ggh XS in pb                  ","")
        Xsec = float(XsecLine3)
        sushiOutputCard.close()

 
        return Xsec



    def computeBR(self):

        command = "./2HDMC-1.7.0/CalcPhys "+str(self.mh)+" "+str(self.mH)+" "+str(self.mA)+" "+str(self.mhc)+" "+str(self.sba)+" 0 0 "+str(self.m12_2)+" "+str(self.tb)+" "+str(self.type)+" "+ self.outputFile
        os.system(command)

        print "reading theory constraints from "+ self.outputFile

        ParamCard = open(self.outputFile,'r')

        linecache.clearcache()

        UnitLine = linecache.getline(self.outputFile,14)
        UnitLine2 = UnitLine.replace("    2    ","")
        UnitLine3 = UnitLine2.replace("    #  Tree-level unitarity (1=Yes, 0=no)","")
        print UnitLine
        self.unitarity = bool(int(UnitLine3))

        PertLine = linecache.getline(self.outputFile,15)
        PertLine2 = PertLine.replace("    3    ","")
        PertLine3 = PertLine2.replace("    #  Perturbativity (1=Yes, 0=no)","")
        self.perturbativity = bool(int(PertLine3))
        print PertLine

        StabLine = linecache.getline(self.outputFile,16)
        StabLine2 = StabLine.replace("    4    ","")
        StabLine3 = StabLine2.replace("    #  Stability (1=Yes, 0=no)","")
        self.stability = bool(int(StabLine3))
        print StabLine

        modeh=0
        modeH=0
        modeA=0
      
        for line in ParamCard :
            if "DECAY  25" in line :
                modeh = 1
                modeH = 0
                modeA = 0
            if "DECAY  35" in line :
                modeh = 0
                modeH = 1
    	        modeA = 0
            elif "DECAY  36" in line :
                modeh = 0
                modeA = 1
        	modeH = 0
            elif "23    36" in line :
        	ABRLine2 = line.replace("       ","")
        	ZABRLine3 = ZABRLine2.replace("     2      23    36","")
                if modeH == 1 :
        	    self.HtoZABR = float(ZABRLine3)
                elif modeh == 1 :
                    self.htoZABR = float(ZABRLine3)

        	  #print "BR ZA", ZABR,
        
            elif "23    35" in line and modeA == 1 :
                ZHBRLine2 = line.replace("       ","")
                ZHBRLine3 = ZHBRLine2.replace("     2      23    35","")
                self.AtoZHBR = float(ZHBRLine3)
        
        
            elif "36    36" in line :
                AABRLine2 = line.replace("       ","")
                AABRLine3 = AABRLine2.replace("     2      36    36","")
                if modeH == 1 :
                    self.HtoAABR = float(AABRLine3)
                elif modeh == 1 :
                    self.htoAABR = float(AABRLine3)

                #print "BR ZA", ZABR,
        
            elif "35    35" in line and modeH == 1 :
              HHBRLine2 = line.replace("       ","")
              HHBRLine3 = HHBRLine2.replace("     2      35    35","")
              self.AtoHHBR = float(HHBRLine3)
        
        
            elif "5    -5" in line :
              bbBRLine2 = line.replace("     2       5    -5","")
              bbBRLine3 = bbBRLine2.replace("       ","")
              if modeH == 1 :
                self.HtobbBR = float(bbBRLine3)
              elif modeA == 1 :
                self.AtobbBR = float(bbBRLine3)
              elif modeh == 1 :
                self.htobbBR = float(bbBRLine3)
        
            elif "23    25" in line :
              ZhBRLine2 = line.replace("     2      23    25","")
              ZhBRLine3 = ZhBRLine2.replace("       ","")
              if modeH == 1 :
                self.HtoZhBR = float(ZhBRLine3)
              elif modeA == 1 :
                self.AtoZhBR = float(ZhBRLine3)
        
        
            elif "6    -6" in line :
              ttBRLine2 = line.replace("     2       6    -6","")
              ttBRLine3 = ttBRLine2.replace("       ","")
              if modeH == 1 :
                self.HtottBR = float(ttBRLine3)
              elif modeA == 1 :
                self.AtottBR = float(ttBRLine3)
              elif modeh == 1 :
                self.htottBR = float(ttBRLine3)
        
            elif "15   -15" in line :
              tautauBRLine2 = line.replace("     2      15   -15","")
              tautauBRLine3 = tautauBRLine2.replace("       ","")
              if modeH == 1 :
                self.HtotautauBR = float(tautauBRLine3)
              elif modeA == 1 :
                self.AtotautauBR = float(tautauBRLine3)
              elif modeh == 1 :
                self.htotautauBR = float(tautauBRLine3)
              #print "BR tautau", tautauBR
        
            elif "25    25" in line :
              hhBRLine2 = line.replace("     2      25    25","")
              hhBRLine3 = hhBRLine2.replace("       ","")
              if modeH == 1 :
                self.HtohhBR = float(hhBRLine3)
              elif modeA == 1 :
                self.AtohhBR = float(hhBRLine3)
              #print "BR hh", hhBR
        
            elif "23    23" in line :
              ZZBRLine2 = line.replace("     2      23    23","")
              ZZBRLine3 = ZZBRLine2.replace("       ","")
              if modeH == 1 :
                self.HtoZZBR = float(ZZBRLine3)
              elif modeA == 1 :
                self.AtoZZBR = float(ZZBRLine3)
              elif modeh == 1 :
                self.htoZZBR = float(ZZBRLine3)
              #print "BR ZZ", ZZBR
        
            elif "24   -24" in line :
              WWBRLine2 = line.replace("     2      24   -24","")
              WWBRLine3 = WWBRLine2.replace("       ","")
              if modeH == 1 :
                self.HtoWWBR = float(WWBRLine3)
              elif modeA == 1 :
                self.AtoWWBR = float(WWBRLine3)
              elif modeh == 1 :
                self.htoWWBR = float(WWBRLine3)
              #print "BR WW", WWBR
        
            elif "22    22" in line :
              ggBRLine2 = line.replace("     2      22    22","")
              ggBRLine3 = ggBRLine2.replace("       ","")
              if modeH == 1 :
                self.HtoggBR = float(ggBRLine3)
              elif modeA == 1 :
                self.AtoggBR = float(ggBRLine3)
              elif modeh == 1 :
                self.htoggBR = float(ggBRLine3)
              #print "BR gg", ggBR
       
            elif "21    21" in line :
              glugluBRLine2 = line.replace("     2      21    21","")
              glugluBRLine3 = glugluBRLine2.replace("       ","")
              if modeH == 1 :
                self.HtoglugluBR = float(glugluBRLine3)
              elif modeA == 1 :
                self.AtoglugluBR = float(glugluBRLine3)
              elif modeh == 1 :
                self.htoglugluBR = float(glugluBRLine3)

        ParamCard.close()
 
