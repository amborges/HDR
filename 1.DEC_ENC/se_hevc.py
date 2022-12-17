import sys
import os
import subprocess
import argparse

sys.path.append('../CFG_GERAL/')
import VIDEOS_SEQUENCES as VD

parser = argparse.ArgumentParser(description='Limpa arquivos CSV do decoder, caso for HEVC')
parser.add_argument('who_path', type=str,
                    help='nome da pasta para onde sera feita a limpeza')
args = parser.parse_args()

HOME_PATH = '/'.join(os.path.realpath(__file__).split('/')[:-1])
initial_path = HOME_PATH + '/../' + args.who_path + '/'

for row in VD.VIDEOS_LIST:
	subprocess.run("sed -ni '/^[!1-9]/p' {}/{}/old_decoder.csv".format(HOME_PATH, row[1]), shell=True)
	#print("{}/{}/old_decoder.csv".format(HOME_PATH, row[1]))
