# Calculators For 2HDM
Tools to use SusHi and 2HDMC to compute H/A/h cross section and branching fractions. 


    module load /nfs/soft/modules/lhapdf/6.1
    export SCRAM_ARCH=slc6_amd64_gcc493
    cmsenv

##First, installation of 2HDMC

    wget http://www.hepforge.org/archive/2hdmc/2HDMC-1.7.0.tar.gz
    cd 2HDMC-1.7.0
    make
    cd ..

##Second, SusHi installation :

    wget http://www.hepforge.org/archive/sushi/SusHi-1.5.0.tar.gz
    tar -zxvf SusHi-1.5.0.tar.gz
    cd SusHi-1.5.0
    ./configure

Edit the makefile, to link the proper 2HDMC version (1.7.0 here)

    make predef=2HDMC
    cd ..


## create repository where sushi cards will go
    
    mkdir Scan

## Run the test
    
    python example/test.py

