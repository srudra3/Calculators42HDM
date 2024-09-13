#!/bin/bash

# Define paths
GSL_DIR="gsl-2.8"
GSL_LIB_DIR="$GSL_DIR/.libs"
GSL_CBLAS_LIB_DIR="$GSL_DIR/cblas/.libs"

# Update LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$GSL_CBLAS_LIB_DIR:$GSL_LIB_DIR:$LD_LIBRARY_PATH

# Create symbolic links if they don't exist
if [ ! -e "$GSL_LIB_DIR/libgslcblas.so" ]; then
    echo "Creating symbolic link for libgslcblas.so in $GSL_LIB_DIR"
    ln -s ../cblas/.libs/libgslcblas.so.0 $GSL_LIB_DIR/libgslcblas.so
fi

if [ ! -e "$GSL_LIB_DIR/libgsl.so.0" ]; then
    echo "Creating symbolic link for libgsl.so.0 in $GSL_LIB_DIR"
    ln -s libgsl.so.28 $GSL_LIB_DIR/libgsl.so.0
fi

# Verify symbolic links
echo "Checking symbolic links:"
ls -l $GSL_LIB_DIR/libgslcblas.so
ls -l $GSL_LIB_DIR/libgsl.so.0

# Verify library paths
echo "LD_LIBRARY_PATH is set to: $LD_LIBRARY_PATH"

# Optionally run the application or other commands
./2HDMC-1.8.0/CalcPhys 125 350 2000 2000 1.0 0 0 2000000.0 1.0 2
SusHi-1.7.0/bin/sushi mH_2000_mA_2100_tb_1p0_cba_0p99_mode_21.in Scan/NNPDF31_nnlo_as_0118_nf_4_mc_hessian/mH_2000_mA_2100_tb_1p0_cba_0p99_mode_21.out
