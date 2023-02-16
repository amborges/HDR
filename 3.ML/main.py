def export_figure(filename, y_pred, y_test, classes):
	#Mostrando a tabela verdade do modelo
	from sklearn.metrics import confusion_matrix
	cm = confusion_matrix(y_test, y_pred, labels=classes)

	#Mostrando a tabela verdade
	import matplotlib.pyplot as plt
	from sklearn.metrics import ConfusionMatrixDisplay
	disp = ConfusionMatrixDisplay(confusion_matrix=cm,
		                          display_labels=classes)
	disp.plot(cmap=plt.get_cmap('Oranges'))
	plt.savefig("img/cmatrix_" + filename + ".png")
	#plt.cla()
	plt.clf()
	#plt.close()

def export_metrics(filename, y_pred, y_test, classes, show_figure = False):
	metricas_filename = 'analise_modelos.csv'
	
	#Mostrando a acurácia
	import numpy as np
	from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score, confusion_matrix
	
	#captura os valores da matriz de confusão
	vn, fp, fn, vp = confusion_matrix(y_test, y_pred).ravel()
	
	#De acordo com as equações descritas na tese
	acc = (vn + vp) / (vn + fp + fn + vp) #acurácia
	pre = vp / (vp + fp)                  #precisão
	sen = vp / (vp + fn)                  #sensibilidade
	rec = vn / (vn + fp)                  #especificidade
	f1  = 2.0 * ((pre * sen) / (pre + sen))
	
	try:
		rocauc = roc_auc_score(y_test, y_pred, average=None, multi_class='ovo')
	except:
		rocauc = -0.0
	
	import os
	csv_file = open(metricas_filename, 'a')
	if os.path.getsize(metricas_filename) == 0:
		csv_file.write("modelo,f1,ROC_AUC,acuracia,precision,recall,sensibility\n")
	
	
	row_line = ','.join([filename, str(f1), str(rocauc), str(acc), str(pre), str(rec), str(sen)])
	csv_file.write(row_line+'\n')
	csv_file.close()
	
	if show_figure:
		export_figure(filename, y_pred, y_test, classes)
	

def ml_treino(model_attributes_list, csv_file, depth, cq):
	print("Treinando com o arquivo", csv_file, "no CQ", cq)
	import os
	if not os.path.exists(csv_file):
		print("Arquivo", csv_file, "ausente!")
		return
	
	import pandas as pd
	df = pd.read_csv(csv_file)
	
	if len(df.index) < 1:
		print("Arquivo", csv_file, "está vazio!")
		return
	
	#importando os dados do modelo CART
	CRITERION, SPLITTER, MAX_DEPTH, MIN_SAMPLES_SPLIT, MIN_SAMPLES_LEAF, MAX_FEATURES, MAX_LEAF_NODES, MIN_IMPURITY_DECREASE, CPP_ALPHA = model_attributes_list
	
	model_name = list_of_models.name_model(model_attributes_list)
	
	X_train, y_train = df.drop(["decision"], axis=1), df["decision"]
	
	model_saved = 'models/model_' + model_name + '_' + depth + '_' + cq + '.bkp'
	
	
	from sklearn.tree import DecisionTreeClassifier
		
	model = DecisionTreeClassifier(
		criterion                = CRITERION, 
		splitter                 = SPLITTER, 
		max_depth                = MAX_DEPTH, 
		min_samples_split        = MIN_SAMPLES_SPLIT, 
		min_samples_leaf         = MIN_SAMPLES_LEAF, 
		min_weight_fraction_leaf = 0.0, 
		max_features             = MAX_FEATURES, 
		random_state             = 42, 
		max_leaf_nodes           = MAX_LEAF_NODES, 
		min_impurity_decrease    = MIN_IMPURITY_DECREASE, 
		class_weight             = None, 
		ccp_alpha                = CPP_ALPHA
	)
	
	model.fit(X_train, y_train)
	
	import pickle
	pickle.dump(model, open(model_saved, 'wb'))

	

def ml_predict(model_attributes_list, csv_file, depth, cq):
	print("Predizendo o arquivo", csv_file, "no CQ", cq)
	try:
		import pandas as pd
		df = pd.read_csv(csv_file)
		df.dropna(inplace=True)
		if len(df.index) < 1:
			print("Arquivo", csv_file, "está vazio!")
			return
		
		model_name = list_of_models.name_model(model_attributes_list)

		model_saved = 'models/model_' + model_name + '_' + depth + '_' + cq + '.bkp'
		
		import os
		if not os.path.exists(model_saved):
			print("Modelo", model_name + '_' + depth + '_' + cq, "ausente!")
			return
		
		import pickle
		model = pickle.load(open(model_saved, 'rb'))
		
		X_test, y_test = df.drop(["decision"], axis=1), df["decision"]
		
		y_predict = model.predict(X_test)
		
		export_metrics(model_name + '_' + depth + '_' + cq,
				        y_predict,
				        y_test,
				        model.classes_,
					     False)
	except Exception as e:
		print()
		print("FALHA NO ARQUIVO", csv_file)
		print("PROBLEMA: ", str(e))
		print()

	
def test_hyperparams(csv_file, parallel_cores):
	import LIST_OF_CART_MODELS as list_of_models
	import numpy as np
	from sklearn.tree import DecisionTreeClassifier
	from sklearn.metrics import make_scorer, f1_score
	from sklearn.experimental import enable_halving_search_cv  # noqa
	from sklearn.model_selection import HalvingRandomSearchCV as HRandomSearch
	#https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.HalvingRandomSearchCV.html#sklearn.model_selection.HalvingRandomSearchCV
	#https://towardsdatascience.com/11-times-faster-hyperparameter-tuning-with-halvinggridsearch-232ed0160155
	
	
	import pandas as pd
	df = pd.read_csv(csv_file)
	
	df.dropna(inplace=True)
	if(len(df.index) <= 1):
		del df
		return None
	
	X_train, y_train = df.drop(["decision"], axis=1), df["decision"]
	number_of_cases = len(X_train)
	
	#criando o básico do modelo
	model = DecisionTreeClassifier(
		min_weight_fraction_leaf = 0.0, 
		random_state             = 42, 
		class_weight             = None
	)
		
	#importando os dados do modelo CART
	list_of_hyperparams = dict(
	                           criterion             = list_of_models.CRITERION,
	                           splitter              = list_of_models.SPLITTER,
	                           max_depth             = list_of_models.MAX_DEPTH,
	                           min_samples_split     = list_of_models.MIN_SAMPLES_SPLIT,
	                           min_samples_leaf      = list_of_models.MIN_SAMPLES_LEAF,
	                           max_features          = list_of_models.MAX_FEATURES,
	                           max_leaf_nodes        = list_of_models.MAX_LEAF_NODES,
	                           min_impurity_decrease = list_of_models.MIN_IMPURITY_DECREASE,
	                           ccp_alpha             = list_of_models.CPP_ALPHA
						)
	
	rndSearch = HRandomSearch(model, 
	                          list_of_hyperparams,
	                          max_resources=number_of_cases,
	                          min_resources=15,
	                          random_state=42,
	                          n_jobs=parallel_cores,
	                          factor=2,
	                          scoring='f1_macro',
	                          return_train_score=True,
	                          verbose=10)
	search = rndSearch.fit(X_train, y_train)
	
	#Exportando os valores das iterações
	df2 = pd.DataFrame(search.cv_results_)
	df2.drop(["mean_fit_time", "std_fit_time", "mean_score_time", "std_score_time", "params", "split0_test_score", 
	          "split1_test_score", "split2_test_score", "split3_test_score", "split4_test_score", "std_test_score",
	          "split0_train_score", "split1_train_score", "split2_train_score", "split3_train_score",
	          "split4_train_score", "std_train_score"], axis=1, inplace=True)
	          
	df2.sort_values('rank_test_score', inplace=True)
	log_file = csv_file.split('2.CSV')[0] + '3.ML/log/iter_of_' + csv_file.split('/')[-1]
	df2.to_csv(log_file, header=False)
	
	#limpando dados
	del df2
	del search
	del rndSearch
	del list_of_hyperparams
	del model
	del number_of_cases
	del X_train
	del y_train
	del df
	
	

def concat_combinations():
	#captura os caminhos atuais das pastas
	path = HOME_PATH + '/log/'
	TMP_FILE = 	HOME_PATH + '/tmp_best_hyperparams_combinations.csv'
	CSV_FILE = 	HOME_PATH + '/best_hyperparams_combinations.csv'
	
	#Novo cabeçalho dos csvs
	HEAD = "apaga1,apaga2,apaga3,splitter,min_samples_split,min_samples_leaf,min_impurity_decrease,max_leaf_nodes,max_features,max_depth,criterion,ccp_alpha,apaga4,apaga5,apaga6"

	import os
	import subprocess
	import pandas as pd
	
	#inserindo o cabeçalho no arquivo	
	bash_cmd = 'echo ' + HEAD + ' > ' + TMP_FILE
	subprocess.run(bash_cmd, shell=True)
	
	#Para cada arquivo csv, remover o cabeçalho original e capturando 20 linhas
	for filename in os.listdir(path):
		f = os.path.join(path, filename)
		if os.path.isfile(f):
			#bash_cmd = 'head -n 21 ' + f + ' | tail -n 20 >> ' + TMP_FILE
			bash_cmd = 'head -n 20 ' + f + ' >> ' + TMP_FILE
			subprocess.run(bash_cmd, shell=True)
			
	#importando o arquivo para limpar as colunas e linhas duplicadas
	df = pd.read_csv(TMP_FILE)
	df.drop(['apaga1','apaga2','apaga3','apaga4','apaga5','apaga6'], axis=1, inplace=True)
	df.drop_duplicates(inplace=True)
	#preenchendo valores NaN por texto 'None'
	df.fillna('None', inplace=True)
	df.to_csv(CSV_FILE, index=False)
	
	#apagando arquivo temporario
	bash_cmd = 'rm -f ' + TMP_FILE
	subprocess.run(bash_cmd, shell=True)
	


def training_and_testing(cores_free, files_to_train, files_to_test):
	import pandas as pd
	df = pd.read_csv(HOME_PATH + '/best_hyperparams_combinations.csv')
	models_list = df.values.tolist()

	the_model_list = []

	#Convertendo listas para tuple
	for s, mss, msl, mid, mln, mf, md, c, ca in models_list:
		#é preciso converter os tipos corretamente
		md  = None if md  == 'None' else int(float(md))
		mln = None if mln == 'None' else int(float(mln))
		
		mf  = None if mf  == 'None' else mf
		
		mid = float(mid)
		ca  = float(ca)
		
		mss = int(float(mss))
		msl = int(float(msl))

		the_tuple = (c, s, md, mss, msl, mf, mln, mid, ca)
		the_model_list.append(the_tuple)
	
	
	#Treina todos os modelos possíveis
	Parallel(n_jobs=cores_free)(
		 delayed(ml_treino)
		        (model_list_,
				 csv_file, 
				 depth,
				 cq
				)
		  for model_list_ in the_model_list
		  for csv_file, depth, cq in files_to_train
		 )

	#testa todos os modelos gerados
	Parallel(n_jobs=cores_free)(
		 delayed(ml_predict)
		        (model_list_,
				 csv_file, 
				 depth,
				 cq
				)
		  for model_list_ in the_model_list
		  for csv_file, depth, cq in files_to_test
		 )
	
	#Corrigindo o arquivo. As vezes o cabeçalho é repetido mais de uma vez no arquivo
	import subprocess
	bash_cmd = "sed '/modelo,f1,ROC_AUC,acuracia,precision,recall/d' -i analise_modelos.csv"
	subprocess.run(bash_cmd, shell=True)
	bash_cmd = "sed '1 i\modelo,f1,ROC_AUC,acuracia,precision,recall' -i analise_modelos.csv"
	subprocess.run(bash_cmd, shell=True)
	
	return the_model_list



def models_cup(models_list):
	import pandas as pd
	df = pd.read_csv(HOME_PATH + '/analise_modelos.csv')
	
	#Primeira coisa, encontrar todos os modelos que possuem um AUC 0.5 ou menor
	df.drop(df[df.ROC_AUC <= 0.75].index, inplace=True)
	
	#Segunda coisa, agrupar os elementos por modelo
	models_name = []
	for model_attributes_list in models_list:
		models_name.append(list_of_models.name_model(model_attributes_list))
	
	dict_columns_action = {'f1':'mean', 'ROC_AUC':'mean','acuracia':'size'}
	dict_columns_rename = {'f1':'f1_average', 'ROC_AUC':'ROC_AUC_average', 'acuracia':'submodels_count'}
	
	pattern = '|'.join(models_name)
	group_by_subtrings = df['modelo'].str.extract('('+ pattern + ')', expand=False)
	#Na linha de baixo faço 3 coisas
	#1. ordeno geral por nomes dos modelos
	#2. capturo alguns dados desse agrupamento
	#3. renomeio os nomes das colunas pra facilitar
	df1 = df.groupby(group_by_subtrings).agg(dict_columns_action).rename(columns=dict_columns_rename)
	
	#terceira coisa, remover os modelos que não possuem todos os 16 submodelos
	df1.drop(df1[df1.submodels_count < 16].index, inplace=True)
	
	#quarta coisa, não preciso mais dessa ultima coluna
	df1.drop('submodels_count', axis=1, inplace=True)
	
	#quarta coisa, ordeno por média de F1
	df1.sort_values('f1_average', ignore_index=True)
	
	df1.to_csv(HOME_PATH + '/winning_models.csv')



def csv_to_tuple(number_of_cases):
	import pandas as pd
	df = pd.read_csv(HOME_PATH + '/winning_models.csv')
	
	list_of_tuples = []
	
	#para cada quantidade a ser considerada, faça
	for n_o_c in range(number_of_cases):
		#capturo o modelo ganhador na posição n_o_c
		model = df.modelo[n_o_c]
		
		#converto o nome do modelo em hiperparametros
		model = model.split('_')
		c   = model[0][1:]
		s   = model[1][1:]
		md  = model[2][2:]
		mss = model[3][3:]
		msl = model[4][3:]
		mf  = model[5][2:]
		mln = model[6][3:]
		mid = model[7][3:]
		ca  = model[8][2:]
		
		#há hiperparametros que recebem None
		md  = 'None' if md  == 'N' else md
		mln = 'None' if mln == 'N' else mln
		
		#colocar aspas para os que são textos
		c = "'" + c + "'"
		s = "'" + s + "'"
		
		#o mf junta os dois casos acima
		mf  = 'None' if mf  == 'N' else "'" + mf + "'"
		
		
		#agora eu incluo numa lista
		list_of_tuples.append("(" + c + "," + s + "," + md + "," + mss + "," + msl + "," + mf + "," + mln + "," + mid + "," + ca + ")")
	
	f = open(HOME_PATH + '/LIST_OF_WIN_MODELS.py', 'w')
	f.write("def name_model(model_attributes_list):\n\t CRITERION, SPLITTER, MAX_DEPTH, MIN_SAMPLES_SPLIT, MIN_SAMPLES_LEAF, MAX_FEATURES, MAX_LEAF_NODES, MIN_IMPURITY_DECREASE, CPP_ALPHA = model_attributes_list\n\t \n\t #substituindo o None por N\n\t MAX_DEPTH      = 'N' if MAX_DEPTH      is None else str(MAX_DEPTH)\n\t MAX_FEATURES   = 'N' if MAX_FEATURES   is None else str(MAX_FEATURES)\n\t MAX_LEAF_NODES = 'N' if MAX_LEAF_NODES is None else str(MAX_LEAF_NODES)\n\t \n\t #Limitando tamanho máximo de valores float\n\t MIN_IMPURITY_DECREASE = '{:.2f}'.format(MIN_IMPURITY_DECREASE)\n\t CPP_ALPHA             = '{:.2f}'.format(CPP_ALPHA)\n\t \n\t #Transformando inteiros em texto\n\t MIN_SAMPLES_SPLIT = str(MIN_SAMPLES_SPLIT)\n\t MIN_SAMPLES_LEAF  = str(MIN_SAMPLES_LEAF)\n\t \t \n\t #Convertendo os valores em código-texto\n\t model_name = 'c{:s}_s{:s}_md{:s}_mss{:s}_msl{:s}_mf{:s}_mln{:s}_mid{:s}_ca{:s}'.format(\n\t \t CRITERION, \n\t \t SPLITTER,\n\t \t MAX_DEPTH, \n\t \t MIN_SAMPLES_SPLIT, \n\t \t MIN_SAMPLES_LEAF,\n\t \t MAX_FEATURES,\n\t \t MAX_LEAF_NODES,\n\t \t MIN_IMPURITY_DECREASE,\n\t \t CPP_ALPHA\n\t )\n\t return model_name\n\n")
	f.write("THIS_LIST = [")
	f.write(',\n'.join(list_of_tuples))
	f.write("]")
	f.close()





#__MAIN()__
import os
HOME_PATH = '/'.join(os.path.realpath(__file__).split('/')[:-1])
main_path = HOME_PATH + '/../2.CSV/CSV/'
depth_list = ['128', '64', '32', '16']
cq_list = ['20', '32', '43', '55']


import sys
sys.path.append('../CFG_GERAL/')
import CPU_CQ_FTBE as CCF
import LIST_OF_CART_MODELS as list_of_models
from joblib import Parallel, delayed


#Cria as pastas importantes, caso ainda não existam
import os
if(not os.path.exists('CSV')):
	os.system('mkdir CSV')

if(not os.path.exists('models')):
	os.system('mkdir models')

if(not os.path.exists('img')):
	os.system('mkdir img')

if(not os.path.exists('log')):
	os.system('mkdir log')

CSV_for_training= [ (main_path + 'training_' + depth + '_' + cq + '_limpo.csv', depth, cq) 
                  for depth in depth_list for cq in cq_list ]
CSV_for_validate= [ (main_path + 'validation_' + depth + '_' + cq + '_limpo.csv', depth, cq) 
                  for depth in depth_list for cq in cq_list ]
CSV_for_testing = [ (main_path + 'test_' + depth + '_' + cq + '_limpo.csv', depth, cq) 
                  for depth in depth_list for cq in cq_list ]




#Primeira fase: testa vários hiperparâmetros e gera um arquivo contendo o csv de todos testados, ordenado pelos melhores. Essa primeira fase considera cada arquivo de treinamento como um loop de teste
MAX_CORES = len(CCF.CPU_LIST)

for csv_file, depth, cq in CSV_for_training:
	test_hyperparams(csv_file, MAX_CORES)


#Segunda fase: Captura as combinações a serem consideradas pra valer. Basicamente, pega os arquivos gerados na primeira fase e importa os 20 primeiros de cada um. Depois remove-se os repetidos e armazena a lista de até 320 combinações em um arquivo novo.
concat_combinations()


#terceira fase: pega a lista dos melhores, e aplica o treinamento e o teste completo para todos os casos
#Há como retorno, os modelos testados
models_list = training_and_testing(len(CCF.CPU_LIST), CSV_for_training, CSV_for_testing)

#quarta fase: pega o arquivo com o resultado de todos os testes, agrupa eles e faz a média, retornando os 3 primeiros lugares
models_cup(models_list)

#quinta fase: converto o csv de vencedores para uma tupla de N possibilidades
csv_to_tuple(1)
