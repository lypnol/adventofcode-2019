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
    char last_char;

    unsigned short streaks[6];
    unsigned short streaks_idx;

    bool is_two_streak;
    bool is_increase;

    for (unsigned int i = low_range; i < hi_range + 1; i++){
        sprintf(candidate, "%d", i);
        last_char = '\0';

        //streaks[0] is never used
        streaks[1] = 1;
        streaks[2] = 1;
        streaks[3] = 1;
        streaks[4] = 1;
        streaks[5] = 1;
        
        streaks_idx = 0;

        is_two_streak = false;
        is_increase = true;

        for (unsigned int j = 0; j < 6; j++)
        {
            if (candidate[j] < last_char) // char are glorified 8bit values, and numbers are in the right order.
            {
                is_increase = false;
                continue; // Early break
            }
            if (candidate[j] == last_char)
                streaks[streaks_idx]++;
            else
                streaks_idx++;
            last_char = candidate[j];
        }
        if ( // Unrolled loop to gain a couple microseconds
            // we never use streaks[0]
            streaks[1] == 2 ||
            streaks[2] == 2 ||
            streaks[3] == 2 ||
            streaks[4] == 2 ||
            streaks[5] == 2
        )
            is_two_streak = true;
        if (is_two_streak && is_increase)
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