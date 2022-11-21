#!/usr/bin/env python3

################################################################################
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
#       Script desenvolvido por Alex Borges, amborges@inf.ufpel.edu.br.        #
#                  Grupo de Pesquisa Video Technology Research Group -- ViTech #
#                                     Universidade Federal de Pelotas -- UFPel #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
################################################################################



################################################################################
#               ARQUIVO DE CONFIGURAÇÃO DEDICADO PARA A LISTA DE               #
################################################################################
#                                                                              #
#                                                                              #
#                 #        # ##### ###    ##### ##### #####                    #
#                  #      #    #   #  ##  #     #   # #                        #
#                   #    #     #   #    # ###   #   # #####                    #
#                    #  #      #   #  ##  #     #   #     #                    #
#                     ##     ##### ###    ##### ##### #####                    #
#                                                                              #
#                                                                              #
################################################################################


 
################################################################################
###                            Configurações Gerais                          ###
### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -###
### Aqui estão a lista dos vídeos que serão utilizados peo main.py           ###
### Deversão estar aqui o nome dos vídeos e a localização deles.             ###
### Apenas comente os vídeos que não pretende utilizar na execução dos       ###
### experimentos. Caso for utilizar uma lista diferente, crie uma nova a     ###
### vontade, mas seguindo a mesma estrutura da lista abaixo.                 ###
################################################################################


##########################
## Definição das Pastas ##
##########################

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

#Lista de vídeos a serem utilizados
#Cada linha é composta por uma resolução (vide acima) e o nome do vídeo
#Também incluí o SI-TI do vídeo, e marquei aqueles que eu considerdo
#recomendados para os nossos experimentos no ViTech.
#Descomente os vídeos que queres utilizar
#Cada linha é composta pelos seguintes elementos
# [ CLASSE, NOME DO VÍDEO, LARGURA, ALTURA, SUBAMOSTRAGEM, PROFUNDIDADE DE BITS, NUMERO DE QUADROS, FRAMES PER UNIT, UNIT SIZE]
VIDEOS_LIST = [
#	['A', 'grandma_qcif', 176, 144, 420, 8, 870, 24, 1],
#	['A', 'highway_qcif', 176, 144, 420, 8, 2000, 24, 1],
#	['A', 'claire_qcif', 176, 144, 420, 8, 495, 24, 1],
	
	
#	['B', 'niklas360p_120f', 640, 360, 420, 8, 120, 30, 1],
#	['B', 'rain2_hdr_amazon_360p', 640, 360, 420, 10, 60, 24000, 1001],
#	['B', 'stockholm_640x360_120f', 640, 360, 420, 8, 120, 60000, 1001],
	

#	['C', 'KristenAndSara_1280x720_60_120f', 1280, 720, 420, 8, 120, 60, 1],
#	['C', 'Netflix_FoodMarket2_1280x720_60fps_8bit_420_120f', 1280, 720, 420, 8, 120, 60, 1],
#	['C', 'Vidyo4_1280x720_60', 1280, 720, 420, 8, 600, 60, 1],

	
#	['E', 'crowd_run_1080p50_60f', 1920, 1080, 420, 8, 60, 50, 1],
#	['E', 'guitar_hdr_amazon_1080p', 1920, 1080, 420, 10, 60, 24000, 1001],
#	['E', 'Netflix_SquareAndTimelapse_1920x1080_60fps_8bit_420_60f', 1920, 1080, 420, 8, 60, 60, 1],
#	['E', 'pan_hdr_amazon_1080p', 1920, 1080, 420, 10, 60, 24000, 1],
#	['E', 'touchdown_pass_1080p_60f', 1920, 1080, 420, 8, 60, 30000, 1001],
	

#	['F', 'life_1080p30_60f', 1920, 1080, 420, 8, 60, 30, 1],
	
	
#	['H', 'Netflix_ToddlerFountain_4096x2160_60fps_10bit_420_60f', 4096, 2160, 420, 10, 60, 60, 1],
#	['H', 'meridian_aom_sdr_12264-12745', 3840, 2160, 420, 10, 482, 60000, 1001],
#	['H', 'meridian_aom_sdr_15932-16309', 3840, 2160, 420, 10, 378, 60000, 1001],
#	['H', 'Netflix_Tango_4096x2160_60fps_10bit_420', 4096, 2160, 420, 10, 295, 60, 1],
#	['H', 'nocturne_aom_sdr_23820-24322', 3840, 2160, 420, 10, 503, 60000, 1001]
	
]


#########
# REMOVIDO POR LEVAR MAIS QUE 15 DIAS
#########
#['H', 'Beauty_3840x2160_120fps_420_10bit_YUV', 3840, 2160, 420, 10, 600, 120, 1],
#['H', 'Bosphorus_3840x2160_120fps_420_10bit_YUV', 3840, 2160, 420, 10, 600, 120, 1],
#['H', 'Lips_3840x2160_120fps_10bit', 3840, 2160, 420, 10, 600, 120, 1],
#['H', 'ShakeNDry_3840x2160_120fps_420_10bit_YUV', 3840, 2160, 420, 10, 300, 120, 1],
#['H', 'YachtRide_3840x2160_120fps_420_10bit_YUV', 3840, 2160, 420, 10, 600, 120, 1]
#['I', 'cosmos_aom_sdr_13446-13649', 4096, 2160, 420, 10, 203, 24, 1],
#['I', 'cosmos_aom_sdr_1573-1749', 4096, 2160, 420, 10, 177, 24, 1],
#['I', 'cosmos_aom_sdr_8686-8826', 4096, 2160, 420, 10, 140, 24, 1],
	
