#Captura os núcleos disponíveis para uso por esse script
CPU_CONTENT = $(shell cat 'CFG_GERAL/CPU_CQ_FTBE.py')
SUBSTRING=$(shell echo $(CPU_CONTENT) | cut -d'[' -f 2)
SUBSTRING2=$(shell echo $(SUBSTRING) | cut -d']' -f 1)


########################################################################
#Variáveis utilizados por esse script

#Lista de núcleos
CPU_LIST=$(shell echo $(SUBSTRING2) | sed 's/ //g')
NUM_OF_CPU=$(shell echo "$(CPU_LIST)," | grep -o ',' | wc -l)
#Pasta dos resultados
THIS_PATH    = $(shell pwd)
RETORNA_PARA = $(THIS_PATH)/OUT_RETORNA
BITSTREAMS   = $(THIS_PATH)/IN_BITSTREAMS

PYDOWNLOAD = python3 CFG_GERAL/project_files/OLD_DECODERS/download_old_decoder.py
PYINSTALL  = python3 CFG_GERAL/project_files/OLD_DECODERS/install_old_decoder.py

########################################################################	

#Qual dos decodificadores abaixo é para utilizar?
#OLD_DECODER = "VP9"
#OLD_DECODER = "VP8"
OLD_DECODER = "H264"
#OLD_DECODER = "H265"
#OLD_DECODER = "H266"


verifica:
	@echo $(CPU_LIST)
	@echo $(NUM_OF_CPU)

#Executa todos os passos
all:
	$(MAKE) primeiro_passo
	$(MAKE) segundo_passo
	$(MAKE) terceiro_passo
	$(MAKE) quarto_passo
	$(MAKE) quinto_passo
	$(MAKE) sexto_passo
	$(MAKE) setimo_passo
	$(MAKE) oitavo_passo
	$(MAKE) nono_passo

processa_hevc_csv2:
ifeq ($(OLD_DECODER), H265)
	cd 1.DEC_ENC && python3 se_hevc.py $(WHO)
endif

#atualiza o caminho das sequencias de videos codificadas com VP9	
#instala VP9 e decodifica os arquivos VP9 e gera o csv-vp9
primeiro_passo:
	cd 1.DEC_ENC && python3 atualiza_sequencias.py $(BITSTREAMS)
	cd 1.DEC_ENC && python3 main.py $(OLD_DECODER)


#instala AV1 e codifica os videos para AV1
segundo_passo:
	$(MAKE) processa_hevc_csv2 WHO=1.DEC_ENC
	cd 1.DEC_ENC && python3 main2.py $(OLD_DECODER)


#converte os arquivos csv brutos para o csv treinável
terceiro_passo:
	cd 2.CSV && taskset -c $(CPU_LIST) python3 main.py $(OLD_DECODER)


#split csv treinavel, limpa dados, treina e testa
quarto_passo:
	cd 3.ML && taskset -c $(CPU_LIST) python3 main.py


#limpa arquivos e copia todos os dados relevantes para a pasta que vai ser recuperavel
quinto_passo:
	#cd 1.DEC_ENC && python3 limpa_csv.py
	#cd 1.DEC_ENC && python3 copia_pastas.py $(RETORNA_PARA)/P1/
	cd 2.CSV && rm -rf csv_*
	cd 3.ML/CSV && rm -rf *.csv
	mv 3.ML/img $(RETORNA_PARA)/P3/
	mv 3.ML/models $(RETORNA_PARA)/P3/
	mv 3.ML/analise_modelos.csv $(RETORNA_PARA)/P3/


#decodifica videos novos no formato VP9
sexto_passo:
	cd 4.TRANSC && python3 main.py $(OLD_DECODER)

	
#codifica os videos AV1 sem modificação
setimo_passo:
	cd 4.TRANSC && python3 main2.py $(OLD_DECODER)


#codifica os videos AV1 sob vários modelos de ML
oitavo_passo:
	$(MAKE) processa_hevc_csv2 WHO=4.TRANSC
	cd 4.TRANSC && python3 main3.py $(OLD_DECODER)


#captura os valores do passo anterior para a pasta que vai ser recuperavel
nono_passo:
	cd 4.TRANSC && python3 copia_pastas.py $(RETORNA_PARA)/P4/


#limpa tudo para recomeçar do zero
clean:
	#PASTA 1
	cd 1.DEC_ENC && python3 limpa_tudo.py
	rm -rf 1.DEC_ENC/CFG/__pycache__
	rm -f 1.DEC_ENC/backup.json
	rm -f 1.DEC_ENC/script_log.log
	rm -rf 1.DEC_ENC/aom
	rm -rf 1.DEC_ENC/libvpx
	rm -rf 1.DEC_ENC/JM
	rm -rf 1.DEC_ENC/HM
	#PASTA2
	rm -rf 2.CSV/csv_*
	rm -rf 2.CSV/__pycache__
	#PASTA 3
	rm -rf 3.ML/CSV
	rm -rf 3.ML/img
	rm -rf 3.ML/models
	rm -rf 3.ML/log
	rm -f  3.ML/analise_modelos.csv
	rm -rf 3.ML/best_hyperparams_combinations.csv
	rm -rf 3.ML/LIST_OF_WIN_MODELS.py
	rm -rf 3.ML/winning_models.csv
	rm -rf 3.ML/__pycache__
	#PASTA 4
	rm -rf 4.TRANSC/CFG/__pycache__
	rm -f 4.TRANSC/backup.json
	rm -f 4.TRANSC/script_log.log
	rm -rf 4.TRANSC/aom
	rm -rf 4.TRANSC/aom_acc
	#PASTAS GERAIS
	rm -rf CFG_GERAL/__pycache__
	rm -rf $(RETORNA_PARA)/P1/*
	rm -rf $(RETORNA_PARA)/P3/*
	rm -f $(RETORNA_PARA)/analise_modelos.csv

	
prepara:
	#baixa o software do decodificador
	$(PYDOWNLOAD) $(OLD_DECODER)
	
	#baixa e prepara o libaom
	cd 1.DEC_ENC && git clone https://aomedia.googlesource.com/aom && cd aom && git reset --hard 9a83c6
	mkdir 1.DEC_ENC/aom/bin
	cp -r 1.DEC_ENC/aom 4.TRANSC/aom
	cp -r 1.DEC_ENC/aom 4.TRANSC/aom_acc
	
	#copia os arquivos necessários para cada projeto
	cd CFG_GERAL/project_files && python3 install.py $(OLD_DECODER)
	cp 2.CSV/THESIS.h 1.DEC_ENC/aom/av1/encoder/THESIS.h
	cp 2.CSV/THESIS.c 1.DEC_ENC/aom/av1/encoder/THESIS.c
	cp 2.CSV/THESIS.h 4.TRANSC/aom_acc/av1/encoder/THESIS.h
	cp 2.CSV/THESIS.c 4.TRANSC/aom_acc/av1/encoder/THESIS.c
	
	#Compilando o software do decodificador
	$(PYINSTALL)  $(OLD_DECODER) $(CPU_LIST) $(NUM_OF_CPU)
	
	#compila o libaom passo 1
	cd 1.DEC_ENC/aom/bin && cmake -DTHESIS_OLD_DECODER=$(OLD_DECODER) -DTHESIS_PASS_DEC_ENC=1 -DAOM_TARGET_CPU=generic .. && taskset -c $(CPU_LIST) make -j $(NUM_OF_CPU)
	
	#compila o libaom passo 4 original
	cd 4.TRANSC/aom/bin && cmake -DAOM_TARGET_CPU=generic .. && taskset -c $(CPU_LIST) make -j $(NUM_OF_CPU)
	
	#compila o libaom passo 4 acelerado
	cd 4.TRANSC/aom_acc/bin && cmake -DTHESIS_PASS_TRANSC=1 -DTHESIS_OLD_DECODER=$(OLD_DECODER) -DAOM_TARGET_CPU=generic -DCMAKE_C_FLAGS="-I/usr/include/python3.8 -lpython3.8 -lm" .. && taskset -c $(CPU_LIST) make -j $(NUM_OF_CPU)


