import os, os.path

class CalcMadWidths:
    def __init__(self, param_card=None, cardtype=None):
        self.mh1 = 0.
        self.mh2 = 0.
        self.mh3 = 0.
        self.mhc = 0.

        self.tb = 0.
        self.sba = 0.

        self.totwh1 = 0.
        self.totwh2 = 0.
        self.totwh3 = 0.
        self.totwhc = 0.

        self.wh1tobb = 0.
        self.wh2tobb = 0.
        self.wh3tobb = 0.

        ##############
        self.h3togluhBR = 0.
        
        self.h3toZhBR = 0.

        self.h2toHpWmBR = 0.
        self.h3toHpWmBR = 0.
        
        self.h2toHmWpBR = 0.
        self.h3toHmWpBR = 0.
        
        self.h2toWWBR = 0.
      
        self.h2toZZBR   = 0.
        
        self.h1tobbBR   = 0.
        self.h2tobbBR   = 0.
        self.h3tobbBR   = 0.
        
        self.h1totautauBR = 0.
        self.h2totautauBR = 0.
        self.h3totautauBR = 0.
        
        self.h2totoptopBR = 0.
        self.h3totoptopBR = 0.
        
        self.h1toglugluBR = 0.
        self.h2toglugluBR = 0.
        self.h3toglugluBR = 0.

        self.ymb= 0.
        self.param_card= param_card
        self.cardtype= cardtype
    
    def __str__(self):
        return """param_card=%s
    cardtype=%s"""%(param_card, cardtype)
    
    def setparam_card(self,param_card) :
        self.param_card=param_card
    
    def setcardtype(self, cardtype):
        self.cardtype=cardtype
    
    #@staticmethod 
    def get_widths_and_BR(self):
    
        """                             
        ###################################
                  2HDMC 1.8.0 
        ###################################
                                    NDA    ID1   ID2
        h / H/ A/ H+-  -> s  s       2       3    -3 
        h / H/ A/ H+-  -> c  c       2       4    -4
        h / H/ A/ H+-  -> b  b       2       5    -5
        h / H/ A/ H+-  -> e  e       2      11   -11
        h / H/ A/ H+-  -> mu mu      2      13   -13
        h / H/ A/ H+-  -> ta ta      2      15   -15
        h / H/ A/ H+-  -> ga ga      2      22    22
        h / H          -> Z  Z       2      23    23
        h / H          -> W+ W-      2      24   -24
        h / H/ A       -> Z  ga      2      23    22
        h / H/ A       -> g  g       2      21    21

        A              -> Z  h       2      23    25
        H              -> Z  A       2      23    36
        
        H+             -> u  s       2       2    -3
        H+             -> u  b       2       2    -5
        H+             -> c  d       2       4    -1
        H+             -> c  s       2       4    -3
        H+             -> c  b       2       4    -5
        H+             -> t  d       2       6    -1
        H+             -> t  s       2       6    -3
        H+             -> t  b       2       6    -5
        H+             -> e  ve      2     -11    12
        H+             -> mu vm      2     -13    14
        H+             -> ta vt      2     -15    16
        H+             -> W+ h       2      24    25
        H+             -> W+ A       2      24    36
        
        ###################################
                  UFO model 
        ###################################
                                    NDA    ID1   ID2
        H / A          -> H+ W-      2    37  -24
        H / A          -> H- W+      2    -37  24 
        h / H/ A       -> b  b~      2    5  -5 
        h / H/ A       -> ta ta~     2    15  -15
        H / A          -> t  t~      2    6  -6
        H              -> W- W+      2    -24  24
        H              -> h  h       2    25  25
        H              -> Z  Z       2    23  23
        H              -> H+ H-      2    -37  37
        H              -> ga A       2    22  36
        h / H/         -> g  g       2    22  22
                
        A              -> h  Z       2    25  23
        A              -> g  h       2    22  25
        """
        thdm_decays_dict = {'toss'    :'2       3    -3',
                        'tocc'    :'2       4    -4',
                        'tobb'    :'2       5    -5',
                        'toee'    :'2      11   -11',
                        'tomumu'  :'2      13   -13',
                        'totautau':'2      15   -15',
                        'togg'    :'2      22    22',
                        'toZZ'    :'2      23    23',
                        'toWW'    :'2      24   -24',
                        'toZga'   :'2      23    22',
                        'togluglu':'2      21    21',
                        'toZh'    :'2      23    25', 
                        'toZA'    :'2      23    36'
                        }
    
        ufo_decay_dict = {'toHmWp':  '2    37  -24', 
                      'toHmWp':  '2    -37  24',
                      'toWW':    '2    -24  24',
                      'toZZ'  :  '2    23  23',
                      'tocc':    '2    4  -4',
                      'tobb':    '2    5  -5',
                      'tomumu':  '2    13  -13',
                      'totautau':'2    15  -15',
                      'totoptop':'2    6  -6',
                      'togg':    '2    22  22',
                      'tohZ':    '2    25  23',
                      'togluh':  '2    22  25' 
                      }
        switch_h1=0
        switch_h2=0
        switch_h3=0
        switch_hc=0
        with open(os.path.join(self.param_card)) as f:
            partial_decay_width =0.
            BR_per_decay=0.
            for line in f:
                if 'DECAY  25' in line: 
                    self.totwh1 = float(line.split()[2])
                    switch_h1=1
                    switch_h2=0
                    switch_h3=0
                    switch_hc=0
                elif 'DECAY  35' in line: 
                    self.totwh2 = float(line.split()[2])
                    switch_h1=0
                    switch_h2=1
                    switch_h3=0
                    switch_hc=0
                elif 'DECAY  36' in line: 
                    self.totwh3 = float(line.split()[2])
                    switch_h1=0
                    switch_h2=0
                    switch_h3=1
                    switch_hc=0
                elif 'DECAY  37' in line: 
                    self.totwhc = float(line.split()[2])
                    switch_h1=0
                    switch_h2=0
                    switch_h3=0
                    switch_hc=1

                decays_dict = (ufo_decay_dict if self.cardtype=='ufo' else( thdm_decays_dict))
               
                for decay_key, decay_pdg in decays_dict.items():
                    if decay_pdg not in line:
                        continue
                    partial_decay_width = float(line.replace('#', ' ').split()[-1])
                    BR_per_decay= float(line.split()[0])
                    #print(line, partial_decay_width, BR_per_decay, decay_key)
                
                    if switch_h1==1:
                        setattr(self, "wh1%s"%decay_key, partial_decay_width)
                        setattr(self, "h1%sBR"%decay_key, BR_per_decay)
                    elif switch_h2==1:
                        setattr(self, "wh2%s"%decay_key, partial_decay_width)
                        setattr(self, "h2%sBR"%decay_key, BR_per_decay)
                    elif switch_h3==1:
                        setattr(self, "wh3%s"%decay_key, partial_decay_width)
                        setattr(self, "h3%sBR"%decay_key, BR_per_decay)
