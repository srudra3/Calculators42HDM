# Keep An Eye To The Latest Versions : 
- [2HDMC](https://2hdmc.hepforge.org)
- [SUSHI](https://sushi.hepforge.org/)
- [LHAPDF](https://lhapdf.hepforge.org/index.html)

- NOT NECESSARY TO WORK WITH 2HDMC 
- [HiggsBounds](http://higgsbounds.hepforge.org)
- [HiggsSignals](http://higgsbounds.hepforge.org)

# Calculators For 2HDM
Tools to use SusHi and 2HDMC to compute H/A/h cross section and branching fractions. 

    ## In a CMSSW release
```bash
    # setup your env 
    module load gcc/gcc-7.3.0-sl7_amd64 lhapdf/6.1.6-sl7_gcc73
    # Install a CMSSW release .eg. CMSSW_10_2_22
    cmsrel CMSSW_10_2_22
    cmsenv
    git cms-init

    # Get and execute the install script
    wget https://raw.githubusercontent.com/cp3-llbb/Calculators42HDM/master/sushi_2hdmc_cmssw.sh
    source sushi_2hdmc_cmssw.sh

    # Setup github remotes
    source first_setup.sh
```
    ## With Conda (from @pdavid) 
- [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/linux.html)
- [CONDA-FORGE](https://conda-forge.org/#page-top)

```bash
    # setup your env
    conda create -n SusHi170 gsl gfortran_linux-64 gxx_linux-64 gcc_linux-64
    conda activate SusHi170

    wget https://raw.githubusercontent.com/cp3-llbb/Calculators42HDM/master/sushi_2hdmc_conda.sh
    source sushi_2hdmc_conda.sh
```

## Run the test
    
    python example/test.py
##Troubleshooting: 
```
lib/libsushi2HDMC.a(runthdmc.o): In function `runthdmc_':
runthdmc.f:(.text+0x13d): undefined reference to `thdmc_set_param_'
collect2: error: ld returned 1 exit status
make[1]: *** [Makefile:197: bin/sushi.2HDMC] Error 1
```
```
    -CFLAGS= -std=c++11 -Wall $(DEBUG) $(OPT)
    +CFLAGS= -std=c++11 -Wall -fPIE $(DEBUG) $(OPT)
    -SOURCES=THDM.cpp SM.cpp DecayTable.cpp Constraints.cpp Util.cpp
    +SOURCES=THDM.cpp SM.cpp DecayTable.cpp Constraints.cpp Util.cpp runTHDM.cpp
```
