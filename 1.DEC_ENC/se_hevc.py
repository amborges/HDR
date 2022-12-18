import sys
import os
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Limpa arquivos CSV do decoder, caso for HEVC ou VVC')
parser.add_argument('who_path', type=str,
                    help='nome da pasta para onde sera feita a limpeza')
parser.add_argument('old_decoder', type=str,
                    help='nome da decodificador utilizado')
args = parser.parse_args()


sys.path.append('../CFG_GERAL/')

if(args.who_path == "1.DEC_ENC"):
	import VIDEOS_SEQUENCES as VD
else:
	import VIDEOS_PREDICAO as VD


if(args.old_decoder == "H265" or args.old_decoder == "H266"):
	HOME_PATH = '/'.join(os.path.realpath(__file__).split('/')[:-1])
	initial_path = HOME_PATH + '/../' + args.who_path + '/'
	for row in VD.VIDEOS_LIST:
		subprocess.run("sed -ni '/^[!1-9]/p' {}{}/old_decoder.csv".format(initial_path, row[1]), shell=True)
		print("cleaning {}{}/old_decoder.csv".format(initial_path, row[1]))
