the .dll in the 'precompiled' folder was compiled with:
>> nvcc -o ../precompiled/libvsnr2d.dll --shared vsnr2d.cu

If there is a problem during CUDA execution (typically 'access memory error'),
it may be necessary to recompile the .dll on your platform and replace the one
located in ../precompiled/

Compilation may ask for a 'cl.exe'.
In case the compiler fails to find its associated path, use the -ccbin argument
Example (to be adapted):
>> nvcc -o libvsnr2d.dll --shared vsnr2d.cu -ccbin "C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC\Tools\MSVC\14.21.27702\bin\Hostx64\x64\cl.exe"   

