import os

import argparse

parser = argparse.ArgumentParser(description='movimenta pastas de lugar.')
parser.add_argument('path_folder', type=str,
                    help='nome da pasta para onde sera movido os dados')
args = parser.parse_args()

for infile in ['../CFG_GERAL/VIDEOS_SEQUENCES.py', '../CFG_GERAL/VIDEOS_TESTE.py', '../CFG_GERAL/VIDEOS_VALIDACAO.py', '../CFG_GERAL/VIDEOS_TREINO.py']:
	fori = open(infile, 'r')
	ftmp = open('tmp', 'w')
	check = False

	for line in fori:
		if not check and 'VIDEO_HOME_PATH' in line:
			tmp = "VIDEO_HOME_PATH = '" + args.path_folder + "'\n"
			check = True
		else:
			tmp = line
		ftmp.write(tmp)
	ftmp.close()
	fori.close()

	os.system('rm ' + infile)
	os.system('mv tmp ' + infile)
