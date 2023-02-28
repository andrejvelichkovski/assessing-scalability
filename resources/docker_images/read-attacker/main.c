#include <stdio.h>
#include <stdlib.h>

const int FILE_SIZE = 4096 * 4096;

int main() {
	
	printf("Starting to prepare benchmark file.\n");

	FILE *fp;

   	fp = fopen("bench-file.txt", "w");

   	for(int i=0;i<FILE_SIZE;i++) {
   		char random_letter = 33 + (rand() % 93);
   		fprintf(fp, "%c\n", random_letter);
   	}

   	fclose(fp);

	printf("Benchmark file preparation done.\n");

   	while(1) {
	   	fp = fopen("bench-file.txt", "r");

	   	printf("STEP \n");

   	    char * line = NULL;
    	size_t len = 0;
    	ssize_t read;

	   	while ((read = getline(&line, &len, fp)) != -1) {
	   		;
	    }

	    fclose(fp);
	}
}