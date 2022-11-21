import sys
sys.path.append('../CFG_GERAL/')
import VIDEOS_SEQUENCES as VD
import subprocess

for row in VD.VIDEOS_LIST:	
	subprocess.run('rm -rf ' + row[1], shell=True)
