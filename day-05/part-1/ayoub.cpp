#include <iostream>
#include <algorithm>
#include <sstream>
#include <string>
#include <ctime>

using namespace std;

string run(string s) {
    istringstream ss(s);
    string curr;
    size_t N = count(s.begin(), s.end(), ',')+1;
    int code[N], i = -1;

    while (getline(ss, curr, ',')) {
        code[++i] = stoi(curr);
    }

    int last_output = 0;
    i = 0;
    while (1) {
        int op = code[i] % 100;
        int m1 = (code[i] / 100)%10, m2 = (code[i] / 1000)%10;
        if (op == 1) {
            int v1 = (m1)?code[i+1]:code[code[i+1]];
            int v2 = (m2)?code[i+2]:code[code[i+2]];
            code[code[i+3]] = v1 + v2;
            i += 4;
        } else if (op == 2) {
            int v1 = (m1)?code[i+1]:code[code[i+1]];
            int v2 = (m2)?code[i+2]:code[code[i+2]];
            code[code[i+3]] = v1 * v2;
            i += 4;
        } else if (op == 3) {
            code[code[i+1]] = 1;
            i += 2;
        } else if (op == 4) {
            last_output = (m1)?code[i+1]:code[code[i+1]];
            i += 2;
        } else if (op == 99) {
            break;
        }
    }

    return to_string(last_output);
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
