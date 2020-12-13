#include <iostream>
#include <algorithm>
#include <sstream>
#include <string>
#include <ctime>

using namespace std;

void cpy(int* src, int* dest, int N) {
    for (int i = 0; i < N; i++) dest[i] = src[i];
}

int exec(int* code, int* inputs) {
    int last_output = 0;
    int i = 0, k = -1;
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
            code[code[i+1]] = inputs[++k];
            i += 2;
        } else if (op == 4) {
            last_output = (m1)?code[i+1]:code[code[i+1]];
            i += 2;
        } else if (op == 5) {
            int v1 = (m1)?code[i+1]:code[code[i+1]];
            int v2 = (m2)?code[i+2]:code[code[i+2]];
            if (v1 != 0) {
                i = v2;
            } else {
                i += 3;
            }
        } else if (op == 6) {
            int v1 = (m1)?code[i+1]:code[code[i+1]];
            int v2 = (m2)?code[i+2]:code[code[i+2]];
            if (v1 == 0) {
                i = v2;
            } else {
                i += 3;
            }
        } else if (op == 7) {
            int v1 = (m1)?code[i+1]:code[code[i+1]];
            int v2 = (m2)?code[i+2]:code[code[i+2]];
            code[code[i+3]] = (v1<v2)?1:0;
            i += 4;
        } else if (op == 8) {
            int v1 = (m1)?code[i+1]:code[code[i+1]];
            int v2 = (m2)?code[i+2]:code[code[i+2]];
            code[code[i+3]] = (v1==v2)?1:0;
            i += 4;
        } else if (op == 99) {
            break;
        }
    }
    return last_output;
}

string run(string s) {
    istringstream ss(s);
    string curr;
    size_t N = count(s.begin(), s.end(), ',')+1;
    int code[N], i = -1, cp[N];
    int phases[5] = {0, 1, 2, 3, 4}, inputs[2] = {0};

    while (getline(ss, curr, ',')) {
        code[++i] = stoi(curr);
    }

    int max = 0, output = 0;
    do {
        for (int j = 0; j < 5; j++) {
            inputs[0] = phases[j];
            if (j == 0) inputs[1] = 0;
            else inputs[1] = output;
            cpy(code, cp, N);
            output = exec(cp, inputs);
            max = (max<output)?output:max;
        }
    } while(next_permutation(phases, phases+5));

    return to_string(max);
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
