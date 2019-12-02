#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>

int run(char* str){
    int array[200]; // good enough for the demo
    int base_array[200]; // good enough for the demo

    int last_idx = 0;

    char delim[] = ",";
	char *ptr = strtok(str, delim);

	while(ptr != NULL)
	{
        int value = atoi(ptr);
        base_array[last_idx] = value;
		array[last_idx++] = value;
		ptr = strtok(NULL, delim);
	}
    
    for(int verb = 0; verb < 100; verb ++){
        for(int noun = 0; noun < 100; noun ++){
            int i = 0;
            memcpy(array, base_array, 200*sizeof(int));
            array[1] = noun;
            array[2] = verb;
            int done = 0;
            while(!done){
                switch(array[i]){
                    case 1:{
                        array[array[i+3]] = array[array[i+1]] + array[array[i+2]];
                        i+=4;
                        continue;
                    }
                    case 2:{
                        array[array[i+3]] = array[array[i+1]] * array[array[i+2]];
                        i+=4;
                        continue;
                    }
                    case 99:{
                        done = 1;
                        continue;
                    }
                }
            }
            if (array[0] ==  19690720){
                return 100 * noun + verb;
            }
        }
    }
    return 0; //Oops
}

int main(int argc, char** argv)
{
    clock_t start = clock();
    int answer = run(argv[1]);
    printf("_duration:%f\n%d\n", (float)( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC, answer);
    return 0;
}