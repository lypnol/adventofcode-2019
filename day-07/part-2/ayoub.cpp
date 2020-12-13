#include <iostream>
#include <algorithm>
#include <sstream>
#include <string>
#include <ctime>

using namespace std;

void cpy(int* src, int* dest, int N) {
    for (int i = 0; i < N; i++) dest[i] = src[i];
}

int exec(int* code, int* inputs, int inputs_size, int *i) {
    int last_output = 0, outputs = 0;
    int k = -1;
    while (1) {
        int op = code[(*i)] % 100;
        int m1 = (code[(*i)] / 100)%10, m2 = (code[(*i)] / 1000)%10;
        if (op == 1) {
            int v1 = (m1)?code[(*i)+1]:code[code[(*i)+1]];
            int v2 = (m2)?code[(*i)+2]:code[code[(*i)+2]];
            code[code[(*i)+3]] = v1 + v2;
            (*i) += 4;
        } else if (op == 2) {
            int v1 = (m1)?code[(*i)+1]:code[code[(*i)+1]];
            int v2 = (m2)?code[(*i)+2]:code[code[(*i)+2]];
            code[code[(*i)+3]] = v1 * v2;
            (*i) += 4;
        } else if (op == 3) {
            if (k == inputs_size-1) return last_output;
            code[code[(*i)+1]] = inputs[++k];
            (*i) += 2;
        } else if (op == 4) {
            outputs++;
            if (outputs > 1) return last_output;
            last_output = (m1)?code[(*i)+1]:code[code[(*i)+1]];
            (*i) += 2;
        } else if (op == 5) {
            int v1 = (m1)?code[(*i)+1]:code[code[(*i)+1]];
            int v2 = (m2)?code[(*i)+2]:code[code[(*i)+2]];
            if (v1 != 0) {
                *i = v2;
            } else {
                (*i) += 3;
            }
        } else if (op == 6) {
            int v1 = (m1)?code[(*i)+1]:code[code[(*i)+1]];
            int v2 = (m2)?code[(*i)+2]:code[code[(*i)+2]];
            if (v1 == 0) {
                *i = v2;
            } else {
                (*i) += 3;
            }
        } else if (op == 7) {
            int v1 = (m1)?code[(*i)+1]:code[code[(*i)+1]];
            int v2 = (m2)?code[(*i)+2]:code[code[(*i)+2]];
            code[code[(*i)+3]] = (v1<v2)?1:0;
            (*i) += 4;
        } else if (op == 8) {
            int v1 = (m1)?code[(*i)+1]:code[code[(*i)+1]];
            int v2 = (m2)?code[(*i)+2]:code[code[(*i)+2]];
            code[code[(*i)+3]] = (v1==v2)?1:0;
            (*i) += 4;
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
    int code[N], i = -1, cp[5][N], idx[5] = {0};
    int phases[5] = {5, 6, 7, 8, 9}, inputs[2] = {0};

    while (getline(ss, curr, ',')) {
        code[++i] = stoi(curr);
    }

    int max = 0, output = 0;
    do {
        output = 0;
        for (int j = 0; j < 5; j++) {
            cpy(code, cp[j], N); idx[j] = 0;
        }
        int iter = 0;
        do {
            for (int j = 0; j < 5; j++) {
                if (iter==0) {
                    inputs[0] = phases[j];
                    inputs[1] = output;
                } else {
                    inputs[0] = output;
                }
                output = exec(cp[j], inputs, (iter==0)?2:1, idx+j);
            }
            iter++;
        } while(cp[4][idx[4]] != 99 );
        max = (max<output)?output:max;
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
