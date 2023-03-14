#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
 
int main(int argc, char **argv)
{
    int FILE_SIZE = 40;
    FILE *fp = fopen("app/bench-file.txt", "w");
    for(int i=0;i<FILE_SIZE;i++) {
        char random_letter = 33 + (rand() % 93);
        fprintf(fp, "%c\n", random_letter);
    }
    fclose(fp);
    printf("File ready\n");

    char file_name[] = "app/bench-file.txt";
 
    while(1) {
    	struct stat fileStat;
    	if(stat(file_name,&fileStat) < 0)    
        	return 1; 
        	
        printf("Information for %s\n",file_name);
    printf("---------------------------\n");
    printf("File Size: \t\t%d bytes\n",fileStat.st_size);
    printf("Number of Links: \t%d\n",fileStat.st_nlink);
    printf("File inode: \t\t%d\n",fileStat.st_ino);
    }
    return 0;
}
