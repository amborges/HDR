#!/usr/bin/env python3


VIDEO_HOME_PATH = '/home/alex/Documents/TESE/TESE_app/IN_BITSTREAMS'
VIDEOS_PATH = {
	'A': VIDEO_HOME_PATH + 'Class_A/',
	'B': VIDEO_HOME_PATH + 'Class_B/',
	'C': VIDEO_HOME_PATH + 'Class_C/',
	'D': VIDEO_HOME_PATH + 'Class_D/',
	'E': VIDEO_HOME_PATH + 'Class_E/',
	'F': VIDEO_HOME_PATH + 'Class_F/',
	'G': VIDEO_HOME_PATH + 'Class_G/',
	'H': VIDEO_HOME_PATH + 'Class_H/',
	'I': VIDEO_HOME_PATH + 'Class_I/'
}

VIDEOS_LIST = []

import VIDEOS_TREINO as VD
for row in VD.VIDEOS_LIST:
	VIDEOS_LIST.append(row)

import VIDEOS_VALIDACAO as VD2
for row in VD2.VIDEOS_LIST:
	VIDEOS_LIST.append(row)
	
import VIDEOS_TESTE as VD3
for row in VD3.VIDEOS_LIST:
	VIDEOS_LIST.append(row)

