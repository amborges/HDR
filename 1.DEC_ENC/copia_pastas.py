import sys
sys.path.append('../CFG_GERAL/')
import VIDEOS_SEQUENCES as VD
import os

import argparse

parser = argparse.ArgumentParser(description='movimenta pastas de lugar.')
parser.add_argument('path_folder', type=str,
                    help='nome da pasta para onde sera movido os dados')
args = parser.parse_args()

HOME_PATH = '/'.join(os.path.realpath(__file__).split('/')[:-1])

for row in VD.VIDEOS_LIST:
	action = 'mv ' + HOME_PATH + '/' + row[1] + '/ ' + args.path_folder
	os.system(action)
