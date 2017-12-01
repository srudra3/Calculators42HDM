# Calculators For 2HDM
Tools to use SusHi and 2HDMC to compute H/A/h cross section and branching fractions. 

```bash
    # Install a random CMSSW release, e.g. CMSSW_7_1_20_patch2
    export SCRAM_ARCH=slc6_amd64_gcc481
    scram p CMSSW CMSSW_7_1_20_patch2

    # Get and execute the install script
    wget https://raw.githubusercontent.com/cp3-llbb/Calculators42HDM/master/install_ingrid.sh
    source install_ingrid.sh

    # Setup github remotes
    source first_setup.sh
```

## Run the test
    
    python example/test.py

