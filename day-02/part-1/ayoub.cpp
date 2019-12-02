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
    size_t code[N], i = -1;

    while (getline(ss, curr, ',')) {
        code[++i] = (size_t)stoi(curr);
    }

    code[1] = 12;
    code[2] = 2;

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

    return to_string(code[0]);
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
