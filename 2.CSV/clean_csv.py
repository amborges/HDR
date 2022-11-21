#função que recebe um dataframe e remove as linhas
#Basicamente, identifica-se qual decisão possui mais elementos
#Daí se reduz ele a fim de se obter 50%-50% dos exemplos, se possível
def remove_extra_elements(df):
	import numpy as np
	np.random.seed(42)
			
	dec_0 = df[df['decision'] == 0]['decision'].count() #nao split
	dec_1 = df[df['decision'] == 1]['decision'].count() #split
	
	valor_maior = 0
			
	#assumi que 0 tem mais, caso contrário, inverter
	if(dec_1 > dec_0):
		valor_maior = 1
		dec_0, dec_1 = dec_1, dec_0
	
	diff = dec_0 - dec_1
	
	if(diff > 0):
		#Se houver diferença, remover os dados extras
		try:
			#capturando a lista de index do caso de maior prevalencia
			lst_idx = list(df[df['decision'] == valor_maior].index)
			#seleciono randomicamente a quantidade de indexes extras
			lst_idx = np.random.choice(lst_idx, diff, replace=False)
			#finalmente, removo esses indexes extras
			df.drop(lst_idx, inplace=True)
			
			#reordenando randomicamente os dados
			df = df.sample(frac=1).reset_index(drop=True)
			
		except Exception as e:
			print("fail [", e, "]")
	
	return df


def prepara_csv(filename, is_training):
	
	for cq in [20, 32, 43, 55]:
	
		import pandas as pd	
		import numpy as np
		
		df = pd.read_csv(filename + '_' + str(cq) + '.csv')#, low_memory=False

		#preparando o dataset
		
		#removendo linhas duplicadas que dão resultados finais diferentes
		#colunas_menos_decisao = list(df.columns)[:-1]
		#df.drop_duplicates(subset=colunas_menos_decisao, inplace=True)

		#Tratando de valores NaN
		df.dropna(inplace=True)
		
		if(len(df.index) < 1):
			print("FALHA AO PROCESSAR O ARQUIVO ", filename, ": DATAFRAM VAZIO!")
			exit()
		
		#capturando dados de cada profundidade
		df_128 = df[df['curr_depth'] == 0].copy(deep=True)
		df_64  = df[df['curr_depth'] == 1].copy(deep=True)
		df_32  = df[df['curr_depth'] == 2].copy(deep=True)
		df_16  = df[df['curr_depth'] == 3].copy(deep=True)
		
		#limpando parte da memória
		del df
		
		#if(is_training):
			#deixar todos os dados com a mesma quantidade de SPLIT/NONSPLIT
		df_128 = remove_extra_elements(df_128)
		df_64  = remove_extra_elements(df_64)
		df_32  = remove_extra_elements(df_32)
		df_16  = remove_extra_elements(df_16)
			
		#eliminando coluna da profundidade e do CQ
		df_128.drop(columns=['curr_depth', 'curr_cq'], inplace=True)
		df_64.drop( columns=['curr_depth', 'curr_cq'], inplace=True)
		df_32.drop( columns=['curr_depth', 'curr_cq'], inplace=True)
		df_16.drop( columns=['curr_depth', 'curr_cq'], inplace=True)
		
		#convertendo todos os dados para o tipo int32
		df_128 = df_128.astype('float')
		df_64  = df_64.astype( 'float')
		df_32  = df_32.astype( 'float')
		df_16  = df_16.astype( 'float')
		
		#exportar os dados para arquivos
		df_128.to_csv('CSV/'+ filename + '_128_' + str(cq) + '_limpo.csv', index=False)
		df_64.to_csv( 'CSV/'+ filename + '_64_' + str(cq) + '_limpo.csv', index=False)
		df_32.to_csv( 'CSV/'+ filename + '_32_' + str(cq) + '_limpo.csv', index=False)
		df_16.to_csv( 'CSV/'+ filename + '_16_' + str(cq) + '_limpo.csv', index=False)
		
		#LIMPANDO MEMÒRIA
		
		import os
		os.remove(filename + '_' + str(cq) + '.csv')
		
		del df_128
		del df_64
		del df_32
		del df_16
		
		import gc
		gc.collect()



def concat_files(list_of_csv, filename):
	HEAD = 'curr_cq,curr_depth,Adpt,Absz,Aptp,Apmd,Ai_i,Bdpt,Bbsz,Bptp,Bpmd,Bi_i,Cdpt,Cbsz,Cptp,Cpmd,Ci_i,Ddpt,Dbsz,Dptp,Dpmd,Di_i,Edpt,Ebsz,Eptp,Epmd,Ei_i,decision\n'
	NUMBER_OF_COMMAS = HEAD.count(',')
	
	for cq in [20, 32, 43, 55]:
		this_filename = filename + '_' + str(cq) + '.csv'
		newfile = open(this_filename, 'w')
		newfile.write(HEAD)
		for csv_file in list_of_csv:
			search_for = 'dataset_'+str(cq)+'.csv'
			if(search_for in csv_file):
				import os
				if not os.path.exists(csv_file):
					print("Erro ao abrir o CSV", csv_file)
					continue
				
				with open(csv_file, "r") as a_file:
					for line in a_file:
						#previne linhas com falhas na inserção de '\n' no arquivo de origem
						if(line.count(",") == NUMBER_OF_COMMAS):
							newfile.write(line)
				
		newfile.close()
		
		#Corrigindo o arquivo final, caso houver algum tipo de erro
		lines_to_remove = []
		with open(this_filename) as a_file:
			current_line = 0
			for line in a_file:
				current_line += 1
				#previne linhas com falhas na inserção de '\n' no arquivo de origem
				if(line.count(",") != NUMBER_OF_COMMAS):
					lines_to_remove.append(current_line)
		
		#Para cada linha com erro, remover
		if(len(lines_to_remove) == 1):
			import os
			command = "sed -i '{}d' {}".format(lines_to_remove[0], this_filename)
			os.system(command)
		elif(len(lines_to_remove) > 1):
			import os
			for line in lines_to_remove.reverse():
				command = "sed -i '{}d {}".format(line, this_filename)
				os.system(command)
		
	

#__MAIN()__

def clean_csv_files():
	import sys
	sys.path.append('../CFG_GERAL/')

	import VIDEOS_TREINO    as VDtreino
	import VIDEOS_VALIDACAO as VDval
	import VIDEOS_TESTE     as VDteste
	import CPU_CQ_FTBE      as CCF

	CSV_for_training= [ ('csv_' + row_vd[1] + '/dataset_' + str(cq) + '.csv') 
		              for row_vd in VDtreino.VIDEOS_LIST
		              for cq in CCF.CQ_LIST ]
	CSV_for_validate= [ ('csv_' + row_vd[1] + '/dataset_' + str(cq) + '.csv') 
		              for row_vd in VDval.VIDEOS_LIST
		              for cq in CCF.CQ_LIST ]
	CSV_for_testing = [ ('csv_' + row_vd[1] + '/dataset_' + str(cq) + '.csv') 
		              for row_vd in VDteste.VIDEOS_LIST
		              for cq in CCF.CQ_LIST ]

	
	concat_files(CSV_for_training, 'training')
	prepara_csv('training', True)
	
	try:
		concat_files(CSV_for_validate, 'validation')
		prepara_csv('validation', False)
	except:
		print("Nao foi possível processar os arquivos CSVs do conjunto de validação.")
		import os
		os.system("rm -f validation_20.csv validation_32.csv validation_43.csv validation_55.csv")

	concat_files(CSV_for_testing, 'test')
	prepara_csv('test', False)

