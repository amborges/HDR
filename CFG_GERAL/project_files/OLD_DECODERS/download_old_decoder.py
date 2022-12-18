#!/usr/bin/env python3

import subprocess
import sys

def download_vp9():
	subprocess.run("git clone https://chromium.googlesource.com/webm/libvpx && cd libvpx && git reset --hard 52b3a0 && mkdir bin", shell=True)
	subprocess.run("mv libvpx 1.DEC_ENC", shell=True)

def download_h264():
	subprocess.run("wget http://iphome.hhi.de/suehring/tml/download/jm19.0.zip && unzip jm19.0.zip && rm -f jm19.0.zip", shell=True)
	subprocess.run("mv JM 1.DEC_ENC", shell=True)
	
def download_h265():
	subprocess.run("svn checkout https://hevc.hhi.fraunhofer.de/svn/svn_HEVCSoftware/tags/HM-16.20/ && mkdir HM-16.20/bin", shell=True)
	subprocess.run("mv HM-16.20 1.DEC_ENC/HM", shell=True)

def download_h266():
	subprocess.run("git clone https://vcgit.hhi.fraunhofer.de/jvet/VVCSoftware_VTM && cd VVCSoftware_VTM && git reset --hard c71f7a9e && mkdir bin", shell=True)
	subprocess.run("mv VVCSoftware_VTM 1.DEC_ENC/VTM", shell=True)



#__MAIN__
old_decoder = sys.argv[1]
try:
	if(old_decoder == "VP9"):
		download_vp9()
	elif (old_decoder == "VP8"):
		download_vp9()
	elif (old_decoder == "H264"):
		download_h264()
	elif (old_decoder == "H265"):
		download_h265()
	elif (old_decoder == "H266"):
		download_h266()
except:
	print("ERRO GRAVE AO BAIXAR O SOFTWARE REFERÊNCIA REQUISITADO\n")
