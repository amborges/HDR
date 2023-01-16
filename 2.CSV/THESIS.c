#include "THESIS.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <limits.h>
#include <math.h> //REQUER -lm na compilação


/*********************************************************************/
/***   DEFINES   *****************************************************/
/*********************************************************************/


//Abaixo vou definir os decodificadores
#define OLD_DECODER_IS_VP9 1
#define OLD_DECODER_IS_VP8 2
#define OLD_DECODER_IS_H264 3
#define OLD_DECODER_IS_H265 4
#define OLD_DECODER_IS_H266 5


//O define abaixo vai indicar quantas linhas poderão ser lidas no CSV para cada superbloco
//Se há 128x128 pixeis, então 128*128, no entanto, no AV1 cada pixel representa uma área de 4x4
//portanto, vou dividir a multiplicação acima por 4, assim eu garanto que haverá espaço o suficiente
//para ler quantos dados forem necessários.
//#define MAX_SIZE_OF_CSV 4096
#define MAX_SIZE_OF_CSV 9999

//Define que aloca um vetor V do tipo T com o tamanho de X
#define VMALLOC(M, X, T) {M = (T*)malloc(sizeof(T)*X);}

//Define que aloca uma matriz M do tipo T com o tamanho de W e H
#define MMALLOC(M, W, H, T) {M = (T**)malloc(sizeof(T*)*W); for (int i = 0; i < W; i++) M[i] = (T*)malloc(sizeof(T)*H); }

//Define que abrevia o laço de preenchimento da matriz
#define FILL_MATRIX(M, W, H) {for (int h = 0; h < H; h++) for (int w = 0; w < W; w++) M[w][h] = lst[idx++];}

//O define abaixo cria um laço capaz de limpar uma matrix de tamanho W
#define FREE_ME(M, W) {for(int w = 0; w < W; w++) free(M[w]); free(M);}





/*********************************************************************/
/***   Variáveis Globais Locais   ************************************/
/*********************************************************************/


static CSV CSV_AV1_SUPERBLOCK[MAX_SIZE_OF_CSV];
static int CSV_AV1_SUPERBLOCK_IDX = 0;


/*********************************************************************/
/***    Funções Simples    *******************************************/
/*********************************************************************/


//Função que lê um caminho e retorna um novo caminho. 
//Mais especificamente, vai receber algo como A e devolver algo como B
//A = /home/PATH_TO_FOLDER/shields2_640x360_120f/cq_55/video/coded_aom.av1
//B = /home/PATH_TO_FOLDER/shields2_640x360_120f/old_decoder.csv
void get_old_decoder_csv_file(char* in_path, char* out_path, int* cq_value){
	//declarando as variaveis que vou precisar
	char *last2nd = NULL, *last1st = NULL, *token = NULL;
    
    //limpando as palavras
    last1st = "";
   	last2nd = "";
   	strcpy(out_path, "");
    
    //só pode iniciar a cópia para a saída após achar a palavra "home"
    int copy_allowed = 0;
    
    //capturo a primeira substring
    token = strtok(in_path, "/");
    
    while (token != NULL) {
    	//para cada substring, faço:
    	
    	//se a substring for vídeo, então parar o laço
    	if(strcmp(token, "video") == 0)
			break;
		
		//verifica se já se pode sair copiando a substring
		if(strcmp(last1st, "home") == 0)
			copy_allowed = 1;
    	
    	//senão, faço andar a lista de palavras lidas
    	last2nd = last1st;
    	last1st = token;
    	
    	//copia a substring para a saída
    	if(copy_allowed){
    		//armazenar na string de saída o resultado
    		strcat(out_path, "/");
    		strcat(out_path, last2nd);
    	}
    	
    	//leio uma nova substring
    	token = strtok(NULL, "/");
    }
    
    //faltou ainda capturar o valor do CQ, portanto, capturo a substring de uma nova palavra
	token = strtok(last1st, "_"); //primeiro pego o termo 'cq'
	token = strtok(NULL, "_"); //agora capturo o número em sí
	*cq_value = atoi(token); //transfiro para o inteiro de saída

    //Criando os arquivos do CSV para o AV1
#if THESIS_PASS_DEC_ENC
	//seja exportando
	sprintf(GLOBAL_VARIABLES.av1_output_csv_file, "%s/av1_%d.csv", out_path, *cq_value);
#elif THESIS_PASS_CSV
	//seja importando
	sprintf(GLOBAL_VARIABLES.av1_input_csv_file,  "%s/av1_%d.csv", out_path, *cq_value);
#endif

    //ao final, adiciono o nome do arquivo CSV do OLD
    strcat(out_path, "/old_decoder.csv");
}


#if !THESIS_PASS_DEC_ENC
//função que recebe um ponto-flutuante e arredonda pra cima caso for maior ou igual a x.5
int my_round(double v){
	int a = (int)(v);
	float b = v - a;
	if(b < 0.5)
		return a;
	else
		return a + 1;
}

//função que pega dois números inteiros, aplica a divisão e retorna o arredondamento para cima dessa divisão.
int math_ceil_div(int a, int b){
	return (int)ceil((double)a / (double)b);
}

//lê um block_size e retorna um vetor contendo a largura, altura e a profundidade daquele block_size
INT3 old_decoder_decode_block_size(int bs){
	// largura, altura, profundidade
#if THESIS_OLD_DECODER == OLD_DECODER_IS_VP9
	INT3 bsv[13] = {
		{ 4,  4, 5},
		{ 4,  8, 4},
		{ 8,  4, 4},
		{ 8,  8, 4},
		{ 8, 16, 3},
		{16,  8, 3},
		{16, 16, 3},
		{16, 32, 2},
		{32, 16, 2},
		{32, 32, 2},
		{32, 64, 1},
		{64, 32, 1},
		{64, 64, 1}
	};
#elif THESIS_OLD_DECODER == OLD_DECODER_IS_VP8
	INT3 bsv[2] = {
		{ 4,  4, 5},
		{16, 16, 3}
	};
	
	int pos = 0;
	if(bs == 16) pos = 1;
	
	bs = pos;
#elif THESIS_OLD_DECODER == OLD_DECODER_IS_H264
	INT3 bsv[7] = {
		{ 4,  4, 5}, //SMB4x4, SI4MB
		{ 4,  8, 4}, //SMB4x8
		{ 8,  4, 4}, //SMB8x4
		{ 8,  8, 4}, //SMB8x8, P8x8, I8MB
		{ 8, 16, 3}, //P8x16
		{16,  8, 3}, //P16x8
		{16, 16, 3}  //P16x16, I16M, IBLOCK, IPCM
	};	
	
	int pos;
	     if (bs == 7 || bs == 9 || bs == 12) pos = 0; //4x4
	else if (bs == 6)                        pos = 1; //4x8
	else if (bs == 5)                        pos = 2; //8x4
	else if (bs == 4 || bs == 8 || bs == 13) pos = 3; //8x8
	else if (bs == 3)                        pos = 4; //8x16
	else if (bs == 2)                        pos = 5; //16x8
	else                                     pos = 6; //16x16
	
	bs = pos;
#elif THESIS_OLD_DECODER == OLD_DECODER_IS_H265
	INT3 bsv[5] = {
		{ 4,  4, 5},
		{ 8,  8, 4},
		{16, 16, 3},
		{32, 32, 2},
		{64, 64, 1}
	};	
	
	int pos;
	     if (bs == 4)  pos = 0; //4x4
	else if (bs == 8)  pos = 1; //8x8
	else if (bs == 16) pos = 2; //16x16
	else if (bs == 32) pos = 3; //32x32
	else               pos = 4; //64x64
	
	bs = pos;
#elif THESIS_OLD_DECODER == OLD_DECODER_IS_H266
	INT3 bsv[6] = {
		{ 4,   4, 5},
		{ 8,   8, 4},
		{16,  16, 3},
		{32,  32, 2},
		{64,  64, 1},
		{128,128, 0}
	};	
	
	int pos;
	     if (bs == 4)  pos = 0; //4x4
	else if (bs == 8)  pos = 1; //8x8
	else if (bs == 16) pos = 2; //16x16
	else if (bs == 32) pos = 3; //32x32
	else if (bs == 64) pos = 4; //64x64
	else               pos = 5; //128x128
	
	bs = pos;
#endif
	
	return bsv[bs];
}


INT3 av1_decode_block_size(int bs){
	// largura, altura, profundidade
	INT3 bsv[22] = {
		{  4,  4, 5},
		{  4,  8, 4},
		{  8,  4, 4},
		{  8,  8, 4},
		{  8, 16, 3},
		{ 16,  8, 3},
		{ 16, 16, 3},
		{ 16, 32, 2},
		{ 32, 16, 2},
		{ 32, 32, 2},
		{ 32, 64, 1},
		{ 64, 32, 1},
		{ 64, 64, 1},
		{ 64,128, 0},
		{128, 64, 0},
		{128,128, 0},
		{  4, 16, 3},
		{ 16,  4, 3},
		{  8, 32, 2},
		{ 32,  8, 2},
		{ 16, 64, 1},
		{ 64, 16, 1}
	};	
	return bsv[bs];
}

//Função que limpa a memória com as matrizes criadas
void free_PF(PROCESSED_FRAME* FRM){
	FREE_ME(FRM->f128, FRM->w128);
	FREE_ME(FRM->f64,  FRM->w64);
	FREE_ME(FRM->f32,  FRM->w32);
	//FREE_ME(FRM->f16,  FRM->w16);
}

//Função que recebe um vetor, uma largura e uma altura.
//Deve retornar um vetor de matrizes
void dreshape(PROCESSED_FRAME* FRM, AVG_PIXEL *lst){
	
	//na primeira vez, inicializa o PROCESSED_FRAME
	if(FRM->initialized == 0){
		//lembrando que, cada ponto no AV1 é multiplo de 4 pixeis
		int w = GLOBAL_VARIABLES.width  / 4;
		int h = GLOBAL_VARIABLES.height / 4;

		FRM->w128 = math_ceil_div(w, 32);
		FRM->h128 = math_ceil_div(h, 32);
		FRM->w64  = math_ceil_div(w, 16);
		FRM->h64  = math_ceil_div(h, 16);
		FRM->w32  = math_ceil_div(w,  8);
		FRM->h32  = math_ceil_div(h,  8);
		//FRM->w16  = math_ceil_div(w,  4);
		//FRM->h16  = math_ceil_div(h,  4);
		
		MMALLOC(FRM->f128, FRM->w128, FRM->h128, AVG_PIXEL);
		MMALLOC(FRM->f64,  FRM->w64,  FRM->h64,  AVG_PIXEL);
		MMALLOC(FRM->f32,  FRM->w32,  FRM->h32,  AVG_PIXEL);
		//MMALLOC(FRM->f16,  FRM->w16,  FRM->h16,  AVG_PIXEL);
		
		FRM->initialized = 1;
	}
	
	int idx = 0; //variável que controla o lst ao longo dos preenchimentos abaixo
	FILL_MATRIX(FRM->f128, FRM->w128, FRM->h128);
	FILL_MATRIX(FRM->f64,  FRM->w64,  FRM->h64);
	FILL_MATRIX(FRM->f32,  FRM->w32,  FRM->h32);
	//FILL_MATRIX(FRM->f16,  FRM->w16,  FRM->h16);
}

//função que lê um arquivo qualquer e retorna quantas linhas ele tem
int lines_in_file(char* file){
	FILE *f = fopen(file, "r");
	char *line = NULL;
    size_t len = 0;
    ssize_t read;
    int counter = 0;
	while ((read = getline(&line, &len, f)) != -1) {
		counter++;
	}
	fclose(f);
	if(line) free(line);
	
	return counter + 1;
}

//função que lê uma linha de um arquivo CSV e transporta os valores para a estrutura CSV
void from_line_get_CSV(char* line, CSV *csv){
	char *token;
	
	token = strtok(line, ",");
	csv->frame_idx = atoi(token);
	
	token = strtok(NULL, ",");
	csv->mi_col = atoi(token);
	
	token = strtok(NULL, ",");
	csv->mi_row = atoi(token);
	
	token = strtok(NULL, ",");
	csv->bsize = atoi(token);

#if !(THESIS_OLD_DECODER == OLD_DECODER_IS_VP8)
	token = strtok(NULL, ",");
	csv->ptype = atoi(token);
#else
	//no VP8 não tem alinhamentos, no geral é só bloco quadrado
	csv->ptype = 0;
#endif

	token = strtok(NULL, ",");
	csv->pmode = atoi(token);

#if !(THESIS_OLD_DECODER == OLD_DECODER_IS_VP8)
	token = strtok(NULL, ",");
	csv->intra_inter = atoi(token);
#else	
	//vamos identificar a flag aqui
	//token = strtok(NULL, ",");
	csv->intra_inter = csv->pmode == 0 ? 0 : 1;//atoi(token);
#endif
}

//Função que lê um arquivo e carrega os dados desse arquivo em uma lista de colunas pré-definidas
void load_old_decoder_csv(char* csv_path){
	//em primeiro lugar, vamos descobrir o tamanho do CSV
	GLOBAL_VARIABLES.old_decoder_csv_size = lines_in_file(csv_path);
	
	//em segundo lugar, vamos alocar o espaço necessário para armazenar todas as entradas do arquivo
	VMALLOC(GLOBAL_VARIABLES.old_decoder_csv, GLOBAL_VARIABLES.old_decoder_csv_size, CSV);
	
	//em terceiro lugar, vamos abrir o arquivo e ir carregando os dados ali
	FILE *f = fopen(csv_path, "r");
	char *line = NULL;
	size_t len = 0;
	ssize_t read;
	int idx = 0;
	while ((read = getline(&line, &len, f)) != -1) {
		from_line_get_CSV(line, &GLOBAL_VARIABLES.old_decoder_csv[idx++]);
	}
	//encerrando ponteiros locais
	fclose(f);
	if(line) free(line);
}

//insere valores em um pixel da matriz
void pixel_set(PIXEL *self, PIXEL vetor_de_valores){
	self->depth       = vetor_de_valores.depth;
	self->bsize       = vetor_de_valores.bsize;
	self->ptype       = vetor_de_valores.ptype;
	self->pmode       = vetor_de_valores.pmode;
	self->intra_inter = vetor_de_valores.intra_inter;
}

//manda o quadro adicionar valores a um ponto do pixel
void frame_setitem(FRAME *self, int pos1, int pos2, PIXEL vetor_de_valores){
	pixel_set(&self->pixel[pos1][pos2], vetor_de_valores);
}

//finaliza o buffer do quadro
void frame_end(FRAME *self){
	for(int w = 0; w < self->max_cols; w++) 
		free(self->pixel[w]); 
	free(self->pixel);
}

//Verificase houve troca de quadro, em caso positivo, retorna 1
int new_frame(){
	if(GLOBAL_VARIABLES.new_frame){
		GLOBAL_VARIABLES.new_frame = 0;
#if THESIS_PASS_CSV
		static int frame_number = 0;
		frame_number++;
		if(frame_number >= GLOBAL_VARIABLES.FTBE)
			GLOBAL_VARIABLES.STOP_PRESS = 1;
#endif
		return 1;
	}
	return 0;
}

#endif



/*********************/
/* FUNÇÕES COMPLEXAS */
/*********************/


#if !THESIS_PASS_DEC_ENC

//inicializa o buffer do quadro
void frame_init(FRAME *self, int width, int height){
	self->max_cols = math_ceil_div(width,  4);
	self->max_rows = math_ceil_div(height, 4);
	
	MMALLOC(self->pixel, self->max_cols, self->max_rows, PIXEL);
	PIXEL empty = {0,0,0,0,0};
	//Preciso executar o laço abaixo para limpar todos os dados sujos que podem existir na memória
	for (int i = 0; i < self->max_cols; i++)
		for (int j = 0; j < self->max_rows; j++)
			pixel_set(&self->pixel[i][j], empty);
}

//verifica se todos os elementos da linha do csv estão com valores válidos
//retorna 0 se todos os elementos forem válidos, caso contrário, 1
int is_the_csv_line_empty(CSV line){
	int returned = 0;
	if(line.frame_idx < 0) returned = 1;
	if(line.mi_col    < 0) returned = 1;
	if(line.mi_row    < 0) returned = 1;
	if(line.bsize     < 0) returned = 1;
	return returned;
}

//de uma linha vinda do CSV do OLD, preenche o buffer do quadro
void old_decoder_row_treatment(CSV line, FRAME *FRM){
#if THESIS_OLD_DECODER == OLD_DECODER_IS_VP9
	//No VP9 a relação da posição dos pixeis é de 8, não de 4 como no AV1
	int mi_col = line.mi_col * 2;
	int mi_row = line.mi_row * 2;
#elif THESIS_OLD_DECODER == OLD_DECODER_IS_VP8
	//No vp8 a relação da posição dos pixeis é de 16, não de 4 como no AV1
	int mi_col = line.mi_col * 4;
	int mi_row = line.mi_row * 4;
#else
// #elif (THESIS_OLD_DECODER == OLD_DECODER_IS_H264) || (THESIS_OLD_DECODER == OLD_DECODER_IS_H265) || (THESIS_OLD_DECODER == OLD_DECODER_IS_H266)
	//No H.26x a relação da posição dos pixeis é de 1, não de 4 como no AV1
	int mi_col = line.mi_col / 4;
	int mi_row = line.mi_row / 4;
#endif
	
	INT3 crd = old_decoder_decode_block_size(line.bsize);
	PIXEL pxl;
	pxl.depth       = (UCHAR)crd.d;
	pxl.bsize       = (UCHAR)line.bsize;
	pxl.ptype       = (UCHAR)line.ptype;
	pxl.pmode       = (UCHAR)line.pmode;
	pxl.intra_inter = (UCHAR)line.intra_inter;
	
	//com as variáveis preparadas, eu preencho o quadro na região determinada	
	for(int c = 0; c < crd.w; c++){
		for(int r = 0; r < crd.h; r++){
			//caso os indexes apontarem para um valor inválido do quadro, não preencher
			if( (mi_col + c < FRM->max_cols) && (mi_row + r < FRM->max_rows) ){
				frame_setitem(FRM, mi_col + c, mi_row + r, pxl);
			}
		}
	}
}

void look_for_new_frame(int col, int row){
	static int lcol = -1;
	static int lrow = -1;
	
	if( (col == 0) && (row == 0) ){
		if( (col < lcol) && (row < lrow) ){
			GLOBAL_VARIABLES.new_frame = 1;
		}
	}
	else{
		lcol = col;
		lrow = row;
	}
}

//de uma linha vinda do codificador AV1, preenche o buffer do quadro
void av1_row_treatment(CSV line, FRAME *FRM){
	look_for_new_frame(line.mi_col, line.mi_row);
	
	INT3 crd = av1_decode_block_size(line.bsize);
	PIXEL pxl;
	pxl.depth       = (UCHAR)crd.d;
	pxl.bsize       = (UCHAR)line.bsize;
	pxl.ptype       = (UCHAR)line.ptype;
	pxl.pmode       = (UCHAR)line.pmode;
	pxl.intra_inter = (UCHAR)line.intra_inter;
	
	//com as variáveis preparadas, eu preencho o quadro na região determinada	
	for(int c = 0; c < crd.w; c++){
		for(int r = 0; r < crd.h; r++){
			//caso os indexes apontarem para um valor inválido do quadro, não preencher
			if( (line.mi_col + c < FRM->max_cols) && (line.mi_row + r < FRM->max_rows) ){
				frame_setitem(FRM, line.mi_col + c, line.mi_row + r, pxl);
			}
		}
	}
}

//de uma lista de valores vindos do CSV do OLD ou do codificador Av1, preenche o buffer do quadro
void fill_frame_buffer(CSV* lst_of_csv, int csv_size, FRAME* FRM, int is_old_decoder){
	for(int i = 0; i < csv_size; i++){
		if(!is_the_csv_line_empty(lst_of_csv[i])){
			//só entra aqui os valores válidos
			if(is_old_decoder)
				old_decoder_row_treatment(lst_of_csv[i], FRM);
			else
				av1_row_treatment(lst_of_csv[i], FRM);
		}
	}
}

//Essa função captura um superbloco de 128x128 do CSV do OLD
int old_decoder_select_csv(CSV* short_csv, int* csv_idx){
	
	if(GLOBAL_VARIABLES.old_decoder_csv_idx >= GLOBAL_VARIABLES.old_decoder_csv_size)
		//não há mais dados a serem lidos.
		return 0;

	//A primeira linha de cada CSV deve ser lida
	//pois CERTAMENTE é múltiplo de 32
	short_csv[(*csv_idx)++] = GLOBAL_VARIABLES.old_decoder_csv[GLOBAL_VARIABLES.old_decoder_csv_idx++];
	
	//laço infinito. Existe uma regra própria para encerrar o laço
	while(1){
		//caso o index do CSV acabe antes do previsto
		if (GLOBAL_VARIABLES.old_decoder_csv_idx >= GLOBAL_VARIABLES.old_decoder_csv_size){
			//encerrar o laço
			break;
		}
		
		//caso a linha lida for início de um superbloco, parar o laço
		if( (GLOBAL_VARIABLES.old_decoder_csv[GLOBAL_VARIABLES.old_decoder_csv_idx].mi_col % 32 == 0) &&
		    (GLOBAL_VARIABLES.old_decoder_csv[GLOBAL_VARIABLES.old_decoder_csv_idx].mi_row % 32 == 0)){
			//encerrar o laço
			break;
		}
		
		//senão
		//capturo os valores
		short_csv[(*csv_idx)] = GLOBAL_VARIABLES.old_decoder_csv[GLOBAL_VARIABLES.old_decoder_csv_idx];
		//incremento os indexes
		(*csv_idx)++;
		GLOBAL_VARIABLES.old_decoder_csv_idx++;
	}
	return 1;
}

//Função que lê um frame em uma determinada posição, e calcula os valores médios daquela região, armazenando esses valores na variável PIXEL
void process_pixels(FRAME *frame, int col, int row, int bsize, AVG_PIXEL* return_info){
	//primeiro, captura os valores das posições reais que eles têm
	int start_from_row = row - 1;
	int start_from_col = col - 1;
	
	int end_in_row = row + math_ceil_div(bsize, 4);
	int end_in_col = col + math_ceil_div(bsize, 4);
	
	//segundo, verifica se as posições são inteiros positivos
	if (start_from_row <= 0) start_from_row = 0;
	if (start_from_col <= 0) start_from_col = 0;
	if (end_in_row <= 0)     end_in_row = 0;
	if (end_in_col <= 0)     end_in_col = 0;
	
	//terceiro, verifica se as posições são menores que o tamanho do quadro
	if (start_from_row >= frame->max_rows) start_from_row = frame->max_rows - 1;
	if (start_from_col >= frame->max_cols) start_from_col = frame->max_cols - 1;
	if (end_in_row >= frame->max_rows)     end_in_row     = frame->max_rows - 1;
	if (end_in_col >= frame->max_cols)     end_in_col     = frame->max_cols - 1;
	
	//quarto, calcula o tamanho máximo de valores a serem somados
	double denominator = (double)(end_in_col - start_from_col) * (end_in_row - start_from_row);
	
	if(denominator == 0.)
		//evita divisão por zero
		return;
	
	//quinto, inicializa as variáveis contadoras
	int lst_idx = 0;
	return_info->depth       = 0.0;
	return_info->bsize       = 0.0;
	return_info->ptype       = 0.0;
	return_info->pmode       = 0.0;
	return_info->intra_inter = 0.0;
	
	//sexto, soma todas as ocorrências daquela região válida
	for (int c = start_from_col; c < end_in_col; c++){
		for (int r = start_from_row; r < end_in_row; r++){
			return_info->depth       += frame->pixel[c][r].depth;
			return_info->bsize       += frame->pixel[c][r].bsize;
			return_info->ptype       += frame->pixel[c][r].ptype;
			return_info->pmode       += frame->pixel[c][r].pmode;
			return_info->intra_inter += frame->pixel[c][r].intra_inter;
		}
	}
	
	//sétimo, calcula a média e armazena no respectivo local
	return_info->depth       = return_info->depth       / denominator;
	return_info->bsize       = return_info->bsize       / denominator;
	return_info->ptype       = return_info->ptype       / denominator;
	return_info->pmode       = return_info->pmode       / denominator;
	return_info->intra_inter = return_info->intra_inter / denominator;
}


//função que aloca a memória dedicada ao vetor PIXEL
//caso o tamanho nunca foi calculado, calcula-se
void info_size(){
	if(GLOBAL_VARIABLES.info_size == 0){
		int w = GLOBAL_VARIABLES.width;
		int h = GLOBAL_VARIABLES.height;
		
		int s1 = math_ceil_div(w, 32);
		int s2 = math_ceil_div(h, 32);
		
		int s3 = math_ceil_div(w, 16);
		int s4 = math_ceil_div(h, 16);
		
		int s5 = math_ceil_div(w,  8);
		int s6 = math_ceil_div(h,  8);
		
		//int s7 = math_ceil_div(w,  4);
		//int s8 = math_ceil_div(h,  4);
		
		//GLOBAL_VARIABLES.info_size = (s1 * s2) + (s3 * s4) + (s5 * s6) + (s7 * s8) + 1;
		GLOBAL_VARIABLES.info_size = (s1 * s2) + (s3 * s4) + (s5 * s6) + 1;  
	}
}

void processa_quadro(AVG_PIXEL* info_list, FRAME *frame){
	int lst_idx = 0;
	int bsize[3] = {128, 64, 32};
	int bsize_ref;
	int step;
	
	//Para cada nível de profundidade, fazer
	for(int depth_ref = 0; depth_ref < 3; depth_ref++){
		bsize_ref = bsize[depth_ref];
		
		//pulando de passo em passo os pixeis de interesse
		step = math_ceil_div(bsize_ref, 3);
		
		//Para cada pixel dentro do passo de interesse, fazer
		for(int r = 0; r < frame->max_rows; r += step){
			for(int c = 0; c < frame->max_cols; c += step){
				//primeiro, limpar a variável info
				info_list[lst_idx].depth = 0;
				
				//depois, extrair os dados de interesse e armazenar em info
				process_pixels(frame, c, r, bsize_ref, &info_list[lst_idx]);
				
				//terceiro, passa para a próxima posição de info
				lst_idx++;
			}
		}
	}
}


//função que lê uma lista de informações processadas, seleciona e anexa a uma string algumas dessas informações
void seleciona_informacoes(AVG_PIXEL **info, int c, int r, int max_col, int max_row, char* attributes){
	char* empty_string = ",,,,,";
	//primeiro se testa os limites da matriz
	if (c < 0)
		sprintf(attributes, "%s%s", attributes, empty_string);
	else if (r < 0)
		sprintf(attributes, "%s%s", attributes, empty_string);
	else if (c >= max_col)
		sprintf(attributes, "%s%s", attributes, empty_string);
	else if (r >= max_row)
		sprintf(attributes, "%s%s", attributes, empty_string);
	else{
		sprintf(attributes, "%s%.2f,%.2f,%.2f,%.2f,%.2f,",attributes, 
		                                                  info[c][r].depth,
		                                                  info[c][r].bsize,
		                                                  info[c][r].ptype,
		                                                  info[c][r].pmode,
		                                                  info[c][r].intra_inter);
	}
}

#endif


#if THESIS_PASS_DEC_ENC
//função que lê os dados armazenados nos buffers processados e exporta eles para um arquivo CSV
void export_data(CSV *data){
	static FILE* f;
	if(!GLOBAL_VARIABLES.av1_csv_file_was_open){
		f = fopen(GLOBAL_VARIABLES.av1_output_csv_file, "w");
		GLOBAL_VARIABLES.av1_csv_file_was_open = 1;
	}
	fprintf(f, "%d,%d,%d,%d,%d,%d,%d\n", data->frame_idx, 
	                                     data->mi_col, 
	                                     data->mi_row, 
	                                     data->bsize, 
	                                     data->ptype, 
	                                     data->pmode, 
	                                     data->intra_inter);
}
#endif


#if THESIS_PASS_CSV

//#essa função recebe um bloco e diz qual é a decisão que foi tomada nele
//# saída: decisão, sendo
//#          0, THESIS_DONT_SPLIT
//#          1, THESIS_DO_SPLIT
void seleciona_decisao(int this_depth, int depth_reference, char* attributes){
	if(this_depth < depth_reference){
		sprintf(attributes, "%s%d", attributes, THESIS_DO_SPLIT); //força SPLIT
	}
	else{
		sprintf(attributes, "%s%d", attributes, THESIS_DONT_SPLIT); //não é pra usar SPLIT
	}
}

//função que lê os dados armazenados nos buffers processados e exporta eles para um arquivo CSV
void export_data(char* attributes){
	static FILE* f = NULL;
	if(!GLOBAL_VARIABLES.av1_csv_file_was_open){
		f = fopen(GLOBAL_VARIABLES.av1_output_csv_file, "a");
		if(f == NULL)
			printf("FALHA AO SALVAR DADOS NO ARQUIVO %s\n", GLOBAL_VARIABLES.av1_output_csv_file);
		GLOBAL_VARIABLES.av1_csv_file_was_open = 1;
		
	}
	/*
	 * CABECALHO
	 * curr_cq, curr_depth,
	 * Adpt, Absz, Aptp, Apmd, Ai_i
	 * Bdpt, Bbsz, Bptp, Bpmd, Bi_i
	 * Cdpt, Cbsz, Cptp, Cpmd, Ci_i
	 * Ddpt, Dbsz, Dptp, Dpmd, Di_i
	 * Edpt, Ebsz, Eptp, Epmd, Ei_i
	 * decision
	 */
	fprintf(f, "%s\n", attributes);
}

#endif


#if THESIS_PASS_TRANSC

//Função que realiza a conexão do código C com o Python
//Há SEMPRE um despejo de memória extra. Nunca consegui resolver
void PyInit(char* model_name){
	Py_Initialize();
	if(!Py_IsInitialized()){
		printf("Falha na Inicializado do Módulo Python\n");
		exit(404);
	}
	
	PyRun_SimpleString("import numpy as np");
	PyRun_SimpleString("import pandas as pd");
	PyRun_SimpleString("from sklearn.naive_bayes import CategoricalNB");
	PyRun_SimpleString("import os");
	PyRun_SimpleString("import pickle");
	
	//capturando o nome da pasta atual
	char path[500];
	getcwd(path, sizeof(path)); //estou assumindo que sempre vai retornar um valor válido. O correto é comparar com null dentro de um if
	//adicionando o resto do caminho que leva até aonde está o arquivo 'ML_Connect.py'
	strcat(path, "/aom_acc/av1/encoder/");
	
	wchar_t* wpath = Py_DecodeLocale(path, NULL);
	PySys_SetPath(wpath);//Sets the working path to the current path
	
	PyRun_SimpleString("global ML_MODEL");
	
	//Carregando o módulo python que desejamos importar
	GLOBAL_VARIABLES.py_module = PyImport_ImportModule("ML_Connect");
	
	//verificando se o módulo foi inicializado corretamente
	if (!(GLOBAL_VARIABLES.py_module != 0)){
		printf("Erro ao inicializar o módulo python\n");
		PyErr_Print();
		return;
	}
	
	PyObject* param = NULL;
	param = Py_BuildValue("(s)", model_name);
	
	//Carregando a função e executando ela
	PyObject* func = PyObject_GetAttrString(GLOBAL_VARIABLES.py_module, "init_py");
	PyObject* result = PyEval_CallObject(func, param);
	
	//identificando se a função executou com sucesso
	if(result == NULL){
		printf("Houve erro para executar a função init_py\n");
		PyErr_Print();
	}
	
	if(func != NULL)
		Py_DECREF(func);
	if(param != NULL)
		Py_DECREF(param);
}

//chama uma função python que retorna um valor inteiro
int PY_machine_learning_decision(int depth, int cq, char* attributes){
	if(GLOBAL_VARIABLES.py_module == NULL){
		return -1;
	}
	
	PyObject* param = NULL;
	param = Py_BuildValue("iis", depth, cq, attributes);
	
	//Carregando a função e executando ela
	PyObject* func = PyObject_GetAttrString(GLOBAL_VARIABLES.py_module, "get_decision");
	PyObject* result = PyEval_CallObject(func, param);
	
	//identificando se a função executou com sucesso
	if(result == NULL){
		printf("Houve erro para executar a função get_decision\n");
		PyErr_Print();
	}
	
	//capturando a resposta
	int iresult = (int)PyLong_AsLong(result);
	
	//limpando a memória
	if(param != NULL)
		Py_DECREF(param);
	if(func != NULL)
		Py_DECREF(func);
	if(result != NULL)
		Py_DECREF(result);
	
	//# saída: decisão, sendo
	//#          0, NÃO usar SPLIT                        (THESIS_DONT_SPLIT)
	//#          1, USAR SPLIT                            (THESIS_DO_SPLIT)
	//#          2, deixar o libaom funcionar normalmente (THESIS_WORKS_NORMAL)
	return iresult;
}


#endif


/*********************/
/* FUNÇÕES  EXTERNAS */
/*********************/

#if THESIS_PASS_DEC_ENC

//função que inicializa todos os alocamentos necessários para a execução do código
void THESIS_initialize(char* path_name){
	//primeira coisa, adicionar as variáveis recebidas em seus respectivos locais
	strcpy(GLOBAL_VARIABLES.video_path, path_name);
		
	//Agora temos que localizar o arquivo CSV do OLD e já aproveitamos para descobrir o CQ utilizado
	char csv_path[500];
	int cq_value;
	get_old_decoder_csv_file(GLOBAL_VARIABLES.video_path, csv_path, &cq_value);
}

//Função que é chamada logo no inicio da codificação, que captura os dados externos e armazena localmente
void THESIS_set_global_values(char* path){
	static unsigned char executed = 0;
	if(!executed){
		executed = 1;
		THESIS_initialize(path);
	}
}

#endif




#if THESIS_PASS_CSV

//função que inicializa todos os alocamentos necessários para a execução do código
void THESIS_initialize(int width, int height, int ftbe, char* in_path_name, char* out_path_name){
	//primeira coisa, adicionar as variáveis recebidas em seus respectivos locais
	strcpy(GLOBAL_VARIABLES.video_path, in_path_name);
	strcpy(GLOBAL_VARIABLES.av1_output_csv_file, out_path_name);
	GLOBAL_VARIABLES.width      = width;
	GLOBAL_VARIABLES.height     = height;
	GLOBAL_VARIABLES.FTBE       = ftbe;
	
	//Agora temos que localizar o arquivo CSV do OLD e já aproveitamos para descobrir o CQ utilizado
	char csv_path[500];
	int cq_value;
	get_old_decoder_csv_file(GLOBAL_VARIABLES.video_path, csv_path, &cq_value);
	
	//adicionando o cq
	GLOBAL_VARIABLES.cq_value = cq_value;
	
	//carregar o arquivo csv
	load_old_decoder_csv(csv_path);
	GLOBAL_VARIABLES.old_decoder_csv_idx = 0;
	
	//zerando o tamanho máximo do buffer de info, seu valor real é calculado em outra parte
	GLOBAL_VARIABLES.info_size = 0;
	
	//determina os limites da matriz PIXEL
	info_size();
	
	//inicializar o controlador dos buffers de PROCESSED_FRAME
	GLOBAL_VARIABLES.OLD_P_FRAME.initialized = 0;
	GLOBAL_VARIABLES.AV1_P_FRAME.initialized = 0;
	GLOBAL_VARIABLES.new_frame = 0;
	
	//carregar o buffer dos quadros
	frame_init(&GLOBAL_VARIABLES.OLD_BUFFER_FRAME, GLOBAL_VARIABLES.width, GLOBAL_VARIABLES.height);
	frame_init(&GLOBAL_VARIABLES.AV1_BUFFER_FRAME, GLOBAL_VARIABLES.width, GLOBAL_VARIABLES.height);
	
	//informar que os quadros dos buffers nunca foram preenchidos nenhuma vez
	GLOBAL_VARIABLES.buffer_filled_at_once = 0;
	
	//preencher os primeiros superblocos do OLD
	//o buffer do OLD precisa estar na frente do AV1, uma linha inteira de superblocos.
	int repeat = 1;//math_ceil_div(GLOBAL_VARIABLES.width, 128) + 1;
	int old_decoder_select_size;
	int read_ok;
	for (int i = 0; i < repeat; i++){
		CSV old_decoder_select[MAX_SIZE_OF_CSV];
		old_decoder_select_size = 0;
		read_ok = old_decoder_select_csv(old_decoder_select, &old_decoder_select_size);
		if(read_ok){
			fill_frame_buffer(old_decoder_select, old_decoder_select_size, &GLOBAL_VARIABLES.OLD_BUFFER_FRAME, 1);
		}
	}
	
	//zerando a variavel que controla o acesso ao csv do av1
	GLOBAL_VARIABLES.av1_csv_file_was_open = 0;
}

int is_new_superblock(CSV elm){
	if(elm.mi_col % 32 == 0 && elm.mi_row % 32 == 0)
		return 1;
	return 0;
}


int THESIS_read_av1_file(){
	if(GLOBAL_VARIABLES.STOP_PRESS)
		return 0;
	
	static FILE* av1_file    = NULL;
	static int av1_file_open = 0;
	static CSV lst_line;
	static int counter       = 0;
	
	if(!av1_file_open){
		av1_file = fopen(GLOBAL_VARIABLES.av1_input_csv_file, "r");
		if(av1_file == NULL){
			printf("ERRO AO ABRIR O ARQUIVO %s\n", GLOBAL_VARIABLES.av1_input_csv_file);
			return 0;
		}
		av1_file_open = 1;
	}
	else{
		CSV_AV1_SUPERBLOCK[CSV_AV1_SUPERBLOCK_IDX++] = lst_line;
	}
	
	char *line = NULL;
	size_t len = 0;
	ssize_t read;

	while ((read = getline(&line, &len, av1_file)) != -1) {
		from_line_get_CSV(line, &CSV_AV1_SUPERBLOCK[CSV_AV1_SUPERBLOCK_IDX++]);
		lst_line = CSV_AV1_SUPERBLOCK[CSV_AV1_SUPERBLOCK_IDX - 1];
		
		if(is_new_superblock(CSV_AV1_SUPERBLOCK[CSV_AV1_SUPERBLOCK_IDX - 1])){
			break;
		}
	}

	return 1;
}

//Função que prepara os dados e exporta os dados
void export_info(int depth, int pos_c, int pos_r){
	if(GLOBAL_VARIABLES.STOP_PRESS)
		return;
	
	//Também é preciso verificar se o buffer dos quadros já foram preenchido ao menos uma vez
	if(!GLOBAL_VARIABLES.buffer_filled_at_once){
		return;
	}
	
	if(depth >= 3){
		//a princípio nunca vai entrar aqui, mas por precaução
		return;
	}
	
	//segundo, preciso converter a posição de referência que estou olhando para os limites da matrix a ser explorada
	int c = math_ceil_div(pos_c, (int)( 32. / pow(2., depth) ) );
	int r = math_ceil_div(pos_r, (int)( 32. / pow(2., depth) ) );
	
	//terceiro, abrevio os valores máximos de coluna e linha
	int max_c, max_r;
	
	//Quarto, abrevio o processed frame que será utilizado
	AVG_PIXEL **info_av1 = NULL;
	AVG_PIXEL **info_old_decoder = NULL;
	switch(depth){
		case 0:
			info_old_decoder = GLOBAL_VARIABLES.OLD_P_FRAME.f128;
			info_av1 = GLOBAL_VARIABLES.AV1_P_FRAME.f128;
			max_c = GLOBAL_VARIABLES.OLD_P_FRAME.w128;
			max_r = GLOBAL_VARIABLES.OLD_P_FRAME.h128;
			break;
		case 1:
			info_old_decoder = GLOBAL_VARIABLES.OLD_P_FRAME.f64;
			info_av1 = GLOBAL_VARIABLES.AV1_P_FRAME.f64;
			max_c = GLOBAL_VARIABLES.OLD_P_FRAME.w64;
			max_r = GLOBAL_VARIABLES.OLD_P_FRAME.h64;
			break;
		case 2:
		default:
			info_old_decoder = GLOBAL_VARIABLES.OLD_P_FRAME.f32;
			info_av1 = GLOBAL_VARIABLES.AV1_P_FRAME.f32;
			max_c = GLOBAL_VARIABLES.OLD_P_FRAME.w32;
			max_r = GLOBAL_VARIABLES.OLD_P_FRAME.h32;
			break;
		//case 3:
		//default:
		//	info_old_decoder = GLOBAL_VARIABLES.OLD_P_FRAME.f16;
		//	info_av1 = GLOBAL_VARIABLES.AV1_P_FRAME.f16;
		//	max_c = GLOBAL_VARIABLES.OLD_P_FRAME.w16;
		//	max_r = GLOBAL_VARIABLES.OLD_P_FRAME.h16;
		//	break;
	}
	
	//Quinto, capturo as informações em formato texto, conforme
	char attributes[5000];
	
	//A. insiro as informações básicas ao modelo (CQ utilizado e profundidade de referência atual)
	sprintf(attributes, "%d,%d,", GLOBAL_VARIABLES.cq_value, depth);
	
	//B. insiro as informações que estão acima do bloco de referência no AV1
	seleciona_informacoes(info_av1, c,     r - 1, max_c, max_r, attributes);
	
	//C. insiro as informações que estão a esquerda do bloco de referência no AV1
	seleciona_informacoes(info_av1, c - 1, r,     max_c, max_r, attributes);
	
	//D. insiro as informações que estão na posição de referência no OLD
	seleciona_informacoes(info_old_decoder, c,     r,     max_c, max_r, attributes);
	
	//E. insiro as informações que estão acima do bloco de referência no OLD
	seleciona_informacoes(info_old_decoder, c,     r - 1, max_c, max_r, attributes);
	
	//F. insiro as informações que estão a esquerda do bloco de referência no OLD
	seleciona_informacoes(info_old_decoder, c - 1, r,     max_c, max_r, attributes);
	
	//captura qual foi o modo escolhido naquela posição
	seleciona_decisao(depth, info_av1[c][r].depth, attributes);
	
	//Por fim, chama o modelo e retorna uma resposta
	export_data(attributes);
}

void loop_exporting(){
	//PARA CADA TAMANHO DE BLOCO
	//PARA CADA POSIÇÃO W H DO QUADRO
	static int iii = 0;
	
	int step;
	for(int depth = 0; depth < 3; depth++){
		switch(depth){
			case 0: step = 32; break;
			case 1: step = 16; break;
			case 2: step =  8; break;
			//case 3: step =  4; break;
		}
		for(int col = 0; col < GLOBAL_VARIABLES.width / 4; col += step){
			for(int row = 0; row < GLOBAL_VARIABLES.height / 4; row += step){
				export_info(depth, col, row);
			}
		}
	}
}

#endif




#if THESIS_PASS_TRANSC

//função que inicializa todos os alocamentos necessários para a execução do código
void THESIS_initialize(char* path_name, int width, int height, char* model_name){
	//primeira coisa, adicionar as variáveis recebidas em seus respectivos locais
	strcpy(GLOBAL_VARIABLES.video_path, path_name);
	GLOBAL_VARIABLES.width      = width;
	GLOBAL_VARIABLES.height     = height;
	GLOBAL_VARIABLES.model_name = model_name;
	
	GLOBAL_VARIABLES.is_there_a_model = 0;
	
	//caso houver algum modelo, identificar sua presença
	if(GLOBAL_VARIABLES.model_name != NULL)
		GLOBAL_VARIABLES.is_there_a_model = 1;
	
	//Agora temos que localizar o arquivo CSV do OLD e já aproveitamos para descobrir o CQ utilizado
	char csv_path[500];
	int cq_value;
	get_old_decoder_csv_file(GLOBAL_VARIABLES.video_path, csv_path, &cq_value);
	
	//adicionando o cq
	GLOBAL_VARIABLES.cq_value = cq_value;
	     if(cq_value == 20) GLOBAL_VARIABLES.icq_value = 0;
	else if(cq_value == 32) GLOBAL_VARIABLES.icq_value = 1;
	else if(cq_value == 43) GLOBAL_VARIABLES.icq_value = 2;
	else if(cq_value == 55) GLOBAL_VARIABLES.icq_value = 3;
	
	//carregar o arquivo csv
	load_old_decoder_csv(csv_path);
	GLOBAL_VARIABLES.old_decoder_csv_idx = 0;
	
	//zerando o tamanho máximo do buffer de info, seu valor real é calculado em outra parte
	GLOBAL_VARIABLES.info_size = 0;
	
	//determina os limites da matriz PIXEL
	info_size();
	
	//inicializar o controlador dos buffers de PROCESSED_FRAME
	GLOBAL_VARIABLES.OLD_P_FRAME.initialized = 0;
	GLOBAL_VARIABLES.AV1_P_FRAME.initialized = 0;
	GLOBAL_VARIABLES.new_frame = 0;
	
	//carregar o buffer dos quadros
	frame_init(&GLOBAL_VARIABLES.OLD_BUFFER_FRAME, GLOBAL_VARIABLES.width, GLOBAL_VARIABLES.height);
	frame_init(&GLOBAL_VARIABLES.AV1_BUFFER_FRAME, GLOBAL_VARIABLES.width, GLOBAL_VARIABLES.height);
	
	//informar que os quadros dos buffers nunca foram preenchidos nenhuma vez
	GLOBAL_VARIABLES.buffer_filled_at_once = 0;
	
	//preencher os primeiros superblocos do OLD
	//o buffer do OLD precisa estar na frente do AV1, uma linha inteira de superblocos.
	int repeat = math_ceil_div(GLOBAL_VARIABLES.width, 128) + 1;
	int old_decoder_select_size;
	int read_ok;
	for (int i = 0; i < repeat; i++){
		CSV old_decoder_select[MAX_SIZE_OF_CSV];
		old_decoder_select_size = 0;
		read_ok = old_decoder_select_csv(old_decoder_select, &old_decoder_select_size);
		if(read_ok){
			fill_frame_buffer(old_decoder_select, old_decoder_select_size, &GLOBAL_VARIABLES.OLD_BUFFER_FRAME, 1);
		}
	}
	//Zerando a conexão python, para garantir funcionalidade futura
	GLOBAL_VARIABLES.py_module = NULL;
	
	//Inicializando a conexão com o código python
	if(GLOBAL_VARIABLES.is_there_a_model)
		PyInit(model_name);
}

//função que retorna a variável GLOBAL_VARIABLES.is_there_a_model
UCHAR THESIS_have_ML(){
	return GLOBAL_VARIABLES.is_there_a_model;
}

//Função que prepara os dados
int THESIS_get_decision(BLOCK_SIZE block_size, int pos_c, int pos_r){
	//https://www.freecodecamp.org/news/transform-machine-learning-models-into-native-code-with-zero-dependencies/
	//ANTES DE TUDO, verifico se existe algum modelo carregado
	if(!GLOBAL_VARIABLES.is_there_a_model){
		//em caso negativo, FAÇA O QUE QUISER
		return THESIS_WORKS_NORMAL;
	}
	
	//Também é preciso verificar se o buffer dos quadros já foram preenchido ao menos uma vez
	if(!GLOBAL_VARIABLES.buffer_filled_at_once){
		return THESIS_WORKS_NORMAL;
	}
	
	//primeira coisa, capturo as informações referentes ao tipo de bloco de referência
	INT3 crd = av1_decode_block_size(block_size);
	
	//se o bloco for 4x4, nada a fazer, mas não testar SPLIT
	if(crd.d >= 3){
		return THESIS_DONT_SPLIT;
	}
	
	//segundo, preciso converter a posição de referência que estou olhando para os limites da matrix a ser explorada
	int c = math_ceil_div(pos_c, (int)( 32. / pow(2., crd.d) ) );
	int r = math_ceil_div(pos_r, (int)( 32. / pow(2., crd.d) ) );
	
	//terceiro, abrevio os valores máximos de coluna e linha
	int max_c, max_r;
	
	//Quarto, abrevio o processed frame que será utilizado
	AVG_PIXEL **info_av1 = NULL;
	AVG_PIXEL **info_old_decoder = NULL;
	switch(crd.d){
		case 0:
			info_old_decoder = GLOBAL_VARIABLES.OLD_P_FRAME.f128;
			info_av1 = GLOBAL_VARIABLES.AV1_P_FRAME.f128;
			max_c = GLOBAL_VARIABLES.OLD_P_FRAME.w128;
			max_r = GLOBAL_VARIABLES.OLD_P_FRAME.h128;
			break;
		case 1:
			info_old_decoder = GLOBAL_VARIABLES.OLD_P_FRAME.f64;
			info_av1 = GLOBAL_VARIABLES.AV1_P_FRAME.f64;
			max_c = GLOBAL_VARIABLES.OLD_P_FRAME.w64;
			max_r = GLOBAL_VARIABLES.OLD_P_FRAME.h64;
			break;
		case 2:
		default:
			info_old_decoder = GLOBAL_VARIABLES.OLD_P_FRAME.f32;
			info_av1 = GLOBAL_VARIABLES.AV1_P_FRAME.f32;
			max_c = GLOBAL_VARIABLES.OLD_P_FRAME.w32;
			max_r = GLOBAL_VARIABLES.OLD_P_FRAME.h32;
			break;
		//case 3:
		//default:
		//	info_old_decoder = GLOBAL_VARIABLES.OLD_P_FRAME.f16;
		//	info_av1 = GLOBAL_VARIABLES.AV1_P_FRAME.f16;
		//	max_c = GLOBAL_VARIABLES.OLD_P_FRAME.w16;
		//	max_r = GLOBAL_VARIABLES.OLD_P_FRAME.h16;
		//	break;
	}
	
	//Quinto, capturo as informações em formato texto, conforme
	char attributes[5000];
	
	//limpando a string
	sprintf(attributes, "");
	
	//ZONA A - insiro as informações que estão na posição de referência no OLD
	seleciona_informacoes(info_old_decoder, c,     r,     max_c, max_r, attributes);
	
	//ZONA B - insiro as informações que estão acima do bloco de referência no OLD
	seleciona_informacoes(info_old_decoder, c,     r - 1, max_c, max_r, attributes);
	
	//ZONA C - insiro as informações que estão acima do bloco de referência no AV1
	seleciona_informacoes(info_av1, c,     r - 1, max_c, max_r, attributes);
	
	//ZONA D - insiro as informações que estão a esquerda do bloco de referência no OLD
	seleciona_informacoes(info_old_decoder, c - 1, r,     max_c, max_r, attributes);
	
	//ZONA E - insiro as informações que estão a esquerda do bloco de referência no AV1
	seleciona_informacoes(info_av1, c - 1, r,     max_c, max_r, attributes);
	
	//Por fim, chama o modelo e retorna uma resposta
	return PY_machine_learning_decision( crd.d, GLOBAL_VARIABLES.icq_value, attributes );
	
}

//Função que é chamada logo no inicio da codificação, que captura os dados externos e armazena localmente
void THESIS_set_global_values(char* model, char* path, unsigned int width, unsigned int height){
	static unsigned char executed = 0;
	if(!executed){
		executed = 1;
		THESIS_initialize(path, width, height, model);
	}
}

//Função que encerra o objeto python
void finalize_python_module(){
	//provavelmente nunca vou usar de verdade essa funcao. 
	//Mas mesmo assim, preciso ter ela e ver se e quando usar
	if(GLOBAL_VARIABLES.py_module != NULL)
		Py_DECREF(GLOBAL_VARIABLES.py_module);
	Py_Finalize();
}

#endif



#if !THESIS_PASS_DEC_ENC
//função que finaliza ponteiros criados ao longo do projeto
void THESIS_finalize(){
	if(GLOBAL_VARIABLES.old_decoder_csv != NULL)
		free(GLOBAL_VARIABLES.old_decoder_csv);	
	
	frame_end(&GLOBAL_VARIABLES.OLD_BUFFER_FRAME);
	frame_end(&GLOBAL_VARIABLES.AV1_BUFFER_FRAME);
	
	free_PF(&GLOBAL_VARIABLES.OLD_P_FRAME);
	free_PF(&GLOBAL_VARIABLES.AV1_P_FRAME);
	
#if THESIS_PASS_TRANSC
	if(Py_IsInitialized())
		finalize_python_module();
#endif
	
}


//função que recebe uma lista de valores de CSV vindos do AV1 e preenche os buffers
void THESIS_update_buffer(){
#if THESIS_PASS_CSV
	if(GLOBAL_VARIABLES.STOP_PRESS)
		return;
#endif

	//Primeira coisa, verificar se há o que ser feito com o CSV do OLD
	CSV old_decoder_select[MAX_SIZE_OF_CSV];
	int old_decoder_select_size = 0;
	int read_ok = old_decoder_select_csv(old_decoder_select, &old_decoder_select_size);
	if(read_ok)
		fill_frame_buffer(old_decoder_select, old_decoder_select_size, &GLOBAL_VARIABLES.OLD_BUFFER_FRAME, 1);
	
	//Depois, preenchemos o buffer do AV1
	fill_frame_buffer(CSV_AV1_SUPERBLOCK, CSV_AV1_SUPERBLOCK_IDX, &GLOBAL_VARIABLES.AV1_BUFFER_FRAME, 0);
	
	if(new_frame()){
		//Após isso, realizar o tratamento necessário para possibilitar a aplicação do modelo de aprendizado de máquina
		
		//Variável que vai conectar o "processa_quadro" com o "dreshape"
		static AVG_PIXEL* tmp = NULL;
		if(tmp == NULL)
			VMALLOC(tmp, GLOBAL_VARIABLES.info_size, AVG_PIXEL);
		
		//DADOS DO OLD
		processa_quadro(tmp, &GLOBAL_VARIABLES.OLD_BUFFER_FRAME);
		dreshape(&GLOBAL_VARIABLES.OLD_P_FRAME, tmp);
		
		//DADOS DO AV1
		processa_quadro(tmp, &GLOBAL_VARIABLES.AV1_BUFFER_FRAME);
		dreshape(&GLOBAL_VARIABLES.AV1_P_FRAME, tmp);
		
		//avisar que o quadro do buffer já foi preenchido ao menos uma vez
		GLOBAL_VARIABLES.buffer_filled_at_once = 1;
#if THESIS_PASS_CSV		
		loop_exporting();
#endif
	}
}

#endif


#if !THESIS_PASS_CSV

//função que recebe uma série de dados proveniente do codificador e armazena na variável temporária do superbloco
void to_csv(int frame_idx, int mi_col, int mi_row, BLOCK_SIZE bsize, int partition_type, int prediction_mode){
	CSV_AV1_SUPERBLOCK[CSV_AV1_SUPERBLOCK_IDX].frame_idx   = frame_idx;
	CSV_AV1_SUPERBLOCK[CSV_AV1_SUPERBLOCK_IDX].mi_col      = mi_col;
	CSV_AV1_SUPERBLOCK[CSV_AV1_SUPERBLOCK_IDX].mi_row      = mi_row;
	CSV_AV1_SUPERBLOCK[CSV_AV1_SUPERBLOCK_IDX].bsize       = bsize;
	CSV_AV1_SUPERBLOCK[CSV_AV1_SUPERBLOCK_IDX].ptype       = partition_type;
	CSV_AV1_SUPERBLOCK[CSV_AV1_SUPERBLOCK_IDX].pmode       = prediction_mode;
	CSV_AV1_SUPERBLOCK[CSV_AV1_SUPERBLOCK_IDX].intra_inter = prediction_mode >= NEARESTMV;

#if THESIS_PASS_DEC_ENC
	export_data(&CSV_AV1_SUPERBLOCK[CSV_AV1_SUPERBLOCK_IDX]);
#endif

	CSV_AV1_SUPERBLOCK_IDX++;

}

void THESIS_get_superblock_tree(PC_TREE *pc_tree, int frame_idx, int mi_col, int mi_row, bool is_root){
	if(is_root){
		CSV_AV1_SUPERBLOCK_IDX = 0;
	}	
	
	const int wbs = mi_size_wide[pc_tree->block_size] / 2;
	if(pc_tree->split[0] != NULL){
		THESIS_get_superblock_tree(pc_tree->split[0], frame_idx, mi_col,       mi_row,       FALSE);
		THESIS_get_superblock_tree(pc_tree->split[1], frame_idx, mi_col + wbs, mi_row,       FALSE);
		THESIS_get_superblock_tree(pc_tree->split[2], frame_idx, mi_col,       mi_row + wbs, FALSE);
		THESIS_get_superblock_tree(pc_tree->split[3], frame_idx, mi_col + wbs, mi_row + wbs, FALSE);
	}
	else if(pc_tree->none != NULL){
		to_csv(frame_idx, mi_col, mi_row, pc_tree->block_size, pc_tree->partitioning, pc_tree->none->mic.mode);
	}
	else if(pc_tree->horizontal[0] != NULL){
		to_csv(frame_idx, mi_col, mi_row, 
		              pc_tree->block_size,
		              pc_tree->partitioning,
		              pc_tree->horizontal[0]->mic.mode);
		to_csv(frame_idx, mi_col, mi_row + wbs, 
		              pc_tree->block_size,
		              pc_tree->partitioning,
		              pc_tree->horizontal[1]->mic.mode);
	}
	else if(pc_tree->vertical[0] != NULL){
		to_csv(frame_idx, mi_col, mi_row, 
		              pc_tree->block_size,
		              pc_tree->partitioning,
		              pc_tree->vertical[0]->mic.mode);
		to_csv(frame_idx, mi_col + wbs, mi_row, 
		              pc_tree->block_size,
		              pc_tree->partitioning,
		              pc_tree->vertical[1]->mic.mode);
	}
	else if(pc_tree->horizontala[0] != NULL){
		to_csv(frame_idx, mi_col      , mi_row, 
		              pc_tree->block_size, 
		              pc_tree->partitioning, 
		              pc_tree->horizontala[0]->mic.mode);
		to_csv(frame_idx, mi_col + wbs, mi_row, 
		              pc_tree->block_size, 
		              pc_tree->partitioning, 
		              pc_tree->horizontala[1]->mic.mode);
		to_csv(frame_idx, mi_col      , mi_row + wbs, 
		              pc_tree->block_size, 
		              pc_tree->partitioning, 
		              pc_tree->horizontala[2]->mic.mode);
	}
	else if(pc_tree->horizontalb[0] != NULL){
		to_csv(frame_idx, mi_col      , mi_row, 
		              pc_tree->block_size, 
		              pc_tree->partitioning, 
		              pc_tree->horizontalb[0]->mic.mode);
		to_csv(frame_idx, mi_col      , mi_row + wbs, 
		              pc_tree->block_size, 
		              pc_tree->partitioning, 
		              pc_tree->horizontalb[1]->mic.mode);
		to_csv(frame_idx, mi_col + wbs, mi_row + wbs, 
		              pc_tree->block_size, 
		              pc_tree->partitioning, 
		              pc_tree->horizontalb[2]->mic.mode);
	}
	else if(pc_tree->verticala[0] != NULL){
		to_csv(frame_idx, mi_col      , mi_row, 
		              pc_tree->block_size, 
		              pc_tree->partitioning, 
		              pc_tree->verticala[0]->mic.mode);
		to_csv(frame_idx, mi_col      , mi_row + wbs, 
		              pc_tree->block_size, 
		              pc_tree->partitioning, 
		              pc_tree->verticala[1]->mic.mode);
		to_csv(frame_idx, mi_col + wbs, mi_row, 
		              pc_tree->block_size, 
		              pc_tree->partitioning, 
		              pc_tree->verticala[2]->mic.mode);
	}
	else if(pc_tree->verticalb[0] != NULL){
		to_csv(frame_idx, mi_col      , mi_row, 
		              pc_tree->block_size, 
		              pc_tree->partitioning, 
		              pc_tree->verticalb[0]->mic.mode);
		to_csv(frame_idx, mi_col + wbs, mi_row, 
		              pc_tree->block_size, 
		              pc_tree->partitioning, 
		              pc_tree->verticalb[1]->mic.mode);
		to_csv(frame_idx, mi_col + wbs, mi_row + wbs,
		              pc_tree->block_size, 
		              pc_tree->partitioning, 
		              pc_tree->verticalb[2]->mic.mode);
	}
	else if(pc_tree->horizontal4[0] != NULL){
		const int q1 = wbs / 2;
		const int q2 = q1 * 3;
		to_csv(frame_idx, mi_col, mi_row, 
		              pc_tree->block_size,
		              pc_tree->partitioning,
		              pc_tree->horizontal4[0]->mic.mode);
		to_csv(frame_idx, mi_col, mi_row + q1, 
		              pc_tree->block_size,
		              pc_tree->partitioning,
		              pc_tree->horizontal4[1]->mic.mode);
		to_csv(frame_idx, mi_col, mi_row + wbs, 
		              pc_tree->block_size,
		              pc_tree->partitioning,
		              pc_tree->horizontal4[2]->mic.mode);
		to_csv(frame_idx, mi_col, mi_row + q2, 
		              pc_tree->block_size,
		              pc_tree->partitioning,
		              pc_tree->horizontal4[3]->mic.mode);
	}
	else if(pc_tree->vertical4[0] != NULL){
		const int q1 = wbs / 2;
		const int q2 = q1 * 3;
		to_csv(frame_idx, mi_col      , mi_row, 
		              pc_tree->block_size,
		              pc_tree->partitioning,
		              pc_tree->vertical4[0]->mic.mode);
		to_csv(frame_idx, mi_col + q1 , mi_row, 
		              pc_tree->block_size,
		              pc_tree->partitioning,
		              pc_tree->vertical4[1]->mic.mode);
		to_csv(frame_idx, mi_col + wbs, mi_row, 
		              pc_tree->block_size,
		              pc_tree->partitioning,
		              pc_tree->vertical4[2]->mic.mode);
		to_csv(frame_idx, mi_col + q2 , mi_row, 
		              pc_tree->block_size,
		              pc_tree->partitioning,
		              pc_tree->vertical4[3]->mic.mode);
	}
}

#endif
