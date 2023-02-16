import sys
import os
sys.path.append('../CFG_GERAL/')
import VIDEOS_SEQUENCES as VD
import CPU_CQ_FTBE as CCF
from joblib import Parallel, delayed

HOME_PATH = '/'.join(os.path.realpath(__file__).split('/')[:-1])
initial_path = HOME_PATH + '/../1.DEC_ENC/'
final_path = '/video/coded_aom.av1'

#Primeira coisa, compilar o código C
old_decoder = sys.argv[1]
if old_decoder == "VP9":
	old_decoder_number = 1
elif old_decoder == "VP8":
	old_decoder_number = 2
elif old_decoder == "H264":
	old_decoder_number = 3
elif old_decoder == "H265":
	old_decoder_number = 4
elif old_decoder == "H266":
	old_decoder_number = 5

os.system("gcc main.c THESIS.c -lm -DTHESIS_PASS_CSV=1 -fcommon -DTHESIS_OLD_DECODER="+str(old_decoder_number))# -lpng -fsanitize=address")

#SINGLE CPU
for _, video_name, video_width, video_height, _, _, _, _, _ in VD.VIDEOS_LIST:
	for cq in CCF.CQ_LIST:
		in_path = initial_path + video_name + '/cq_' + str(cq) + final_path
		out_path = 'csv_' + video_name
		
		if(not os.path.exists(out_path)):
			os.system('mkdir ' + out_path)
		
		out_path = out_path + '/dataset_' + str(cq) + '.csv'
		
		full_command = "./a.out " + str(video_width) + ' ' + str(video_height) + ' ' + str(CCF.FTBE) + ' ' + in_path + ' ' + out_path
		#print(full_command)
		os.system(full_command)

#limpa os arquivos
from clean_csv import clean_csv_files as CLEANER
CLEANER()

