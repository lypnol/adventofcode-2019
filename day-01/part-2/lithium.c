#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>

int run(char* s) {
    int counter = 0;
    int fuel = 0;

    const char delim[] = "\n";
	char *ptr = strtok(s, delim);

	while(ptr != NULL)
	{
        fuel = (atoi(ptr) / 3) - 2;
        while (fuel > 0){
            counter += fuel;
            fuel = (fuel / 3) - 2;
        }
		ptr = strtok(NULL, delim);
	}
    return counter;
}

int main(int argc, char** argv)
{
    clock_t start = clock();
    int answer = run(argv[1]);
    
    printf("_duration:%f\n%d\n", (float)( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC, answer);
    return 0;
}
