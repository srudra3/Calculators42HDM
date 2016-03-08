# Calculators For 2HDM
Tools to use SusHi and 2HDMC 


    module load /nfs/soft/modules/lhapdf/6.1
    export SCRAM_ARCH=slc6_amd64_gcc493
    cmsenv

First, intsallation of 2HDMC

    wget http://www.hepforge.org/archive/2hdmc/2HDMC-1.7.0.tar.gz
    cd 2HDMC-1.7.0
    make

Second, SusHi installation :

    wget http://www.hepforge.org/archive/sushi/SusHi-1.5.0.tar.gz
    tar -zxvf SusHi-1.5.0.tar.gz
    cd SusHi-1.5.0
    ./configure

Edit the makefile, to link the proper 2HDMC version (1.7.0 here)

    make predef=2HDMC


