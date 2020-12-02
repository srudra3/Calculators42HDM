# no shebang, source this
## Suggested env:
# conda create -n SusHi170 gsl gfortran_linux-64 gxx_linux-64 gcc_linux-64
# conda activate SusHi170
#
srcdir=$(dirname ${0})
echo "--> Building LHAPDF"
tar xzf "${srcdir}/LHAPDF-6.3.0.tar.gz"
pushd LHAPDF-6.3.0
./configure
make
popd
echo "--> Building 2HDMC"
tar xzf "${srcdir}/2HDMC-1.8.0.tar.gz"
#patch -p0 -i "${srcdir}/2HDMC_Makefile.patch" ## adds HiggsBounds and HiggsSignals
patch -p0 -i "${srcdir}/2HDMC_Makefile_conda.patch"
pushd 2HDMC-1.8.0/
make
popd
echo "--> Building SusHi"
tar xzf "${srcdir}/SusHi-1.7.0.tar.gz"
patch -p0 -i "${srcdir}/SusHi_Makefile_conda.patch"
pushd SusHi-1.7.0
export LDFLAGS="-L${CONDA_PREFIX}/lib"
./configure
make predef=2HDMC
popd
