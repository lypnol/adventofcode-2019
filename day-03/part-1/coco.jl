using Test
using Dates


##################################
## Bruteforce version
##################################

function constructSet(line)
    path = []
    x = 0
    y = 0
    instructions = split(line, ",")
    for inst in instructions
        dir = inst[1]
        number = parse(Int, inst[2:end])
        
        if dir == 'R'
            positions = map(i -> (x, y + i), 1:number)
        elseif dir == 'L'
            positions = map(i -> (x, y - i), 1:number)
        elseif dir == 'U'
            positions = map(i -> (x + i , y), 1:number)
        elseif dir == 'D'
            positions = map(i -> (x - i , y), 1:number)
        end
        x = positions[end][1]
        y = positions[end][2]
        append!(path, positions)
    end
    return path
end

function run(input)
    input = split(input, "\n")
    set1 = constructSet(input[1])
    set2 = constructSet(input[2])
    inter = intersect(Set(set1), Set(set2))
    return  minimum(pos -> abs(pos[1]) + abs(pos[2]), inter)
end

##############################################################
### Another faster version
##############################################################

function getVertices(line)
    vertices = []
    (x, y) = (0, 0)
    instructions = split(line, ",")
    for inst in instructions
        dir = inst[1]
        steps = parse(Int, inst[2:end])
        if dir == 'R'
            append!(vertices, [((x, y), (x, y+steps))])
            y = y + steps
        elseif dir == 'L'
            append!(vertices,[((x, y-steps), (x, y))])
            y = y - steps
        elseif dir == 'U'
            append!(vertices, [((x, y), (x + steps, y))])
            x = x + steps
        elseif dir == 'D'
            append!(vertices, [((x - steps, y), (x, y))])
            x = x - steps
        end
    end
    return vertices
end

function getDir(ver)
    (x1, y1), (x2, y2) = ver
    if x1 == x2 
        return "LR"
    elseif y1 == y2
        return "UD"
    end
end

@test getDir(((1, 2), (1, 3))) == "LR"
@test getDir(((1, 2), (3, 2))) == "UD"

function getIntersectionVertices(ver1, ver2)
    ((x1, y1), (x2, y2)) = ver1
    ((x3, y3), (x4, y4)) = ver2
    dir1 = getDir(ver1)
    dir2 = getDir(ver2)
    if dir1 == dir2 == "LR"
        if x1 == x3
            return [(x1, y) for y in max(y1, y3):min(y2, y4)]
        else
            return []
        end
    elseif dir1 == dir2 == "UD"
        if y1 == y3
            return [(x, y1) for x in max(x1, x3):min(x2, x4)]
        else
            return []
        end
    elseif dir1 == "UD" && dir2 == "LR"
        if x1 <= x3 <= x2 && y3 <= y1 <= y4
            return [(x3, y1)]
        else
            return []
        end
    elseif dir1 == "LR" && dir2 == "UD"
        # invert the two
        ((x1, y1), (x2, y2)) = ver2
        ((x3, y3), (x4, y4)) = ver1
        if x1 <= x3 <= x2 && y3 <= y1 <= y4
            return [(x3, y1)]
        else
            return []
        end
    end
end

@test getIntersectionVertices(
    ((1, 2), (1, 3)),
    ((1, 2), (1, 4))
) == [(1, 2), (1, 3)]

@test getIntersectionVertices(
    ((1, 2), (1, 7)),
    ((1, 4), (1, 20))
) == [(1, 4), (1, 5), (1, 6),  (1, 7)]

@test getIntersectionVertices(
    ((2, 1), (7, 1)),
    ((4, 1), (20, 1))
) == [(4, 1), (5, 1), (6, 1),  (7, 1)]

@test getIntersectionVertices(
    ((2, 5), (2, 10)),
    ((1, 6), (5, 6))
) == [(2, 6)]

@test getIntersectionVertices(
    ((1, 6), (5, 6)),
    ((2, 5), (2, 10))
) == [(2, 6)]

function getIntersections(vertices1, vertices2)
    intersections = []
    for ver1 in vertices1
        for ver2 in vertices2
            inter = getIntersectionVertices(ver1, ver2)
            append!(intersections, inter)
        end
    end
    return intersections
end
           
function run2(input)
    input = split(input, "\n")
    vertices1 = getVertices(input[1])
    vertices2 = getVertices(input[2])
    inter = getIntersections(vertices1, vertices2)
    inter = filter(x -> x ≠ (0, 0), inter)
    return minimum(pos -> abs(pos[1]) + abs(pos[2]), inter)
end

@test run2("R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83") == 159
@test run2("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7") == 135

#########################################

function main()
    input = ARGS[1]
    # input = split(input, "\n")
    res, time, memory = @timed run2(input)
    println("_duration:$(time*1000)")
    println(res)
end

main()
