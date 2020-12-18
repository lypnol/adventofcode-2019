#include <iostream>
#include <ctime>

#define WIDTH 25
#define L_WIDTH 5
#define HEIGHT 6
#define SPACE 150

using namespace std;

bool is_letter_A(char* res, int k) {
    const char A[HEIGHT][L_WIDTH] = {
        {'0', '1', '1', '0', '0'},
        {'1', '0', '0', '1', '0'},
        {'1', '0', '0', '1', '0'},
        {'1', '1', '1', '1', '0'},
        {'1', '0', '0', '1', '0'},
        {'1', '0', '0', '1', '0'}};
    for (int i = 0; i < HEIGHT; i++)
    for (int j = 0; j < L_WIDTH; j++)
        if (res[WIDTH*i+k*L_WIDTH+j] != A[i][j]) return false;
    return true;
}

bool is_letter_B(char* res, int k) {
    const char B[HEIGHT][L_WIDTH] = {
        {'1', '1', '1', '0', '0'},
        {'1', '0', '0', '1', '0'},
        {'1', '1', '1', '0', '0'},
        {'1', '0', '0', '1', '0'},
        {'1', '0', '0', '1', '0'},
        {'1', '1', '1', '0', '0'}};
    for (int i = 0; i < HEIGHT; i++)
    for (int j = 0; j < L_WIDTH; j++)
        if (res[WIDTH*i+k*L_WIDTH+j] != B[i][j]) return false;
    return true;
}

bool is_letter_C(char* res, int k) {
    const char C[HEIGHT][L_WIDTH] = {
        {'0', '1', '1', '0', '0'},
        {'1', '0', '0', '1', '0'},
        {'1', '0', '0', '0', '0'},
        {'1', '0', '0', '0', '0'},
        {'1', '0', '0', '1', '0'},
        {'0', '1', '1', '0', '0'}};
    for (int i = 0; i < HEIGHT; i++)
    for (int j = 0; j < L_WIDTH; j++)
        if (res[WIDTH*i+k*L_WIDTH+j] != C[i][j]) return false;
    return true;
}

bool is_letter_E(char* res, int k) {
    const char E[HEIGHT][L_WIDTH] = {
        {'1', '1', '1', '1', '0'},
        {'1', '0', '0', '0', '0'},
        {'1', '1', '1', '0', '0'},
        {'1', '0', '0', '0', '0'},
        {'1', '0', '0', '0', '0'},
        {'1', '1', '1', '1', '0'}};
    for (int i = 0; i < HEIGHT; i++)
    for (int j = 0; j < L_WIDTH; j++)
        if (res[WIDTH*i+k*L_WIDTH+j] != E[i][j]) return false;
    return true;
}

bool is_letter_F(char* res, int k) {
    const char F[HEIGHT][L_WIDTH] = {
        {'1', '1', '1', '1', '0'},
        {'1', '0', '0', '0', '0'},
        {'1', '1', '1', '0', '0'},
        {'1', '0', '0', '0', '0'},
        {'1', '0', '0', '0', '0'},
        {'1', '0', '0', '0', '0'}};
    for (int i = 0; i < HEIGHT; i++)
    for (int j = 0; j < L_WIDTH; j++)
        if (res[WIDTH*i+k*L_WIDTH+j] != F[i][j]) return false;
    return true;
}

bool is_letter_G(char* res, int k) {
    const char G[HEIGHT][L_WIDTH] = {
        {'0', '1', '1', '0', '0'},
        {'1', '0', '0', '1', '0'},
        {'1', '0', '0', '0', '0'},
        {'1', '0', '1', '1', '0'},
        {'1', '0', '0', '1', '0'},
        {'0', '1', '1', '1', '0'}};
    for (int i = 0; i < HEIGHT; i++)
    for (int j = 0; j < L_WIDTH; j++)
        if (res[WIDTH*i+k*L_WIDTH+j] != G[i][j]) return false;
    return true;
}

bool is_letter_H(char* res, int k) {
    const char H[HEIGHT][L_WIDTH] = {
        {'1', '0', '0', '1', '0'},
        {'1', '0', '0', '1', '0'},
        {'1', '1', '1', '1', '0'},
        {'1', '0', '0', '1', '0'},
        {'1', '0', '0', '1', '0'},
        {'1', '0', '0', '1', '0'}};
    for (int i = 0; i < HEIGHT; i++)
    for (int j = 0; j < L_WIDTH; j++)
        if (res[WIDTH*i+k*L_WIDTH+j] != H[i][j]) return false;
    return true;
}

bool is_letter_J(char* res, int k) {
    const char J[HEIGHT][L_WIDTH] = {
        {'0', '0', '1', '1', '0'},
        {'0', '0', '0', '1', '0'},
        {'0', '0', '0', '1', '0'},
        {'0', '0', '0', '1', '0'},
        {'1', '0', '0', '1', '0'},
        {'0', '1', '1', '0', '0'}};
    for (int i = 0; i < HEIGHT; i++)
    for (int j = 0; j < L_WIDTH; j++)
        if (res[WIDTH*i+k*L_WIDTH+j] != J[i][j]) return false;
    return true;
}

bool is_letter_K(char* res, int k) {
    const char K[HEIGHT][L_WIDTH] = {
        {'1', '0', '0', '1', '0'},
        {'1', '0', '1', '0', '0'},
        {'1', '1', '0', '0', '0'},
        {'1', '0', '1', '0', '0'},
        {'1', '0', '1', '0', '0'},
        {'1', '0', '0', '1', '0'}};
    for (int i = 0; i < HEIGHT; i++)
    for (int j = 0; j < L_WIDTH; j++)
        if (res[WIDTH*i+k*L_WIDTH+j] != K[i][j]) return false;
    return true;
}

bool is_letter_L(char* res, int k) {
    const char L[HEIGHT][L_WIDTH] = {
        {'1', '0', '0', '0', '0'},
        {'1', '0', '0', '0', '0'},
        {'1', '0', '0', '0', '0'},
        {'1', '0', '0', '0', '0'},
        {'1', '0', '0', '0', '0'},
        {'1', '1', '1', '1', '0'}};
    for (int i = 0; i < HEIGHT; i++)
    for (int j = 0; j < L_WIDTH; j++)
        if (res[WIDTH*i+k*L_WIDTH+j] != L[i][j]) return false;
    return true;
}

bool is_letter_P(char* res, int k) {
    const char P[HEIGHT][L_WIDTH] = {
        {'1', '1', '1', '0', '0'},
        {'1', '0', '0', '1', '0'},
        {'1', '0', '0', '1', '0'},
        {'1', '1', '1', '0', '0'},
        {'1', '0', '0', '0', '0'},
        {'1', '0', '0', '0', '0'}};
    for (int i = 0; i < HEIGHT; i++)
    for (int j = 0; j < L_WIDTH; j++)
        if (res[WIDTH*i+k*L_WIDTH+j] != P[i][j]) return false;
    return true;
}

bool is_letter_R(char* res, int k) {
    const char R[HEIGHT][L_WIDTH] = {
        {'1', '1', '1', '0', '0'},
        {'1', '0', '0', '1', '0'},
        {'1', '0', '0', '1', '0'},
        {'1', '1', '1', '0', '0'},
        {'1', '0', '1', '0', '0'},
        {'1', '0', '0', '1', '0'}};
    for (int i = 0; i < HEIGHT; i++)
    for (int j = 0; j < L_WIDTH; j++)
        if (res[WIDTH*i+k*L_WIDTH+j] != R[i][j]) return false;
    return true;
}

bool is_letter_U(char* res, int k) {
    const char U[HEIGHT][L_WIDTH] = {
        {'1', '0', '0', '1', '0'},
        {'1', '0', '0', '1', '0'},
        {'1', '0', '0', '1', '0'},
        {'1', '0', '0', '1', '0'},
        {'1', '0', '0', '1', '0'},
        {'0', '1', '1', '0', '0'}};
    for (int i = 0; i < HEIGHT; i++)
    for (int j = 0; j < L_WIDTH; j++)
        if (res[WIDTH*i+k*L_WIDTH+j] != U[i][j]) return false;
    return true;
}

bool is_letter_Y(char* res, int k) {
    const char Y[HEIGHT][L_WIDTH] = {
        {'1', '0', '0', '0', '1'},
        {'1', '0', '0', '0', '1'},
        {'0', '1', '0', '1', '0'},
        {'0', '0', '1', '0', '0'},
        {'0', '0', '1', '0', '0'},
        {'0', '0', '1', '0', '0'}};
    for (int i = 0; i < HEIGHT; i++)
    for (int j = 0; j < L_WIDTH; j++)
        if (res[WIDTH*i+k*L_WIDTH+j] != Y[i][j]) return false;
    return true;
}

bool is_letter_Z(char* res, int k) {
    const char Z[HEIGHT][L_WIDTH] = {
        {'1', '1', '1', '1', '0'},
        {'0', '0', '0', '1', '0'},
        {'0', '0', '1', '0', '0'},
        {'0', '1', '0', '0', '0'},
        {'1', '0', '0', '0', '0'},
        {'1', '1', '1', '1', '0'}};
    for (int i = 0; i < HEIGHT; i++)
    for (int j = 0; j < L_WIDTH; j++)
        if (res[WIDTH*i+k*L_WIDTH+j] != Z[i][j]) return false;
    return true;
}


char get_letter(char* res, int k) {
    if (is_letter_A(res, k)) return 'A';
    else if (is_letter_B(res, k)) return 'B';
    else if (is_letter_C(res, k)) return 'C';
    else if (is_letter_E(res, k)) return 'E';
    else if (is_letter_F(res, k)) return 'F';
    else if (is_letter_G(res, k)) return 'G';
    else if (is_letter_H(res, k)) return 'H';
    else if (is_letter_J(res, k)) return 'J';
    else if (is_letter_K(res, k)) return 'K';
    else if (is_letter_L(res, k)) return 'L';
    else if (is_letter_P(res, k)) return 'P';
    else if (is_letter_R(res, k)) return 'R';
    else if (is_letter_U(res, k)) return 'U';
    else if (is_letter_Y(res, k)) return 'Y';
    else if (is_letter_Z(res, k)) return 'Z';
    return '?';
}

string run(char* s) {
    int i = -1, j = 0;
    char res[SPACE+1] = {0};
    while (s[j]) {
        i = j;
        j += SPACE;
        for (int k = i; k < j; k++) {            
            int pos = k%SPACE;
            if ((s[k] == '0' || s[k] == '1') && res[pos] == 0) {
                res[pos] = s[k];
            }
        }
    }
    char r[1+WIDTH/L_WIDTH] = {0};
    for (i = 0; i < WIDTH/L_WIDTH; i++) r[i] = get_letter(res, i); 
    return string(r);
}

int main(int argc, char** argv) {
    if (argc < 2) {
        cout << "Missing one argument" << endl;
        exit(1);
    }

    clock_t start = clock();
    string answer = run(argv[1]);
    
    cout << "_duration:" << float( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC << "\n";
    cout << answer << "\n";
    return 0;
}
