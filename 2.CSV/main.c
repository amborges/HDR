#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "THESIS.h"

int main(int argc, char** argv){
	int width = atoi(argv[1]);
	int height = atoi(argv[2]);
	int FTBE  = atoi(argv[3]);
	char* in_path = argv[4];
	char* out_path = argv[5];
	
	THESIS_initialize(width, height, FTBE, in_path, out_path);
	
	while(THESIS_read_av1_file()){
		THESIS_update_buffer();
	}
	
	THESIS_finalize();
	return 0;
}
