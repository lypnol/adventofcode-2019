#include <iostream>
#include <string>
#include <algorithm>
#include <sstream>
#include <ctime>
#include <limits>

using namespace std;

typedef struct Point {
    int x, y;
} Point;

Point most_left(Point a, Point b, Point c, Point d) {
    Point r = a;
    r = (b.x < r.x)?b:r; r = (c.x < r.x)?c:r; r = (d.x < r.x)?d:r;
    return r;
}

Point most_right(Point a, Point b, Point c, Point d) {
    Point r = a;
    r = (b.x > r.x)?b:r; r = (c.x > r.x)?c:r; r = (d.x > r.x)?d:r;
    return r;
}

Point most_up(Point a, Point b, Point c, Point d) {
    Point r = a;
    r = (b.y > r.y)?b:r; r = (c.y > r.y)?c:r; r = (d.y > r.y)?d:r;
    return r;
}

Point most_down(Point a, Point b, Point c, Point d) {
    Point r = a;
    r = (b.y < r.y)?b:r; r = (c.y < r.y)?c:r; r = (d.y < r.y)?d:r;
    return r;
}

int abs(int x) {
    return (x > 0)?x:(-x);
}

Point intersection(Point a1, Point b1, Point a2, Point b2) {
    Point max{numeric_limits<int>::max(), numeric_limits<int>::max()};

    if (b1.y != a1.y && b2.y != a2.y) return max;
    if (b1.x != a1.x && b2.x != a2.x) return max;

    Point a = most_left(a1, b1, a2, b2);
    Point b = most_right(a1, b1, a2, b2);
    Point c = most_up(a1, b1, a2, b2);
    Point d = most_down(a1, b1, a2, b2);

    int max_width = (abs(b1.x - a1.x) > abs(b2.x - a2.x))?abs(b1.x - a1.x):abs(b2.x - a2.x);
    int max_height = (abs(b1.y - a1.y) > abs(b2.y - a2.y))?abs(b1.y - a1.y):abs(b2.y - a2.y);
    
    if (max_width < b.x-a.x) return max;
    if (max_height < c.y-d.y) return max;

    return Point{c.x, a.y};
}

string run(string s) {
    istringstream ss(s);
    string line;
    Point *wires[2];
    int i = 0, j = 0, length[2];

    while (getline(ss, line)) {
        istringstream path(line);
        string step;
        length[i] = count(line.begin(), line.end(), ',')+2;
        wires[i] = (Point*)malloc(sizeof(Point)*length[i]);
        wires[i][0] = {0, 0};
        j = 1;

        while (getline(path, step, ',')) {
            wires[i][j] = wires[i][j-1];
            if (step.at(0) == 'R') {
                wires[i][j].x += stoi(step.substr(1));
            } else if (step.at(0) == 'L') {
                wires[i][j].x -= stoi(step.substr(1));
            } else if (step.at(0) == 'U') {
                wires[i][j].y += stoi(step.substr(1));
            } else if (step.at(0) == 'D') {
                wires[i][j].y -= stoi(step.substr(1));
            }
            j++;
        }
        i++;
        if (i == 2) break;
    }

    int steps1 = 0, steps2 = 0, min_steps = numeric_limits<int>::max();
    for (i = 1; i < length[0]; i++) {
        steps2 = 0;
        for (j = 1; j < length[1]; j++) {
            Point intersect = intersection(
                wires[0][i-1], wires[0][i],
                wires[1][j-1], wires[1][j]);
            if (!(i == 1 && j == 1) && intersect.x != numeric_limits<int>::max() && intersect.y != numeric_limits<int>::max()) {
                int s1 = steps1 + abs(intersect.x - wires[0][i-1].x)+abs(intersect.y - wires[0][i-1].y);
                int s2 = steps2 + abs(intersect.x - wires[1][j-1].x)+abs(intersect.y - wires[1][j-1].y);
                min_steps = (min_steps>(s1+s2))?(s1+s2):min_steps;
            }
            steps2 += abs(wires[1][j].x - wires[1][j-1].x)+abs(wires[1][j].y - wires[1][j-1].y);
        }
        steps1 += abs(wires[0][i].x - wires[0][i-1].x)+abs(wires[0][i].y - wires[0][i-1].y);
    }

    return to_string(min_steps);
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
