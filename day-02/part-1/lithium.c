#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>

int run(char* str) {
    int array[200]; // good enough for the demo
    int last_idx = 0;

    char delim[] = ",";
	char *ptr = strtok(str, delim);

	while(ptr != NULL)
	{
		array[last_idx++] = atoi(ptr);
		ptr = strtok(NULL, delim);
	}

    // AoC quality bug fixing
    array[1] = 12;
    array[2] = 2;
    
    for (int i = 0; i < last_idx; i+=4){
        int opcode = array[i];
        switch(opcode){
            case 1:{
                array[array[i+3]] = array[array[i+1]] + array[array[i+2]];
                continue;
            }
            case 2:{
                array[array[i+3]] = array[array[i+1]] * array[array[i+2]];
                continue; // Otherwise we might execute this opcode again
            }
            case 99:{
                return array[0];
            }
        }
    }
    return 0; // Oops
}

int main(int argc, char** argv)
{
    clock_t start = clock();
    int answer = run(argv[1]);
    printf("_duration:%f\n%d\n", (float)( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC, answer);
    return 0;
}
