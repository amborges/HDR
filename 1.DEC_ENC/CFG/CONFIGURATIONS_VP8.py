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
#                          #       #  #####  #####                             #
#                           #     #   #   #  #   #                             #
#                            #   #    #####  #####                             #
#                             # #     #          #                             #
#                              #      #      #####                             #
#                                                                              #
#                                                                              #
################################################################################


 
################################################################################
###                            Configurações Gerais                          ###
### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -###
### Aqui tu prepara as condições das simulações que queres executar para os  ###
### teus experimentos. Apesar de estar preparado inicialmente para o AV1,    ###
### com o software libaom, modificações para outros codificadores é          ###
### relativamente simples. Basicamente é necessário modificar algumas pastas ###
### e nomes. Ao longo deste arquivo, vou comentando algumas funcionalidades. ###
################################################################################


#################################
## Ativação de Funcionalidades ##
#################################

#Precisa baixar o libaom?
DOWNLOAD = False

#Se precisar que o download do libaom seja regredido para alguma versão passada
#então modifique o texto abaixo para a versão requerida. Utilize somente os
#seis primeiros caracteres da versão, por exemplo 'df1c60'
DOWNGRADE_TO = '52b3a0'

#Precisa compilar o libvpx?
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
#CQ. Caso tu adicionar algo, então esse algo será uma simulação a mais que será 
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
CODEC_NAME = 'vpxdec'

#tipo de extensão do vídeo. PREFERENCIALMENTE Y4M.
#MAS caso tu preferir utilizar YUV, modifique a função GENERATE_COMMAND
#para incluir as informações de altura, largura, bit-depth, subsample e fps.
VIDEO_EXTENSION = '.yuv'


##########################
## Definição das Pastas ##
##########################

#caminho da pasta de compilação do libvpx
#é de lá que ele vai compilar e manter os executáveis
#Caso houver mais de uma versão de libvpx, ir adicionando as pastas
# >>>
#>>>  ATENÇÃO: Todas devem estar na mesma pasta atual do projeto!!!!  <<<
# >>>
CODEC_PATHS = ['libvpx']


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
	#./vpxdec -o dec.y4m cod.vp8 > file.csv
	
	vp9_decoder = codec_path + CODEC_NAME
	
	input_file = home_path + '/../IN_BITSTREAMS/VP8/' + folder + '/cq_20/video/coded_libvpx.vp8'
	
	this_folder = home_path + '/' + folder + '/'
	
	output_file = this_folder + 'decoded_video.y4m'
	csv_file = this_folder + 'old_decoder.csv'
	
	command = vp9_decoder + ' -o ' + output_file + ' ' + input_file + ' > ' + csv_file + ' &'
	
	output_filename = ''
	print(command)
	#retornando a linha de comando e o arquivo de saída
	return command, output_filename
	

#A seguinte função lê o arquivo de log e retorna os três valores relevantes de cada arquivo
#entrada, o nome do arquivo que se deseja ler
#saída, o PSNR-Y, o bitrate e o tempo de execução. Todas do tipo float
def get_psnr_bitrate_time(from_file):
	#abro o arquivo obtido do libaom
	f = open(from_file)
	#preciso da última linha, mas tenho que passar por todo o arquivo
	lst_fst_line = ''
	lst_snd_line = ''
	for lst_line in f:
		lst_snd_line = lst_fst_line
		lst_fst_line = lst_line
		pass
	f.close()
	
	#TRATANDO A PENULTIMA LINHA
	#ex: Pass 2/2 frame    5/5      42316B   67705b/f 4058277b/s 1046549 us (4.78 fps)[K
	words = lst_snd_line.split(' ')
	#removo os indexes que não contêm palavras
	words = list(filter(lambda a: len(a) > 0, words))
	#idx - o que aparece
	#0 - Pass
	#1 - 2/2
	#2 - frame
	#3 - 5/5
	#4 - 42316B    
	#5 - 67705b/f
	#6 - 4058277b/s[<--- valor que me interessa]
	#7 - 1046549   [<--- valor que me interessa]
	#8 - us
	#9 - (4.78
	#10 - fps)[K
	
	bitrate = float(words[6][:-3]) / 1000 #removendo o b/s e convertendo de bps para kbps
	time = float(words[7]) / 1000 # convertendo de ms para seg
		
	#TRATANDO A ULTIMA LINHA
	#ex: Stream 0 PSNR (Overall/Avg/Y/U/V) 42.746 43.507 42.434 47.531 48.041
	
	#separo a linha em palavras
	words = lst_line.split(' ')
	#removo os indexes que não contêm palavras
	words = list(filter(lambda a: len(a) > 0, words))
	#idx = o que aparece
	#0 - Stream
	#1 - 0 
	#2 - PSNR 
	#3 - (Overall/Avg/Y/U/V) 
	#4 - 42.746 
	#5 - 43.507 
	#6 - 42.434   [<--- valor que me interessa]
	#7 - 47.531 
	#8 - 48.041
	
	#O que me interessa são o PSNR-Y (6), bitrate (9) e o tempo (11)
	psnr_y = float(words[6])
	return psnr_y, bitrate, time
	

import os
#Função que permite baixar o libaom
#pego somente o caminho do aom, sem o bin/
def DO_DOWNLOAD(codec_path):
	if(os.path.exists(codec_path)):
		#se a pasta já existe, apagar tudo
		os.system('rm -rf ' + codec_path)
	
	#faz download do libaom e coloca na pasta desejada
	git_command = 'git clone https://chromium.googlesource.com/webm/libvpx ' + codec_path
	
	#caso deseja fazer downgrade...
	if DOWNGRADE_TO != '':
		git_command += ' && cd ' + codec_path + ' && git reset --hard ' + DOWNGRADE_TO
	
	#executa o git
	os.system(git_command)


#Função que compila o libaom
#O código já adapta para possíveis versões diferentes de sistema operacional
def DO_COMPILE(os_version, codec_path):
	#se precisar compilar o libaom, então COMPILA
	if(os.path.exists(codec_path)):
		#se a pasta já existe, apagar tudo pra deixar uma compilação limpa
		os.system('rm -rf ' + codec_path)
	os.system('mkdir ' + codec_path)
	
	cmake_command = 'cd ' + codec_path + ' && ../configure'
	make_command = 'cd ' + codec_path + ' && make -j ' + str(len(ALLOWED_CORES))
	os.system(cmake_command)
	os.system(make_command)
