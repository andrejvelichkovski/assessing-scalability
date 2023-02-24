#include <stdio.h>
#include <stdlib.h>

const int STREAM_ARRAY_SIZE=10000000;

int main(int argc, char *argv[])
{

    double *a = malloc(10000000 * sizeof(double));
    double *b = malloc(10000000 * sizeof(double));
    double *c = malloc(10000000 * sizeof(double));

	printf("Hello world!\n");

    printf("STARTED");
    int			k;
    int 		j;
    double scalar;
    printf("STREAM version $Revision: 5.10 $\n");

    for (j=0; j<STREAM_ARRAY_SIZE; j++) {
	    a[j] = 1.0;
	    b[j] = 2.0;
	    c[j] = 0.0;
	}


    for (j = 0; j < STREAM_ARRAY_SIZE; j++)
		a[j] = 2.0E0 * a[j];

    /*	--- MAIN LOOP --- repeat test cases NTIMES times --- */

    scalar = 3.0;
    while(1)
	{
        for (j=0; j<STREAM_ARRAY_SIZE; j++)
            c[j] = a[j];

        for (j=0; j<STREAM_ARRAY_SIZE; j++)
            b[j] = scalar*c[j];

        for (j=0; j<STREAM_ARRAY_SIZE; j++)
            c[j] = a[j]+b[j];

        for (j=0; j<STREAM_ARRAY_SIZE; j++)
            a[j] = b[j]+scalar*c[j];
	}
	return 0;
}
