#include <stdio.h>
#include <time.h>
#include <stdlib.h>

struct orbit{
    int name;
    int parent;
};

struct planet{
    int name;
    int depth;
};

typedef struct orbit orbit;
typedef struct planet planet;

int hash(char word[3]){
    return ('Z' * 'Z' * word[0] + 1) + ('Z' * word[1] + 1) + word[2]; // hi quality, collision-free
}

// int quickatoi(char word[3]){
//     return 100 * (word[0] - 48) + 10 * (word[1] - 48) + word[2] - 48;
// }

int run(char* s) {
    int max = 2000;
    char c = 'a';

    char word_a[3];
    char word_b[3];

    orbit orbits[max];
    int orbit_index = 0;

    orbit tmp;

    while (c != '\0'){
        word_a[0] = s++[0];
        word_a[1] = s++[0];
        word_a[2] = s++[0];
        s++;
        word_b[0] = s++[0];
        word_b[1] = s++[0];
        word_b[2] = s++[0];

        tmp.parent = hash(word_a);
        tmp.name = hash(word_b);
        orbits[orbit_index++] = tmp;

        c = s++[0];
    }
    planet planets[max];
    int planet_index = 0;
    planet tmplanet;
    tmplanet.name = hash("COM");
    tmplanet.depth = 0;
    planets[planet_index++] = tmplanet;

    int should_run = 1;

    while (should_run){
        should_run = 0;
        for (int i = 0; i < orbit_index; i++){
            for (int j = 0; j < planet_index; j++){
                if (planets[j].name == orbits[i].parent){
                    tmplanet.name = orbits[i].name;
                    tmplanet.depth = planets[j].depth + 1;
                    planets[planet_index++] = tmplanet;
                    orbits[i].parent = 0;
                    orbits[i].name = 0;
                    should_run = 1;
                }
            }
        }
    }

    int out = 0;
    
    for(int i = 0; i < planet_index; i++){
        out += planets[i].depth;
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
