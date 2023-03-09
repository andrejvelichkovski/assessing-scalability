#include <stdio.h>
#include <stdlib.h>


int main(int argc, char *argv[])
{

	printf("Starting benchmark.\n");

	while(1) {
		FILE *fp;

	   	fp = fopen("app/bench-file.txt", "w");

//		char random_letter = 33 + (rand() % 93);
//		fprintf(fp, "%c\n", random_letter);
	   	
	   	fclose(fp);
	   	
//	   	printf("Step\n");
	}
	return 0;
}
