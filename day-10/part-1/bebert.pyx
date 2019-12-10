import cython

DEF GRID_W = 40
DEF GRID_H = 40
DEF GRID_LEN = 1600

@cython.cdivision(True)
cdef int gcd(int a, int b):
    cdef int r
    while b != 0:
        r = a % b
        a, b = b, r
    return a

@cython.cdivision(True)
cdef void step(char* g, int x, int y, int dx, int dy):
    if g[(y + dy) * GRID_W + (x + dx)] == 0:
        return

    cdef int gcd_dx_dy = gcd(dx if dx > 0 else -dx, dy if dy > 0 else -dy)
    cdef int reduced_dx = dx // gcd_dx_dy
    cdef int reduced_dy = dy // gcd_dx_dy
    g[(y + dy) * GRID_W + (x + dx)] = 0
    g[(y + reduced_dy) * GRID_W + (x + reduced_dx)] = 1

# cdef void print_grid(char* g):
#     cdef str pg = ''
#     cdef int i
#     for i in range(GRID_LEN):
#         if i % GRID_W == 0:
#             pg += "\n"
#         pg += ".#x-"[g[i]]
#     print(pg)

cpdef int run(s):
    cdef int i, x, y, count
    cdef str a

    cdef char[1600] grid
    cdef char[1600] cur_grid
    for i in range(GRID_LEN):
        grid[i] = 0

    for y, line in enumerate(s.splitlines()):
        for x, a in enumerate(line):
            if a == "#":
                grid[y * GRID_W + x] = 1

    cdef int max_ast = 0
    cdef int max_x = 0
    cdef int max_y = 0

    # print_grid(grid)

    for y in range(GRID_H):
        for x in range(GRID_W):
            if grid[y * GRID_W + x] == 0:
                continue

            # reset
            for i in range(GRID_LEN):
                cur_grid[i] = grid[i]

            cur_grid[y * GRID_W + x] = 0

            # Zone 1
            dy = 0
            for dx in range(1, GRID_W - x):
                step(cur_grid, x, y, dx, dy)

            for dy in range(1, GRID_H - y):
                for dx in range(0, GRID_W - x):
                    step(cur_grid, x, y, dx, dy)

            # Zone 2
            for dy in range(0, GRID_H - y):
                for dx in range(-1, -x-1, -1):
                    step(cur_grid, x, y, dx, dy)

            # Zone 3
            for dy in range(-1, -y-1, -1):
                for dx in range(0, GRID_W - x):
                    step(cur_grid, x, y, dx, dy)

            # Zone 4
            for dy in range(-1, -y-1, -1):
                for dx in range(-1, -x-1, -1):
                    step(cur_grid, x, y, dx, dy)

            count = 0
            for i in range(GRID_LEN):
                if cur_grid[i] == 1:
                    count += 1

            if count > max_ast:
                max_ast = count
                max_x = x
                max_y = y

            # if x == 5 and y == 3:
            #     cur_grid[3 * GRID_W + 5] = 2
            #     print_grid(cur_grid)
            #     print(f"count: {count}")
            #     print(f"max_ast: {max_ast}")

    # print(f"Max (x, y): ({max_x}, {max_y}) -> {max_ast}")
    return max_ast
