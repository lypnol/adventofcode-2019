#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>

struct segment {
    int start;
    int end;
    int offset;
    // int initial_distance; // shh, part 2
};
typedef struct segment segment;

int run(char* str){
    segment *hor_segments_1;
    segment *ver_segments_1;

    hor_segments_1 = (segment *)malloc(sizeof(segment)*200);
    ver_segments_1 = (segment *)malloc(sizeof(segment)*200);

    segment *hor_segments_2;
    segment *ver_segments_2;

    hor_segments_2 = (segment *)malloc(sizeof(segment)*200);
    ver_segments_2 = (segment *)malloc(sizeof(segment)*200);

    int hor_index_1 = 0;
    int ver_index_1 = 0;

    int hor_index_2 = 0;
    int ver_index_2 = 0;

    int last_x = 0;
    int last_y = 0;

    const char *line_separator = "\n";
    const char *token_separator = ",";

    char *line1 = strtok(str, line_separator); // line 1
    char *line2 = strtok(NULL, line_separator); // line 2

    char *token_line_1 = strtok(line1, token_separator);

    int best = __INT_MAX__;
    segment tmp;

    while (token_line_1 != NULL) {
        int value = atoi(token_line_1 + 1);
        switch(token_line_1[0]){
            case 'R':{
                tmp.start = last_x;
                last_x += value;
                tmp.end = last_x;
                tmp.offset = last_y;
                hor_segments_1[hor_index_1++] = tmp;
                break;
            }
            case 'L':{
                tmp.end = last_x;
                last_x -= value;
                tmp.start = last_x;
                tmp.offset = last_y;
                hor_segments_1[hor_index_1++] = tmp;
                break;
            }
            case 'U':{
                tmp.start = last_y;
                last_y += value;
                tmp.end = last_y;
                tmp.offset = last_x;
                ver_segments_1[ver_index_1++] = tmp;
                break;
            }
            case 'D':{
                tmp.end = last_y;
                last_y -= value;
                tmp.start = last_y;
                tmp.offset = last_x;
                ver_segments_1[ver_index_1++] = tmp;
                break;
            }
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
                tmp.start = last_x;
                last_x += value;
                tmp.end = last_x;
                tmp.offset = last_y;
                hor_segments_2[hor_index_2++] = tmp;
                break;
            }
            case 'L':{
                tmp.end = last_x;
                last_x -= value;
                tmp.start = last_x;
                tmp.offset = last_y;
                hor_segments_2[hor_index_2++] = tmp;
                break;
            }
            case 'U':{
                tmp.start = last_y;
                last_y += value;
                tmp.end = last_y;
                tmp.offset = last_x;
                ver_segments_2[ver_index_2++] = tmp;
                break;
            }
            case 'D':{
                tmp.end = last_y;
                last_y -= value;
                tmp.start = last_y;
                tmp.offset = last_x;
                ver_segments_2[ver_index_2++] = tmp;
                break;
            }
        }
        token_line_2 = strtok(NULL, token_separator);
    }

    for (int hor_1 = 0; hor_1 < hor_index_1; hor_1++){
        for (int ver_2 = 0; ver_2 < ver_index_2; ver_2++){
            if 
            (
                hor_segments_1[hor_1].start <= ver_segments_2[ver_2].offset &&
                hor_segments_1[hor_1].end >= ver_segments_2[ver_2].offset &&
                ver_segments_2[ver_2].start <= hor_segments_1[hor_1].offset &&
                ver_segments_2[ver_2].end >= hor_segments_1[hor_1].offset
            )
            {
                if (abs(ver_segments_2[ver_2].offset) + abs(hor_segments_1[hor_1].offset) < best){
                    best = abs(ver_segments_2[ver_2].offset) + abs(hor_segments_1[hor_1].offset);
                }
            }
        }
    }
    for (int hor_2 = 0; hor_2 < hor_index_2; hor_2++){
        for (int ver_1 = 0; ver_1 < ver_index_1; ver_1++){
            if 
            (
                hor_segments_2[hor_2].start <= ver_segments_1[ver_1].offset &&
                hor_segments_2[hor_2].end >= ver_segments_1[ver_1].offset &&
                ver_segments_1[ver_1].start <= hor_segments_2[hor_2].offset &&
                ver_segments_1[ver_1].end >= hor_segments_2[hor_2].offset
            )
            {
                if (abs(hor_segments_2[hor_2].offset) + abs(ver_segments_1[ver_1].offset) < best){
                    best = abs(ver_segments_1[ver_1].offset) + abs(hor_segments_2[hor_2].offset);
                }
            }
        }
    }
    free(hor_segments_1);
    free(hor_segments_2);
    free(ver_segments_1);
    free(ver_segments_2);
    return best;
}

int main(int argc, char** argv)
{
    clock_t start = clock();
    int answer = run(argv[1]);
    
    printf("_duration:%f\n%d\n", (float)( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC, answer);
    return 0;
}
