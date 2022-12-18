#!/usr/bin/env python3

################################################################################
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
#       Script desenvolvido por Alex Borges, amborges@inf.ufpel.edu.br.        #
#                  Grupo de Pesquisa Video Technology Research Group -- ViTech #
#                                     Universidade Federal de Pelotas -- UFPel #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
# script de configuração compatível com o arquivo main.py versão 1.4           #
################################################################################
__COMPATIBLE_WITH_VERSION__ = 1.4


################################################################################
#                     ARQUIVO DE CONFIGURAÇÃO DEDICADO PARA O                  #
################################################################################
#                                                                              #
#                                                                              #
#                         #   #  #####  #        #  #####                      #
#                         #   #  #       #      #   #                          #
#                         #####  ###      #    #    #                          #
#                         #   #  #         #  #     #                          #
#                         #   #  #####      ##      #####                      #
#                                                                              #
#                                                                              #
################################################################################


 
################################################################################
###                            Configurações Gerais                          ###
### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -###
### Aqui tu prepara as condições das simulações que queres executar para os  ###
### teus experimentos. Apesar de estar preparado inicialmente para o HEVC,   ###
### com o software HM, modificações para outros codificadores é relativamente###
### simples. Basicamente é necessário modificar algumas pastas e nomes. Ao   ###
### longo deste arquivo, vou comentando algumas funcionalidades.             ###
################################################################################


#################################
## Ativação de Funcionalidades ##
#################################

#Precisa baixar o HM?
DOWNLOAD = False

#Se precisar que o download do HM seja regredido para alguma versão passada
#então modifique o texto abaixo para a versão requerida. Utilize somente os
#seis primeiros caracteres da versão, por exemplo 'HM-16.10+SCM-8.0'
DOWNGRADE_TO = 'HM-16.20'

#Precisa compilar o HM?
COMPILE  = False

#Quer realizar somente uma única simulação, para ver alguma coisa específica?
TESTE    = False

#É para executar de fato o experimento, com todas as simulações possíveis?
EXECUTE  = True

#É para calcular as métricas de codificação
METRICS = False

#É para gerar o gráfico da curva de BD-Rate?
PLOT = False

#Quer que mostre na tela o estado geral das simulações?
#Caso opte por False, o arquivo de log ainda será gerado.
VERBOSE = False

######################################
## Parâmetros Gerais das Simulações ##
######################################

import sys
sys.path.append('../CFG_GERAL/')
import CPU_CQ_FTBE as CCF
ALLOWED_CORES = CCF.CPU_LIST

#Lista de CQs a serem utilizados, deixe descomentado o que tu preferir
CQ_LIST = CCF.CQ_LIST


#Parâmetros extras que podem ser incluídos ao codificador. 
#Este é um atributo que permite criar várias simulações onde há apenas a inclusão
#de um ou mais parâmetros ao codificador, além daqueles parâmetros padrões que
#devem estar inclusos (que eu chamo de codificação âncora). Se tu deixar a lista
#vazia, então somente uma única simulação será realizada com aquele vídeo naquele 
#QP. Caso tu adicionar algo, então esse algo será uma simulação a mais que será 
#realizada. Cada nova variação de simulação será identificada nos arquivos de saída.
#POR FAVOR, lembre de adicionar um espaço entre as aspas e o parâmetro em si. Só 
#pra facilitar o meu trabalho durante o código. Sim, foi preguiça.
#Exemplos:
##EXTRA_PARAMS = [] # sem parâmetros extras, 1 conjunto de experimento
##EXTRA_PARAMS = [' --enable-rect-partitions=0'] # UM parâmetro extra, 2 conjuntos de experimentos
##EXTRA_PARAMS = [' --enable-rect-partitions=0', ' --min-partition-size=16 --max-partition-size=64'] # DOIS parâmetros, 3 conjuntos
EXTRA_PARAMS = []



############################
## Configuração do SCRIPT ##
############################

#Quantidade de quadros a ser executado (frames to be executed)
#Se deixar com valor negativo, então o vídeo inteiro será codificado
FTBE = CCF.FTBE

#Número máximo de núcleos que podem ser utilizados simultaneamente
#Em geral, se tu selecionou os cores disponíveis, é pq eles podem
#ser utilizados. Acaso tiveres alguma restrição, modificar aqui.
#O detalhe é que o computador não utilizará todos os núcleos
#anotados em ALLOWED_CORES
MAX_CORES = len(ALLOWED_CORES)

#nome do codificador. Se houver alguma mudança, mude aqui
CODEC_NAME = 'TAppDecoderStatic'

#tipo de extensão do vídeo. PREFERENCIALMENTE Y4M.
#MAS caso tu preferir utilizar YUV, modifique a função GENERATE_COMMAND
#para incluir as informações de altura, largura, bit-depth, subsample e fps.
VIDEO_EXTENSION = '.yuv'


##########################
## Definição das Pastas ##
##########################

#caminho da pasta de compilação do HM
#é de lá que ele vai compilar e manter os executáveis
#Caso houver mais de uma versão de HM, ir adicionando as pastas
# >>>
#>>>  ATENÇÃO: Todas devem estar na mesma pasta atual do projeto!!!!  <<<
# >>>
CODEC_PATHS = ['HM']



############################# [ [ [ A  T  E  N  Ç  Ã  O ] ] ] ########################################
#       Aqui se encontram funções que poderão sofrer mudanças. Deve-se alterar o que for preciso     #
#           para que a linha de comando seja adequada ao codificador que se está utilizando          #
######################################################################################################

#entradas vindas da classe LIST_OF_EXPERIMENTS, esses valores não são alteráveis.
#todos os valores são do tipo texto.
#   cq, valor de quantização (CQ ou QP)
#   folder, nome da pasta em que o experimento será executado
#   video_path, caminho completo do vídeo que será codificado
#   codec_path, caminho para o executável
#   home_path, caminho da pasta atual em que o script está executando
#   path_id, nome do executável
#   extra_param, parâmetros extras de execução, caso houver
#   width, largura do vídeo
#   height, altura do vídeo
#   subsample, subamostragem (444, 422, 420 etc)
#   bitdepth, profundidade de bits (esperado 8 ou 10)
#   num_frames, número de quadros que há no vídeo
#   frames_per_unit, número de frames por unidade de tempo do vídeo
#   unit_size, tamanho da unidade de tempo do vídeo em segundos
def GENERATE_COMMAND(cq, folder, video_path, codec_path, home_path, path_id, extra_param, width, height, subsample, bitdepth, num_frames, frames_per_unit, unit_size):
	#criando cada parte da linha de comando. Lembrar do espaçamento entre os parâmetros
	
	#comando completo
	#./vpxdec -o dec.y4m cod.hevc > file.csv
	
	hevc_decoder = codec_path + CODEC_NAME
	
	input_file  = home_path + '/../IN_BITSTREAMS/' + folder + '/cq_22/video/coded_HM.hevc'
	
	this_folder = home_path + '/' + folder + '/'
	
	output_file = this_folder + 'decoded_video.yuv'
	csv_file    = this_folder + 'old_decoder.csv'
	
	command = hevc_decoder + ' --BitstreamFile=' + input_file + ' --ReconFile=' + output_file + ' > ' + csv_file + ' &'
	
	output_filename = ''
	
	#retornando a linha de comando e o arquivo de saída
	return command, output_filename
	


#A seguinte função lê o arquivo de log e retorna os três valores relevantes de cada arquivo
#entrada, o nome do arquivo que se deseja ler
#saída, o PSNR-Y, o bitrate e o tempo de execução. Todas do tipo float
def get_psnr_bitrate_time(from_file):
	#abro o arquivo obtido do HM
	f = open(from_file)
	#preciso da última linha, mas tenho que passar por todo o arquivo
	#Os dados de bitrate e PSNR estão em algumas linhas antes do final do arquivo
	foundSummary = False
	interesting_line = 0
	
	for lst_line in f:
		if "SUMMARY" in lst_line:
			foundSummary = True
		if foundSummary:
			interesting_line += 1
			#Somente na terceira linha após o summary é que 
			#os dados de bitrate e psnr estão posicionados
			if(interesting_line == 3):
				interesting_line = lst_line
				foundSummary = False
		pass
	f.close()
	
	#Neste momento, eu tenho duas variáveis
	#interesting_line, cujos dados estão como
	#	        5    a    5327.2800   44.2158   47.1400   48.4901   44.8564
	#lst_line, cujos dados estão como
	# Total Time:       51.451 sec.
	
	#O tempo é mais fácil de se pegar.
	#primeiro crio um vetor com o texto
	lst_line = lst_line.split(' ')
	#depois removo elementos vazios desse vetor
	lst_line = list(filter(lambda a: len(a) > 0, lst_line))
	#Agora tenho o vetor abaixo, só me interessa o terceiro elemento
	#    ['Total', 'Time:', '51.451', 'sec.\n']
	#idx:   0        1         2         3
	time = float(lst_line[2])
	
	#O bitrate e o PSNR-Y, seguem uma lógica parecida. Separo e depois limpo
	interesting_line = interesting_line.split(' ')
	interesting_line = list(filter(lambda a: len(a) > 0, interesting_line))
	#O vetor abaixo é o que eu obtenho, me interessam os elementos 4 e 5
	#     ['\t', '5', 'a', '5327.2800', '44.2158', '47.1400', '48.4901', '44.8564', '\n']
	#idx:    0    1    2       3            4          5          6          7       8
	
	psnr_y = float(interesting_line[4])
	bitrate = float(interesting_line[3])
	
	return psnr_y, bitrate, time
	

import os
import urllib.request, urllib.error, urllib.parse
#Função que permite baixar o HM
def DO_DOWNLOAD(codec_path):
	if(os.path.exists(codec_path)):
		#se a pasta já existe, apagar tudo
		os.system('rm -rf ' + codec_path)
	
	#O caminho geral é sempre o mesmo
	url = 'https://hevc.hhi.fraunhofer.de/svn/svn_HEVCSoftware/tags/'
	
	#Tenho que pegar a versão daqui, senão dá erro
	#já que não posso atualizar uma variável global
	HM_VERSION = DOWNGRADE_TO
	#Identifica se o usuário deseja uma versão específica
	if HM_VERSION == '':
		#Em caso não quiser, então tenho que procurar a versão mais atualizada do HM
		
		#Baixo o conteúdo do index.html
		response = urllib.request.urlopen(url)
		webContent = response.read()
		
		#Crio um dicionário vazio para acumular todas as versões
		AllVersions = {}
		
		#Eu separo o conteúdo que me interessa e já removo a parte inicial do código html
		lines = webContent.split(b'<li><a href="')
		
		#Para cada linha das versões...
		for line in lines:
			#Faço um try, pois há linhas no html que não possuem a versão do HM
			try:
				#Aqui terei uma linha como essa: HM-1.0/">HM-1.0/</a></li>
				#Quero pegar somente o texto até o '/', E já aproveito para retirar o 'HM-'
				version = str(line).split('/')[0][5:]
				#Há um problema, a versão 16.20 é superior ao 16.3, mas se eu transformar
				#em float direto, isso não vai ser seguido. Portanto, preciso adicionar
				#um zero entre o ponto e o número, para transformar 16.3 em 16.03
				#Além disso, tenho que remover os '+RExt-1.0/' do número
				version_number = version.split('+')[0]
				integer_part = version_number.split('.')[0]
				decimal_part = version_number.split('.')[1]
				if(len(decimal_part) == 1):
					decimal_part = '0' + decimal_part
				#Aqui, eu junto as partes do número e converto em float
				float_version = float(integer_part + '.' + decimal_part)
				
				#Depois de tudo, eu adiciono as versões no dicionário
				#terei algo assim: '10.1+RExt-2.0': 10.01
				AllVersions.update({version: float_version})
			except:
				#Se der erro no código acima, OK, segue o baile
				continue
				
		
		#Depois de juntar todas as versões, organizo elas em ordem numérica
		AllVersions = dict(sorted(AllVersions.items(), key=lambda item: item[1]))
		
		#Para todos os fins, só me interessa a última versão
		#Já adiciono o HM- que removi anteriormente
		HM_VERSION = 'HM-' + list(AllVersions)[-1]
		
		
	command_line = 'svn checkout ' + url + HM_VERSION + '/'
	command_line += ' && mv ' + HM_VERSION + ' ' + CODEC_PATHS[0]
	
	#executa a linha de comando
	os.system(command_line)


import subprocess
#Função que compila o HM
#O código já adapta para possíveis versões diferentes de sistema operacional
def DO_COMPILE(os_version, codec_path):
	
	#OBSERVACAO:
	#o codec_path vai incluir uma pasta que não existe, chamada /bin
	#Por isso, sempre coloco um ../ depois de codec_path

	if(os.path.exists(codec_path)):
		#se a pasta já existe, apagar tudo pra deixar uma compilação limpa
		os.system('make -C ' + codec_path + '../build/linux clean')
		os.system('rm -rf ' + codec_path)
	
	#Eu preciso que a pasta /bin exista
	os.system('mkdir ' + codec_path)
	
	#Não sei se faz diferença, atualmente estou testando apenas no Ubuntu 18.04
	make_command = 'make -C ' + codec_path + '../build/linux all'
	
	if os_version > 18.04:
		#na versão 20.04 dá alerta de erro: -Werror=class-memaccess
		#solução é mandar adicionar a flag '-Wno-error=class-memaccess' em 
		#todos os lugares onde aparecer '-Werror'
		sed_command = "sed -i 's/-Werror/-Werror -Wno-error=class-memaccess/g' HM/build/linux/common/makefile.base"
		subprocess.call(sed_command, shell=True)
	
	os.system(make_command)
