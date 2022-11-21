import sys
sys.path.append('../CFG_GERAL/')
import VIDEOS_SEQUENCES as VD
import CPU_CQ_FTBE as CCF
import subprocess

for row in VD.VIDEOS_LIST:
	subprocess.run('rm -f ' + row[1] + '/vp9.csv', shell=True)
	subprocess.run('rm -f ' + row[1] + '/vp9_dec.y4m', shell=True)
	for cq in CCF.CQ_LIST:
		subprocess.run('rm -f ' + row[1] + '/av1_' + str(cq) + '.csv', shell=True)
