#include <stdio.h>

int main() {
        printf("Hello world\n");
        while(1) {
                for(int i=2;i<=100000000;i++) {
                        int flag=0;
                        for(int j=2;j<=i/2;j++) {
                                if(i%j==0) {
                                        flag=1;
                                        break;
                                }
                        }
                }

        }
        return 0;
}