#!/usr/bin/env python3

import subprocess
import sys

def install_vp9(cores_list, num_of_cores):
	subprocess.run("cd 1.DEC_ENC/libvpx/bin && ../configure --enable-vp9-highbitdepth  && taskset -c {} make -j {}".format(cores_list, num_of_cores), shell=True)

def install_vp8(cores_list, num_of_cores):
	subprocess.run("cd 1.DEC_ENC/libvpx/bin && ../configure  && taskset -c {} make -j {}".format(cores_list, num_of_cores), shell=True)

def install_h264(cores_list, num_of_cores):
	subprocess.run("cd 1.DEC_ENC/JM && bash unixprep.sh && cd bin && make -C ../ clean && taskset -c {} make -j {} -C .. all".format(cores_list, num_of_cores), shell=True)
	
def install_h265(cores_list, num_of_cores):
	subprocess.call("sed -i 's/-Werror/-Wno-error=class-memaccess/g' 1.DEC_ENC/HM/build/linux/common/makefile.base", shell=True)
	subprocess.run("cd 1.DEC_ENC/HM/bin && make -C ../build/linux clean && taskset -c {} make -j {} -C ../build/linux all".format(cores_list, num_of_cores), shell=True)
	
	
	
	
#__MAIN__#
old_decoder  = sys.argv[1]
cores_list   = sys.argv[2]
num_of_cores = sys.argv[3]
try:
	if(old_decoder == "VP9"):
		install_vp9(cores_list, num_of_cores)
	elif (old_decoder == "VP8"):
		install_vp8(cores_list, num_of_cores)
	elif (old_decoder == "H264"):
		install_h264(cores_list, num_of_cores)
	elif (old_decoder == "H265"):
		install_h265(cores_list, num_of_cores)
except:
	print("ERRO GRAVE AO COMPILAR O SOFTWARE REFERÊNCIA REQUISITADO\n")
