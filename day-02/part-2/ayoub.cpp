#include <iostream>
#include <sstream>
#include <string>
#include <ctime>

using namespace std;

string run(string s) {
    istringstream ss(s);
    string curr;
    size_t N = count(s.begin(), s.end(), ',')+1;
    size_t code[N], initial[N], i = -1, x = 0, y = 0;

    while (getline(ss, curr, ',')) {
        code[++i] = (size_t)stoi(curr);
        initial[i] = code[i];
    }

    for (x = 0; x < 100; x++) {
        for (y = 0; y < 100; y++) {
            for (i = 0; i < N; i++) code[i] = initial[i];

            code[1] = x;
            code[2] = y;

            i = 0;
            while (1) {
                if (code[i] == 1) {
                    code[code[i+3]] = code[code[i+1]] + code[code[i+2]];
                    i += 4;
                } else if (code[i] == 2) {
                    code[code[i+3]] = code[code[i+1]] * code[code[i+2]];
                    i += 4;
                } else if (code[i] == 99) {
                    break;
                }
            }

            if (code[0] == 19690720) return to_string(100 * x + y);
        }
    }

    return "none";
}

int main(int argc, char** argv) {
    if (argc < 2) {
        cout << "Missing one argument" << endl;
        exit(1);
    }

    clock_t start = clock();
    auto answer = run(string(argv[1]));
    
    cout << "_duration:" << float( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC << "\n";
    cout << answer << "\n";
    return 0;
}
