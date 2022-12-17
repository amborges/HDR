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
	['E', 'FountainSky_1920x1080p30_130f', 1920, 1080, 420, 8, 130, 30000, 1001],
	['E', 'Skater227_1920x1080_30fps', 1920, 1080, 420, 10, 300, 30, 1],
	['E', 'TimeLapseStreet_1920x1080p30_130f', 1920, 1080, 420, 8, 130, 30, 1],
	['E', 'Wheat_1920x1080', 1920, 1080, 420, 8, 300, 30000, 1001],
	['E', 'WorldCup_1920x1080_30p', 1920, 1080, 420, 8, 150, 30, 1],
	['E', 'WorldCup_far_1920x1080_30p', 1920, 1080, 420, 8, 150, 30, 1],
	['E', 'WorldCupFarSky_1920x1080_30p', 1920, 1080, 420, 8, 150, 30, 1]
]

