#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>

int coords(int x, int y){
    return (30000 * (x + 15000)) + (y + 15000);
}

int run(char* str){
    int *space;
    space = (int *)malloc(sizeof(int)*30000*30000);

    int last_x = 0;
    int last_y = 0;

    const char *line_separator = "\n";
    const char *token_separator = ",";

    char *line1 = strtok(str, line_separator); // line 1
    char *line2 = strtok(NULL, line_separator); // line 2

    char *token_line_1 = strtok(line1, token_separator);

    int modx = 0;
    int mody = 0;

    int best = __INT_MAX__;

    while (token_line_1 != NULL) {
        int value = atoi(token_line_1 + 1);
        switch(token_line_1[0]){
            case 'R':{
                modx = 1;
                mody = 0;
                break;
            }
            case 'L':{
                modx = -1;
                mody = 0;
                break;
            }
            case 'U':{
                modx = 0;
                mody = 1;
                break;
            }
            case 'D':{
                modx = 0;
                mody = -1;
                break;
            }
        }
        for(int i = 0; i < value; i++){
            last_x += modx;
            last_y += mody;
            //printf("(%d:%d)\n", last_x, last_y);
            space[coords(last_x, last_y)] = 1;
        }
        token_line_1 = strtok(NULL, token_separator);
    }
    last_x = 0;
    last_y = 0;

    char *token_line_2 = strtok(line2, token_separator);
    while (token_line_2 != NULL) {
        int value = atoi(token_line_2 + 1);
        switch(token_line_2[0]){
            case 'R':{
                modx = 1;
                mody = 0;
                break;
            }
            case 'L':{
                modx = -1;
                mody = 0;
                break;
            }
            case 'U':{
                modx = 0;
                mody = 1;
                break;
            }
            case 'D':{
                modx = 0;
                mody = -1;
                break;
            }
        }
        for(int i = 0; i < value; i++){
            last_x += modx;
            last_y += mody;
            if (space[coords(last_x, last_y)] == 1){
                int distance = abs(last_x) + abs(last_y);
                if (distance < best){
                    best = distance;
                }
            }
            //printf("(%d:%d)\n", last_x-5000,last_y-5000);
        }
        token_line_2 = strtok(NULL, token_separator);
    }

    free(space);
    return best;
}

int main(int argc, char** argv)
{
    clock_t start = clock();
    int answer = run(argv[1]);
    
    printf("_duration:%f\n%d\n", (float)( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC, answer);
    return 0;
}
