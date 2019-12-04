#include <stdio.h>
#include <time.h>
#include <stdlib.h>

typedef unsigned int bool;
#define true 1;
#define false 0;

unsigned int run(char* s) {
    unsigned int hi_range = atoi(s + 7);
    s[6] = '\0'; // Quickest way to "substring"
    unsigned int low_range = atoi(s);
    
    unsigned int valid = 0;
    char candidate[7];
    char last_char = '\0';

    bool is_consecutive = false;
    bool is_increase = true;
    
    for (unsigned int i = low_range; i < hi_range; i++){
        sprintf(candidate, "%d", i);

        last_char = '\0';
        is_consecutive = false;
        is_increase = true;

        for (unsigned int j = 0; j < 6; j++){
            if (candidate[j] < last_char) // char are glorified 8bit values, and numbers are in the right order.
            {
                is_increase = false;
                break; // Early break
            }
            if (candidate[j] == last_char)
                is_consecutive = true;
            last_char = candidate[j];
        }
        if (is_consecutive && is_increase)
            valid++;
    }
    return valid;
}

int main(int argc, char** argv)
{

    clock_t start = clock();
    unsigned int answer = run(argv[1]);
    
    printf("_duration:%f\n%d\n", (float)( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC, answer);
    return 0;
}
