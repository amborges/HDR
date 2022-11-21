#ifndef THESIS_H_ //0
#define THESIS_H_

#ifdef __cplusplus //1
	extern "C" {
#endif //-1


//Definindo geral as diretivas
#if defined(THESIS_PASS_DEC_ENC) && THESIS_PASS_DEC_ENC //1
	//#define THESIS_PASS_DEC_ENC 1
	#define THESIS_PASS_CSV     0
	#define THESIS_PASS_TRANSC  0
#else
	#define THESIS_PASS_DEC_ENC 0
#endif  //-1

#if defined(THESIS_PASS_CSV) && THESIS_PASS_CSV //1
	#define THESIS_PASS_DEC_ENC 0
	//#define THESIS_PASS_CSV     1
	#define THESIS_PASS_TRANSC  0
#else
	#define THESIS_PASS_CSV     0
#endif  //-1

#if defined(THESIS_PASS_TRANSC) && THESIS_PASS_TRANSC //1
	#define THESIS_PASS_DEC_ENC 0
	#define THESIS_PASS_CSV     0
	//#define THESIS_PASS_TRANSC  1
#else
	#define THESIS_PASS_TRANSC  0
#endif  //-1



//Inicializadores
#if THESIS_PASS_DEC_ENC || THESIS_PASS_TRANSC //1
	#include "av1/encoder/context_tree.h"
	#include "av1/common/enums.h"
#endif  //-1

#if THESIS_PASS_CSV || THESIS_PASS_TRANSC //1
	#include <stdint.h> //int64_t 
#endif //-1

#if THESIS_PASS_TRANSC //1
	#include <Python.h> //REQUER -I/usr/include/python3.8 -lpython3.8 na compilação
#endif //-1


#ifndef TRUE //1
	#define TRUE 1
	#define FALSE 0
#endif //-1

#define UCHAR unsigned char


/************************************/
/* DEFINIÇÕES DE TIPOS E ESTRUTURAS */
/************************************/

//estrutura que armazena as informações vindas do CSV
typedef struct CSV_S{
	int frame_idx;
	int mi_col;
	int mi_row;
	int bsize;
	int ptype;
	int pmode;
	int intra_inter;
} CSV;

//vetor que armazena largura, altura e profundidade
typedef struct {int w, h, d; } INT3;

//Estrutura que armazena as informações relevantes de cada pixel
typedef struct PIXEL_S{
	UCHAR depth;
	UCHAR bsize;
	UCHAR ptype;
	UCHAR pmode;
	UCHAR intra_inter;
} PIXEL;

//Estrutura que armazena as médias relevantes de cada zona de busca
typedef struct AVG_PIXEL_S{
	float depth;
	float bsize;
	float ptype;
	float pmode;
	float intra_inter;
} AVG_PIXEL;

//Estrutura que armazena uma lista de matrizes e seus tamanhos
typedef struct PROCESSED_FRAME_S{
	AVG_PIXEL** f128;
	AVG_PIXEL** f64;
	AVG_PIXEL** f32;
	AVG_PIXEL** f16;
	
	int w128;
	int h128;
	int w64;
	int h64;
	int w32;
	int h32;
	int w16;
	int h16;
	
	//variável que controla se essa estrutura já foi inicializada
	UCHAR initialized;
} PROCESSED_FRAME;


//Estrutura principal do projeto: BUFFER do QUADRO
typedef struct FRAME_S{
	int max_cols;
	int max_rows;
	PIXEL **pixel;
} FRAME;


#if !THESIS_PASS_DEC_ENC //1
	//enumerador da resposta do ML
	enum {
		THESIS_DONT_SPLIT   = 0,
		THESIS_DO_SPLIT     = 1,
		THESIS_WORKS_NORMAL = 2
	} THESIS_DECISION;
#endif //-1

//estrutura que armazenará uma série de variáveis globais
struct GLOBAL_VARIABLES_S{
	//localização da pasta
	char video_path[500];

#if THESIS_PASS_DEC_ENC || THESIS_PASS_CSV //1
	//variavel que armazena o caminho onde será salvo os dados no CSV
	char av1_output_csv_file[5000];
	
	//controla se o arquivo acima já foi incializado ou não
	unsigned char av1_csv_file_was_open;
#endif //-1

#if THESIS_PASS_CSV //1
	//variavel que armazena o caminho onde será lido os dados do CSV do AV1
	char av1_input_csv_file[500];
#endif //-1

#if THESIS_PASS_TRANSC || THESIS_PASS_CSV //1
	char* model_name;
	UCHAR is_there_a_model;

	//valores gerais do vídeo
	int width;
	int height;
	int cq_value;

#if THESIS_PASS_TRANSC //2
	int icq_value;
#endif //-2

	//arquivo OLD que contem todos os valores lidos
	CSV* old_decoder_csv;
	int old_decoder_csv_size;
	int old_decoder_csv_idx;
	
	//buffers dos quadros do OLD e AV1
	FRAME OLD_BUFFER_FRAME;
	FRAME AV1_BUFFER_FRAME;
	
	//controle do quadro, informando se o buffer já foi preenchido completamente ao menos uma única vez
	UCHAR buffer_filled_at_once;
	
	//buffer dos quadros PROCESSADOS do OLD e AV1
	PROCESSED_FRAME OLD_P_FRAME;
	PROCESSED_FRAME AV1_P_FRAME;
	
	//controlador de novos quadros
	UCHAR new_frame;
	
	//controlador do tamanho a ser alocado a qualquer estrutura INFO que for criada
	uint64_t info_size;

#if THESIS_PASS_CSV //2
	//controla a parada geral do programa, se ativo, mais nada pode funcionar
	int STOP_PRESS;
	
	//variável que indica quando a STOP_PRESS deve ser acionada
	int FTBE;
#endif //-2

#if THESIS_PASS_TRANSC //2
	//variável que mantem a conexão com o objeto python
	PyObject* py_module;
#endif //-2
#endif //-1
	
} GLOBAL_VARIABLES;





/*******************************************/
/* DEFINIÇÕES DE FUNÇÕES DE ACESSO EXTERNO */
/*******************************************/




//Limpa a memória de PROCESSED_FRAME
void free_PF(PROCESSED_FRAME* FRM);

//Importa valores inseridos no libaom para dentro na nossa estrutura
#if THESIS_PASS_DEC_ENC //1
	void THESIS_set_global_values(char* path);
#else //_1
	void THESIS_set_global_values(char* model, char* path, unsigned int width, unsigned int height);
#endif //-1

//Inicializa e finaliza as estruturas principais do código
#if THESIS_PASS_CSV //1
	void THESIS_initialize(int width, int height, int ftbe, char* in_path_name, char* out_path_name);
#elif THESIS_PASS_TRANSC //_1
	void THESIS_initialize(char* path_name, int width, int height, char* model_name);
#endif //-1

#if THESIS_PASS_TRANSC || THESIS_PASS_CSV //1
void THESIS_finalize();
#endif //-1


#if THESIS_PASS_TRANSC || THESIS_PASS_DEC_ENC //1
	//navega na árvore PC_TREE para descobrir a estrutura e exportar
	void THESIS_get_superblock_tree(PC_TREE *pc_tree, int frame_idx, int mi_col, int mi_row, bool is_root);
#endif //-1

#if THESIS_PASS_CSV //1
	int THESIS_read_av1_file();
#endif //-1

#if THESIS_PASS_TRANSC || THESIS_PASS_CSV //1
	//atualiza os buffers a cada novo superbloco
	void THESIS_update_buffer();
#endif //-1

#if THESIS_PASS_TRANSC //1
	//Identifica se houve sucesso no carregamento do ML
	UCHAR THESIS_have_ML();
	
	//pega a informação vinda do ML
	int THESIS_get_decision(BLOCK_SIZE block_size, int pos_c, int pos_r);
#endif //-1



#ifdef __cplusplus //1
	}  // extern "C"
#endif //-1

#endif //THESIS_H_ 0
