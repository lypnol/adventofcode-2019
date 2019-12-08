#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned int bool;
#define true 1;
#define false 0;

int run(char* str) {
    int array[10000]; // good enough for the demo
    int last_idx = 0;

    char delim[] = ",";
	char *ptr = strtok(str, delim);

	while(ptr != NULL)
	{
		array[last_idx++] = atoi(ptr);
		ptr = strtok(NULL, delim);
	}
    int opcode;
    bool mode_1 = false;
    bool mode_2 = false;
    // bool parameter_3_mode = false; // unused
    int i = 0;

    int out = -1;

    while (1){
        opcode = array[i] % 100;
        mode_1 = (array[i] / 100) % 10 == 1;
        mode_2 = (array[i] / 1000) % 10 == 1;
        // parameter_3_mode = (array[i] / 10000) % 10 == 1; // unused
        switch(opcode){
            case 1:{
                // ADD
                array[array[i+3]] = (mode_1?array[i+1]:array[array[i+1]]) + (mode_2?array[i+2]:array[array[i+2]]);
                i+=4;
                continue;
            }
            case 2:{
                // MULT
                array[array[i+3]] = (mode_1?array[i+1]:array[array[i+1]]) * (mode_2?array[i+2]:array[array[i+2]]);
                i+=4;
                continue;
            }
            case 3:{
                // IN
                array[array[i+1]] = 5;
                i+=2;
                continue;
            }
            case 4:{
                // OUT
                out = array[array[i+1]];
                i+=2;
                continue;
            }
            case 5:{
                // JZ
                if ((mode_1?array[i+1]:array[array[i+1]]) == 0){
                    i+=3;
                }
                else{
                    i = mode_2?array[i+2]:array[array[i+2]];
                }
                continue;
            }
            case 6:{
                // JNZ
                if ((mode_1?array[i+1]:array[array[i+1]]) == 0){
                    i = mode_2?array[i+2]:array[array[i+2]];
                }
                else{
                    i+=3;
                }
                continue;
            }
            case 7:{
                // LT
                if ((mode_1?array[i+1]:array[array[i+1]]) < (mode_2?array[i+2]:array[array[i+2]])){
                    array[array[i+3]] = 1;
                }
                else{
                    array[array[i+3]] = 0;
                }
                i+=4;
                continue;
            }
            case 8:{
                // EQ
                if ((mode_1?array[i+1]:array[array[i+1]]) == (mode_2?array[i+2]:array[array[i+2]])){
                    array[array[i+3]] = 1;
                }
                else{
                    array[array[i+3]] = 0;
                }
                i+=4;
                continue;
            }
            case 99:{
                // END
                return out;
            }
        }
    }
    return out;
}

int main(int argc, char** argv)
{
    clock_t start = clock();
    int answer = run(argv[1]);
    printf("_duration:%f\n%d\n", (float)( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC, answer);
    return 0;
}
