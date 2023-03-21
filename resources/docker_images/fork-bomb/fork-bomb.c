#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

int main()
{
    while(1)
    {
        int child_id = fork();
        if(child_id > 0) {
            wait(NULL);
        }
    	else if (child_id==0){
		    exit(0);
	    }
	    else {
	    	printf("ERROR %d\n", child_id);
	    	exit(1);
	    }
    }
    return 0;
}
