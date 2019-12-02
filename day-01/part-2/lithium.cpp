#include <iostream>
#include <string>
#include <sstream>
#include <ctime>

using namespace std;

string run(string s) {

    unsigned int counter = 0;
    stringstream ss(s);
    string token;
    int fuel = 0;
    while(getline(ss, token, '\n')) {
        fuel = (stoi(token) / 3) - 2;
        while (fuel > 0){
            counter += fuel;
            fuel = (fuel / 3) - 2;
        }
    }
    return to_string(counter);
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
