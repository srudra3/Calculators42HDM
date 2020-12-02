#!/bin/bash

DIR='cp3_llbb/Calculators42HDM'
set -x
# In a CMSSW release
if [[ ! -d "$DIR" ]]; then
    echo "reclone ..."
    git clone -o upstream git@github.com:cp3-llbb/Calculators42HDM.git $DIR
fi
scram b
cmsenv

echo "--> Building LHAPDF"
pushd $DIR
wget https://lhapdf.hepforge.org/downloads/?f=LHAPDF-6.3.0.tar.gz -O LHAPDF-6.3.0.tar.gz
## ^ or use a web browser to download, which will get the filename correct
tar xf LHAPDF-6.3.0.tar.gz
pushd LHAPDF-6.3.0
./configure #--prefix=/path/for/installation
make
make install
popd

echo "--> Building Higgs Bounds"
pushd $DIR
wget https://higgsbounds.hepforge.org/downloads?f=HiggsBounds-5.3.2beta.tar.gz -O HiggsBounds-5.3.2beta.tar.gz
tar -zxvf HiggsBounds-5.3.2beta.tar.gz
pushd HiggsBounds-5.3.2beta
./configure
make
popd

echo "--> Building Higgs Signals"
wget https://higgsbounds.hepforge.org/downloads?f=HiggsSignals-2.2.3beta.tar.gz -O HiggsSignals-2.2.3beta.tar.gz
tar -zxvf HiggsSignals-2.2.3beta.tar.gz
pushd HiggsSignals-2.2.3beta
./configure
make
popd

echo "--> Building 2HDMC"
pushd $DIR
wget http://www.hepforge.org/archive/2hdmc/2HDMC-1.8.0.tar.gz
tar -zxvf 2HDMC-1.8.0.tar.gz
pushd 2HDMC-1.8.0
make
popd

echo "--> Building SUSHI"
wget http://www.hepforge.org/archive/sushi/SusHi-1.7.0.tar.gz
tar -zxvf SusHi-1.7.0.tar.gz
pushd SusHi-1.7.0
./configure

## Edit the makefile, to link the proper 2HDMC version 
#sed -i -e 's|^HiggsBounds_DIR =.*$|HiggsBounds_DIR = ../HiggsBounds-5.3.2beta|' Makefile
#sed -i -e 's|^HiggsSignals_DIR =.*$|HiggsSignals_DIR = ../HiggsSignals-2.2.3beta|' Makefile
sed -i -e 's|^2HDMCPATH =.*$|2HDMCPATH = ../2HDMC-1.8.0|' Makefile
sed -i -e 's|^2HDMCVERSION =.*$|2HDMCVERSION = 1.8.0|' Makefile
make predef=2HDMC
popd

source first_setup.sh
pushd ${CMSSW_BASE}
set +x
