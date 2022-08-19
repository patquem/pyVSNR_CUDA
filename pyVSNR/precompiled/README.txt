.dll obtained from compilation on a PC Windows-64 bits, with the following commands:
>> cd pyVSNR
>> nvcc -o ../precompiled/libvsnr2d.dll -L cufftw.lib cufft.lib cublas.lib --shared vsnr2d.cu
