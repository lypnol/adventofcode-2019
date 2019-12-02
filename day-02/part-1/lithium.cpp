#include <iostream>
#include <string>
#include <sstream>
#include <ctime>

using namespace std;

void do_add(unsigned int in_1_idx, unsigned int in_2_idx, unsigned int out_idx, unsigned int array[]){
    array[out_idx] = array[in_1_idx] + array[in_2_idx];
}

void do_multiply(unsigned int in_1_idx, unsigned int in_2_idx, unsigned int out_idx, unsigned int array[]){
    array[out_idx] = array[in_1_idx] * array[in_2_idx];
}

string run(string s) {
    stringstream ss(s);
    string token;
    unsigned int array[200]; // good enough for the demo
    unsigned int last_idx = 0;
    while (getline(ss, token, ',')){
        array[last_idx++] = stoi(token);
    }
    // AoC quality bug fixing
    array[1] = 12;
    array[2] = 2;
    
    for (unsigned int i = 0; i < last_idx; i+=4){
        unsigned int opcode = array[i];
        switch(opcode){
            case 1:{
                do_add(array[i+1], array[i+2], array[i+3], array);
                continue;
            }
            case 2:{
                do_multiply(array[i+1], array[i+2], array[i+3], array);
                continue; // Otherwise we might execute this opcode again
            }
            case 99:{
                return to_string(array[0]);
            }
        }
    }
    return "Something went wrong";
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
