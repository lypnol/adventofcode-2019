#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned int bool;
#define true 1;
#define false 0;

int* parse(char* str){
    int *array;
    array = (int *)malloc(sizeof(int) * 1000);
    int last_idx = 0;

    char delim[] = ",";
	char *ptr = strtok(str, delim);

	while(ptr != NULL)
	{
		array[last_idx++] = atoi(ptr);
		ptr = strtok(NULL, delim);
	}
    return array;
}


int run_one(int *array, int input_1, int input_2) {

    int opcode;
    bool mode_1 = false;
    bool mode_2 = false;
    // bool parameter_3_mode = false; // unused

    bool first_input = true;
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
                array[array[i+1]] = (first_input?input_1:input_2);
                first_input = false;
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

int run(char* str){
    int best = 0;
    const int number_of_permutations = 120;
    const int permutations[120][5] = {
        {0,1,2,3,4},
        {1,0,2,3,4},
        {2,0,1,3,4},
        {0,2,1,3,4},
        {1,2,0,3,4},
        {2,1,0,3,4},
        {2,1,3,0,4},
        {1,2,3,0,4},
        {3,2,1,0,4},
        {2,3,1,0,4},
        {1,3,2,0,4},
        {3,1,2,0,4},
        {3,0,2,1,4},
        {0,3,2,1,4},
        {2,3,0,1,4},
        {3,2,0,1,4},
        {0,2,3,1,4},
        {2,0,3,1,4},
        {1,0,3,2,4},
        {0,1,3,2,4},
        {3,1,0,2,4},
        {1,3,0,2,4},
        {0,3,1,2,4},
        {3,0,1,2,4},
        {4,0,1,2,3},
        {0,4,1,2,3},
        {1,4,0,2,3},
        {4,1,0,2,3},
        {0,1,4,2,3},
        {1,0,4,2,3},
        {1,0,2,4,3},
        {0,1,2,4,3},
        {2,1,0,4,3},
        {1,2,0,4,3},
        {0,2,1,4,3},
        {2,0,1,4,3},
        {2,4,1,0,3},
        {4,2,1,0,3},
        {1,2,4,0,3},
        {2,1,4,0,3},
        {4,1,2,0,3},
        {1,4,2,0,3},
        {0,4,2,1,3},
        {4,0,2,1,3},
        {2,0,4,1,3},
        {0,2,4,1,3},
        {4,2,0,1,3},
        {2,4,0,1,3},
        {3,4,0,1,2},
        {4,3,0,1,2},
        {0,3,4,1,2},
        {3,0,4,1,2},
        {4,0,3,1,2},
        {0,4,3,1,2},
        {0,4,1,3,2},
        {4,0,1,3,2},
        {1,0,4,3,2},
        {0,1,4,3,2},
        {4,1,0,3,2},
        {1,4,0,3,2},
        {1,3,0,4,2},
        {3,1,0,4,2},
        {0,1,3,4,2},
        {1,0,3,4,2},
        {3,0,1,4,2},
        {0,3,1,4,2},
        {4,3,1,0,2},
        {3,4,1,0,2},
        {1,4,3,0,2},
        {4,1,3,0,2},
        {3,1,4,0,2},
        {1,3,4,0,2},
        {2,3,4,0,1},
        {3,2,4,0,1},
        {4,2,3,0,1},
        {2,4,3,0,1},
        {3,4,2,0,1},
        {4,3,2,0,1},
        {4,3,0,2,1},
        {3,4,0,2,1},
        {0,4,3,2,1},
        {4,0,3,2,1},
        {3,0,4,2,1},
        {0,3,4,2,1},
        {0,2,4,3,1},
        {2,0,4,3,1},
        {4,0,2,3,1},
        {0,4,2,3,1},
        {2,4,0,3,1},
        {4,2,0,3,1},
        {3,2,0,4,1},
        {2,3,0,4,1},
        {0,3,2,4,1},
        {3,0,2,4,1},
        {2,0,3,4,1},
        {0,2,3,4,1},
        {1,2,3,4,0},
        {2,1,3,4,0},
        {3,1,2,4,0},
        {1,3,2,4,0},
        {2,3,1,4,0},
        {3,2,1,4,0},
        {3,2,4,1,0},
        {2,3,4,1,0},
        {4,3,2,1,0},
        {3,4,2,1,0},
        {2,4,3,1,0},
        {4,2,3,1,0},
        {4,1,3,2,0},
        {1,4,3,2,0},
        {3,4,1,2,0},
        {4,3,1,2,0},
        {1,3,4,2,0},
        {3,1,4,2,0},
        {2,1,4,3,0},
        {1,2,4,3,0},
        {4,2,1,3,0},
        {2,4,1,3,0},
        {1,4,2,3,0},
        {4,1,2,3,0}
    }; // yes. got to go fast

    int *amp_code = parse(str);
    int *working_copy = (int *)malloc(sizeof(int) * 1000);
    memcpy(working_copy, amp_code, 1000*sizeof(int));

    int amp_input;
    for (int i = 0; i < number_of_permutations; i++){
        //printf("%d %d %d %d %d\n", permutations[i][0],permutations[i][1],permutations[i][2],permutations[i][3],permutations[i][4]);
        amp_input = 0;
        for (int phase = 0; phase < 5; phase ++){
            memcpy(working_copy, amp_code, 1000*sizeof(int)); // initialize program copy
            amp_input = run_one(working_copy, permutations[i][phase], amp_input);
        }
        if (amp_input > best){
            best = amp_input;
        }
    }
    return best;
}

int main(int argc, char** argv)
{
    clock_t start = clock();
    int answer = run(argv[1]);
    printf("_duration:%f\n%d\n", (float)( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC, answer);
    return 0;
}
