import sys
sys.path.append('../CFG_GERAL/')
import VIDEOS_SEQUENCES_PREDICAO as VD
import os

import argparse

parser = argparse.ArgumentParser(description='movimenta pastas de lugar.')
parser.add_argument('path_folder', type=str,
                    help='nome da pasta para onde sera movido os dados')
args = parser.parse_args()

for row in VD.VIDEOS_LIST:
	os.system('mv ' + row[1] + ' ' + args.path_folder)
