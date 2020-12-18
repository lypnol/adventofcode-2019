#include <iostream>
#include <ctime>

#define WIDTH 25
#define HEIGHT 6

using namespace std;

int run(char* s) {
    int i = -1, j = 0;
    int res = 0;
    int min_zeros = WIDTH*HEIGHT;
    while (s[j]) {
        i = j;
        j += WIDTH*HEIGHT;
        int zeros = 0, ones = 0, twos = 0;
        for (int k = i; k < j; k++) {
            if (s[k] == '0') zeros++;
            else if (s[k] == '1') ones++;
            else if (s[k] == '2') twos++;
        }
        if (zeros < min_zeros) {
            min_zeros = zeros;
            res = ones*twos;
        }
    }

    return res;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        cout << "Missing one argument" << endl;
        exit(1);
    }

    clock_t start = clock();
    int answer = run(argv[1]);
    
    cout << "_duration:" << float( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC << "\n";
    cout << answer << "\n";
    return 0;
}
