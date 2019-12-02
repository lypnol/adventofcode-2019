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

unsigned int do_compute_intcode(unsigned int last_idx, unsigned int array[]){
    for (unsigned int i = 0; i < last_idx; i+=4){
        switch(array[i]){
            case 1:{
                do_add(array[i+1], array[i+2], array[i+3], array);
                continue;
            }
            case 2:{
                do_multiply(array[i+1], array[i+2], array[i+3], array);
                continue; // Otherwise we might execute this opcode again
            }
            case 99:{
                return array[0];
            }
        }
    }
    return 0; // This means an error in the intcode program tho
}

string run(string s) {
    stringstream ss(s);
    string token;
    unsigned int base_array[200];
    unsigned int array[200]; // good enough for the demo
    unsigned int last_idx = 0;
    while (getline(ss, token, ',')){
        base_array[last_idx] = stoi(token);
        array[last_idx++] = stoi(token);
    }

    unsigned int noun = 0;
    unsigned int verb = 0;

    while (do_compute_intcode(last_idx, array) != 19690720){
        copy(begin(base_array), end(base_array), begin(array)); // reset array to base values
        noun ++;
        if (noun == 100){
            noun = 0;
            verb ++;
        }
        if (verb == 100){
            return "something went wrong";
        }
        array[1] = noun;
        array[2] = verb;
    }
    return to_string((100 * noun) + verb);
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
