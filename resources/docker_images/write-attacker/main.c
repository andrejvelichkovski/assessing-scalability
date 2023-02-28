#include <stdio.h>
#include <stdlib.h>

const int FILE_SIZE = 4096 * 4096 * 4;

int main() {
   	while(1) {
   		printf("STEP\n");
   	   	FILE *fp = fopen("bench-file.txt", "w");
	   	for(int i=0;i<FILE_SIZE;i++) {
	   		char random_letter = 33 + (rand() % 93);
	   		fprintf(fp, "%c\n", random_letter);
	   	}
	   	fclose(fp);
	}
}