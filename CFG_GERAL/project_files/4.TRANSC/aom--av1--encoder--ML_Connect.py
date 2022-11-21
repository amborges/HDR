import numpy as np
import pandas as pd
import pickle
import os

global ML_MODEL

CABECALHO_ESPERADO = [#ZONA A - informações que estão na posição de referência no VP9
                      'Adpt', 'Absz', 'Aptp', 'Apmd', 'Ai_i',
                       
                      #ZONA B - informações que estão acima do bloco de referência no VP9
                      'Bdpt', 'Bbsz', 'Bptp', 'Bpmd', 'Bi_i',
                       
                      #ZONA C - informações que estão acima do bloco de referência no AV1 
                      'Cdpt', 'Cbsz', 'Cptp', 'Cpmd', 'Ci_i',
                       
                      #ZONA D - informações que estão a esquerda do bloco de referência no VP9 
                      'Ddpt', 'Dbsz', 'Dptp', 'Dpmd', 'Di_i',
                       
                      #ZONA E - informações que estão a esquerda do bloco de referência no AV1 
                      'Edpt', 'Ebsz', 'Eptp', 'Epmd', 'Ei_i'
                      
                     ]

def init_py(model_name):
	global ML_MODEL
	home_path = '/'.join(os.path.realpath(__file__).split('/')[:-5])
	model_path = home_path + '/OUT_RETORNA/P3/models/model_' + model_name
	
	ML_MODEL = []
	for depth in [128, 64, 32, 16]:
		ML_MODEL.append([
			pickle.load(open(model_path + '_' + str(depth) + '_20.bkp', 'rb')),
			pickle.load(open(model_path + '_' + str(depth) + '_32.bkp', 'rb')),
			pickle.load(open(model_path + '_' + str(depth) + '_43.bkp', 'rb')),
			pickle.load(open(model_path + '_' + str(depth) + '_55.bkp', 'rb')),
			])

def convert_string_to_int_or_none(s):
	try:
		a = int(s)
	except:
		a = None
	return a

def convert_string_to_float_or_none(s):
	try:
		a = float(s)
	except:
		a = None
	return a

def get_decision(depth, cq, attributes):
	#O depth aqui chega como 0 (128) à 3 (16)
	#O cq aqui chega como 0 (20) à 3 (55)
	global ML_MODEL
	
	try:
		#coloco esse -1 no final, pois a string vêm do C com uma vírgula a mais no fim
		arr = [convert_string_to_float_or_none(x) for x in attributes.split(',')[:-1]]
		NN = [None] * len(arr)
		df = pd.DataFrame([arr, NN], columns=CABECALHO_ESPERADO)
		df = df.dropna(axis=0)
		if not df.empty:
			#preciso colocar int, pois o modelo me retorna um valor float
			y_predict = int(ML_MODEL[depth][cq].predict(df)[0])
			y_probability = ML_MODEL[depth][cq].predict_proba(df)[0][y_predict]
			if(y_probability > 0.9):
				return y_predict
			else:
				return 2
	except Exception as err:
		print("machine_learning_decision ERRO:", err)
		return 2
