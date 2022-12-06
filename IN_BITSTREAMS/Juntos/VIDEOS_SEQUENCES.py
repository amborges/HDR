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

VIDEO_HOME_PATH = '/home/pc-einstein/Documents/Alex/'

#caminhos das pastas dos vídeos separados por resolução
VIDEOS_PATH = {
	'A': VIDEO_HOME_PATH + 'class_A/',
	'B': VIDEO_HOME_PATH + 'class_B/',
	'C': VIDEO_HOME_PATH + 'class_C/',
	'D': VIDEO_HOME_PATH + 'class_D/',
	'E': VIDEO_HOME_PATH + 'class_E/',
	'F': VIDEO_HOME_PATH + 'class_F/',
	'G': VIDEO_HOME_PATH + 'class_G/',
	'H': VIDEO_HOME_PATH + 'class_H/',
	'I': VIDEO_HOME_PATH + 'class_I/'
}

#Lista de vídeos a serem utilizados
#Cada linha é composta por uma resolução (vide acima) e o nome do vídeo
#Também incluí o SI-TI do vídeo, e marquei aqueles que eu considerdo
#recomendados para os nossos experimentos no ViTech.
#Descomente os vídeos que queres utilizar
#Cada linha é composta pelos seguintes elementos
# [ CLASSE, NOME DO VÍDEO, LARGURA, ALTURA, SUBAMOSTRAGEM, PROFUNDIDADE DE BITS, NUMERO DE QUADROS, FRAMES PER UNIT, UNIT SIZE]
VIDEOS_LIST = [
	['C', 'boat_hdr_amazon_720p', 1280, 720, 420, 10, 60, 24000, 1001],
	['C', 'dark720p_120f', 1280, 720, 420, 8, 120, 30, 1],
	['C', 'FourPeople_1280x720_60_120f', 1280, 720, 420, 8, 120, 60, 1],
	['C', 'gipsrestat720p_120f', 1280, 720, 420, 8, 120, 50, 1],
	['C', 'Johnny_1280x720_60_120f', 1280, 720, 420, 8, 120, 60, 1],
	['C', 'KristenAndSara_1280x720_60_120f', 1280, 720, 420, 8, 120, 60, 1],
	['C', 'Netflix_DinnerScene_1280x720_60fps_8bit_420_120f', 1280, 720, 420, 8, 120, 60, 1],
	['C', 'Netflix_DrivingPOV_1280x720_60fps_8bit_420_120f', 1280, 720, 420, 8, 120, 60, 1],
	['C', 'Netflix_FoodMarket2_1280x720_60fps_8bit_420_120f', 1280, 720, 420, 8, 120, 60, 1],
	['C', 'Netflix_RollerCoaster_1280x720_60fps_8bit_420_120f', 1280, 720, 420, 8, 120, 60, 1],
	['C', 'Netflix_Tango_1280x720_60fps_8bit_420_120f', 1280, 720, 420, 8, 120, 60, 1],
	['C', 'rain_hdr_amazon_720p', 1280, 720, 420, 10, 60, 24000, 1001],
	['C', 'vidyo1_720p_60fps_120f', 1280, 720, 420, 8, 120, 60, 1],
	['C', 'vidyo3_720p_60fps_120f', 1280, 720, 420, 8, 120, 60, 1],
	['C', 'vidyo4_720p_60fps_120f', 1280, 720, 420, 8, 120, 60, 1],

	['C', 'FourPeople_1280x720_60', 1280, 720, 420, 8, 600, 60, 1],
	['C', 'Johnny_1280x720_60', 1280, 720, 420, 8, 600, 60, 1],
	['C', 'Vidyo1_1280x720_60', 1280, 720, 420, 8, 600, 60, 1],
	['C', 'KristenAndSara_1280x720_60', 1280, 720, 420, 8, 600, 60, 1],
	['C', 'Vidyo3_1280x720_60', 1280, 720, 420, 8, 600, 60, 1],
	['C', 'Vidyo4_1280x720_60', 1280, 720, 420, 8, 600, 60, 1]
]

