#include <stdio.h>
#include <sys/types.h>

int main()
{
    while(1)
    {
	printf("starting new system\n");
    	fork();
    	sleep(0.1);
    }
    return 0;
}
