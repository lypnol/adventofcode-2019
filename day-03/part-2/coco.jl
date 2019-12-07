using Test
# using ProgressMeter

function constructSet(line)
    path = []
    pathWithSteps = []
    position = (0, 0)
    paths = (0, 0, 0)
    instructions = split(line, ",")
    totalSteps = 1
    for inst in instructions
        # println(inst)
        dir = inst[1]
        number = parse(Int, inst[2:end])
        for i in 1:number
            if dir == 'R'
                position = position[1], position[2] + 1
            elseif dir == 'L'
                position = position[1], position[2] - 1
            elseif dir == 'U'
                position = position[1] + 1, position[2]
            elseif dir == 'D'
                position = position[1] - 1, position[2] 
            end
            append!(path, [position])
            append!(pathWithSteps, [(position[1], position[2], totalSteps)])
            totalSteps += 1
        end
    end
    return path, pathWithSteps
end


function getClosestIntersection(set1, set2)
    inter = intersect(set1, set2)
    best = minimum(pos -> abs(pos[1]) + abs(pos[2]), inter)
    return best
end

function part1(input)
    set1, _ = constructSet(input[1])
    set2, _ = constructSet(input[2])
    return getClosestIntersection(set1, set2)
end


function part2(input)
    path1, path1withSteps = constructSet(input[1])
    path2, path2withSteps = constructSet(input[2])
    inter = intersect(path1, path2)
    
    distances1 = Dict()
    # println(path1withSteps)
    for (x, y, steps) in path1withSteps
        if !haskey(distances1, (x, y))
            distances1[(x, y)] = steps
        end
    end

    distances2 = Dict()
    for (x, y, steps) in path2withSteps
        # println(x, y, steps)
        if !haskey(distances2, (x, y))
            distances2[(x, y)] = steps
        end
    end
    
    return minimum(pos -> distances1[pos] + distances2[pos], inter)
end

@test part2(["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"]) == 610
@test part2(["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"]) == 410


# println("part1")
# println(part1(lines))
# println("part2")
# println(part2(lines))


function run(s)
    return part2(split(s, "\n"))
end

#########################################

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time*1000)")
    println(res)
end

main()
