#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* struct of pgm file */
typedef struct pgmData{
	int row_max;
	int col_max;
	char version[3];
	int maxValue;
	int **data_matrix;
}PGMdata;

/* skip comments */
void comments(FILE *fp){
    int tempc;
  
    while ((tempc = fgetc(fp)) != EOF && isspace(tempc)) {
        ;
    }
    fseek(fp, -1, SEEK_CUR);
   
    if(tempc == '#'){
    	while(fgetc(fp) != '\n'){
    		;
		}  
    } 

} 

/* read pgm file */
void readPGM(char path[], PGMdata *pgm){
	FILE * fp;
	char tempc;
	int i;
	int j;
	
	fp = fopen(path, "rb");
    if (fp == NULL) {
        printf("\nCan not open file to read\n");
        exit(1);
    }
     	
	comments(fp);
	fgets(pgm->version, sizeof(pgm->version), fp);
	comments(fp);
	fscanf(fp, "%d", &pgm->col_max);
	comments(fp);
	fscanf(fp, "%d", &pgm->row_max);
	comments(fp);
	fscanf(fp, "%d", &pgm->maxValue);
	comments(fp);
 	
	pgm->data_matrix = (int **) malloc(sizeof(int *) * pgm->row_max);
	if (pgm->data_matrix == NULL) {
        printf("\nMemory allocation failure\n");
        exit(1);
    }
	for(i=0; i<pgm->row_max; i++){
		pgm->data_matrix[i] = (int *) malloc(sizeof(int) * pgm->col_max);
		if (pgm->data_matrix[i] == NULL) {
        	printf("\nMemory allocation failure\n");
        	exit(1);
		}
	}

	if(strcmp(pgm->version,"P2") == 0){
		for(i=0; i<pgm->row_max; i++){
			for(j=0; j<pgm->col_max; j++){
				fscanf(fp, "%d", &pgm->data_matrix[i][j]);
			}
		}		
		printf("\nReading P2 successful\n");
	}
	else if(strcmp(pgm->version,"P5") == 0){
		for(i=0; i<pgm->row_max; i++){
			for(j=0; j<pgm->col_max; j++){
				fscanf(fp, "%c", &tempc);
				pgm->data_matrix[i][j] = (int)tempc;
			}
		}	
		printf("\nReading P5 successful\n");
	}
	else{
		printf("\nUnknown format\n");
	}

	fclose(fp);
}

/* write pgm file */
void writePGM(char path[], PGMdata *pgm, int **data_matrix){
	FILE * fp;
	int i;
	int j;
	int temp;
	
	fp = fopen(path, "wb");
    if (fp == NULL) {
        printf("\nCan not open file to read\n");
        exit(1);
    }
  	
	fprintf(fp, "%s\n", pgm->version);
    fprintf(fp, "%d %d \n", pgm->col_max, pgm->row_max);
    fprintf(fp, "%d\n", pgm->maxValue);
   
    if(strcmp(pgm->version, "P2") == 0){
	    for(i=0; i<pgm->row_max; i++){
	    	for(j=0; j<pgm->col_max; j++){
	    		fprintf(fp, "%d ", data_matrix[i][j]);
			}
		}
		printf("Writing (P2 ");
	}
	else if(strcmp(pgm->version, "P5") == 0){
	    for(i=0; i<pgm->row_max; i++){
	    	for(j=0; j<pgm->col_max; j++){
	    		temp = data_matrix[i][j];
	    		fprintf(fp, "%c", (unsigned char)temp);
			}
		}
		printf("Writing (P5 ");
	}
	else{
		printf("Unknown format\n");		
	}

	
	fclose(fp);
}

/* set avarage filter matris */
int setFilterMatrisAvarage(int **filter_matrix, int row, int col, int **data_matrix, int N){
	int i;
	int j;
	int i_filter=0;
	int j_filter=0;
	int avarage = 0;
  
	for(i=row-N/2; i<=row+N/2; i++){
		j_filter = 0;
		for(j=col-N/2; j<=col+N/2; j++){
			filter_matrix[i_filter][j_filter] = data_matrix[i][j];
			avarage += filter_matrix[i_filter][j_filter];
			j_filter++;
		}
		i_filter++;
	}
	
	avarage /= (N*N);
	
	return avarage;
}

/* set median filter matris */
int setFilterMatrisMedian(int **filter_matrix, int row, int col, int *median, int **data_matrix, int N){
	int i;
	int j;
	int i_filter=0;
	int j_filter=0;
	int count = 0;
	int temp;
    
	for(i=row-N/2; i<=row+N/2; i++){
		j_filter = 0;
		for(j=col-N/2; j<=col+N/2; j++){
			filter_matrix[i_filter][j_filter] = data_matrix[i][j];
			median[count] = filter_matrix[i_filter][j_filter];
			j_filter++;
			count++;
		}
		i_filter++;
	}
	
	// median
	for(i=0; i<=N*N/2; i++){
		for(j=i+1; j<N*N; j++){
			if(median[i]>median[j]){
				temp = median[i];
				median[i] = median[j];
				median[j] = temp;
			}
		}
	}
	
	return median[N*N/2];
}

/* avarage filter */
void avarageFilter(char file_path[], int **filter_matrix, PGMdata *pgm, int N){
	int i;
	int j;
	char path_new[100];
	int **dataMatrix;

	dataMatrix = (int **) malloc(sizeof(int *) * pgm->row_max);
	if (dataMatrix == NULL) {
        printf("\nMemory allocation failure\n");
        exit(1);
    }
	for(i=0; i<pgm->row_max; i++){
		dataMatrix[i] = (int *) malloc(sizeof(int) * pgm->col_max);
		if (dataMatrix[i] == NULL) {
        	printf("\nMemory allocation failure\n");
        	exit(1);
		}
	}
	
	for(i=0; i<pgm->row_max; i++){
		for(j=0; j<pgm->col_max; j++){
			dataMatrix[i][j] = pgm->data_matrix[i][j];
		}
	}

	for(i=N/2; i<pgm->row_max-N/2; i++){
		for(j=N/2; j<pgm->col_max-N/2; j++){
			dataMatrix[i][j] = setFilterMatrisAvarage(filter_matrix, i, j, dataMatrix, N);
		}
	}

	i=0;
	while(file_path[i] != '\0' && file_path[i] != '.'){
		path_new[i] = file_path[i];
		i++;
	}
	path_new[i] = '\0';

	// write file
	strcat(path_new, "_avarage.pgm");
	writePGM(path_new, pgm, dataMatrix);
	printf("avarage) is succesful\n");
	
	// free allocated
	for(i=0; i<N; i++){
		free(dataMatrix[i]);
	}
	free(dataMatrix);
}

/* median filter */
void medianFilter(char file_path[], int **filter_matrix, PGMdata *pgm, int N){
	int i;
	int j;
	char path_new[100];
	int *median;
	int **dataMatrix;

	dataMatrix = (int **) malloc(sizeof(int *) * pgm->row_max);
	if (dataMatrix == NULL) {
        printf("\nMemory allocation failure\n");
        exit(1);
    }
	for(i=0; i<pgm->row_max; i++){
		dataMatrix[i] = (int *) malloc(sizeof(int) * pgm->col_max);
		if (dataMatrix[i] == NULL) {
        	printf("\nMemory allocation failure\n");
        	exit(1);
		}
	}
	
	for(i=0; i<pgm->row_max; i++){
		for(j=0; j<pgm->col_max; j++){
			dataMatrix[i][j] = pgm->data_matrix[i][j];
		}
	}
	
	median = (int *)malloc(sizeof(int) * N *N);
	
	for(i=N/2; i<pgm->row_max-N/2; i++){
		for(j=N/2; j<pgm->col_max-N/2; j++){
			dataMatrix[i][j] = setFilterMatrisMedian(filter_matrix, i, j, median, dataMatrix, N);
		}
	}
	
	i=0;
	while(file_path[i] != '\0' && file_path[i] != '.'){
		path_new[i] = file_path[i];
		i++;
	}
	path_new[i] = '\0';
	
	// write file
	strcat(path_new, "_median.pgm");	
	writePGM(path_new, pgm, dataMatrix);
	printf("median) is succesful\n");
	
	// free allocated
	free(median);
	for(i=0; i<N; i++){
		free(dataMatrix[i]);
	}
	free(dataMatrix);
}

int main(){
	PGMdata *pgm;
	char file_path [100];
	int **filterMatrix;
	int i;
	int N;
	
	printf("Please enter the file path: ");
	scanf("%s", &file_path);

	/* number of filter matrix */	
	printf("Enter the size of the filter matrix (3, 5, 7 etc.): ");
	scanf("%d", &N);
	
	/* allocated */
	pgm = (PGMdata *) malloc(sizeof(PGMdata));
	filterMatrix = (int **) malloc(sizeof(int*) * N);
	for(i=0; i<N; i++){
		filterMatrix[i] = (int *) malloc(sizeof(int) * N);
	}
	
	/* run program */
	readPGM(file_path, pgm);	
	avarageFilter(file_path, filterMatrix, pgm, N);
	medianFilter(file_path, filterMatrix, pgm, N);
	
	/* free allocated */
	for(i=0; i<N; i++){
		free(filterMatrix[i]);
	}
	free(filterMatrix);
	for(i=0; i<pgm->row_max; i++){
		free(pgm->data_matrix[i]);
	}
	free(pgm->data_matrix);		
	free(pgm);
	
	return 0;
}
