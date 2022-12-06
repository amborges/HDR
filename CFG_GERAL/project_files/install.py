#!/usr/bin/env python3

import os
import glob

HOME_PATH = '/'.join(os.path.realpath(__file__).split('/')[:-3])
FILES_PATH = '/'.join(os.path.realpath(__file__).split('/')[:-1])

import sys
sys.path.append(HOME_PATH + '/CFG_GERAL')
import CPU_CQ_FTBE as CCF

#capturando o decodificador a ser utilizado
old_decoder = sys.argv[1]

if old_decoder == "VP9":
	decoder_path = 'libvpx--vp9'
elif old_decoder == "VP8":
	decoder_path = 'libvpx--vp8'
elif old_decoder == "H264":
	decoder_path = 'JM--'
elif old_decoder == "H265":
	decoder_path = 'HM--'



#copia os arquivos modificados para os locais corretos
all_cp = []
files = glob.glob(FILES_PATH+'/1.DEC_ENC/*')
for i in range(len(files)):
	if( ('aom--' in files[i]) or (decoder_path in files[i]) ):
		old_path = files[i]
		new_path = files[i].replace('CFG_GERAL/project_files/', '').replace('--', '/')
		cp_command = 'cp ' + old_path + ' ' + new_path
		all_cp.append(cp_command)

files = glob.glob(FILES_PATH+'/4.TRANSC/*')
for i in range(len(files)):
	if( ('aom_acc--' in files[i]) or (decoder_path in files[i]) ):
		old_path = files[i]
		new_path = files[i].replace('CFG_GERAL/project_files/', '').replace('--', '/')
		cp_command = 'cp ' + old_path + ' ' + new_path
		all_cp.append(cp_command)

import subprocess
for cmd in all_cp:
	subprocess.run(cmd, shell=True)
	
