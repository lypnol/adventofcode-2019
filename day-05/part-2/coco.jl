using Test
using Logging


function parseInput(input)
    chars = split(input, ",")
    chars = parse.(Int, chars)
    return chars
end

function getVal(val, codes, mode)
    if mode == 0
        return codes[val + 1]
    elseif mode == 1
        return val
    end
end

function part1(codes, input=1)
    i = 1
    outputs = []
    @debug "codes $(codes)"
    while codes[i] != 99
        operation = codes[i]
        numbers = digits(operation, pad=5)
        instruction = numbers[1] + 10*numbers[2]
        @debug "position=$(i)"
        @debug "instruction: $(instruction)"
        mode1 = numbers[3]
        mode2 = numbers[4]
        mode3 = numbers[5]
        if instruction == 1
            val1, val2, dest = codes[i+1:i+3]
            codes[dest+1] = getVal(val1, codes, mode1) + getVal(val2, codes, mode2) #codes[val2]
            i += 4
        elseif instruction == 2
            val1, val2, dest = codes[i+1:i+3]
            codes[dest+1] = getVal(val1, codes, mode1) * getVal(val2, codes, mode2) #codes[val2]
            i += 4
        elseif instruction == 3
            dest = codes[i+1] + 1
            codes[dest] = input
            i += 2
        elseif instruction == 4
            val = getVal(codes[i+1], codes, mode1)
            append!(outputs, val)
            i += 2
        elseif instruction == 5
            val1 = getVal(codes[i+1], codes, mode1)
            dest = getVal(codes[i+2], codes, mode2)
            # println(dest)
            if val1 != 0
                i = dest + 1
            else
                i += 3
            end
        elseif instruction == 6
            val1 = getVal(codes[i+1], codes, mode1)
            dest = getVal(codes[i+2], codes, mode2)
            if dest == i
                println("error: infinite loop")
                exit()
            end
            @debug "val1 , $(val1)"
            @debug "dest $(dest)"
            if val1 == 0
                i = dest + 1
            else
                i += 3
            end
        elseif instruction == 7
            val1 = getVal(codes[i+1], codes, mode1)
            val2 = getVal(codes[i+2], codes, mode2)
            dest = codes[i+3] +1 
            if val1 < val2
                codes[dest] = 1
            else
                codes[dest] = 0
            end
            i += 4
        elseif instruction == 8
            val1 = getVal(codes[i+1], codes, mode1)
            val2 = getVal(codes[i+2], codes, mode2)
            dest = codes[i+3] +1 
            if val1 == val2
                codes[dest] = 1
            else
                codes[dest] = 0
            end    
            i += 4
        else
            throw(Exception())
        end
        @debug "code : $(codes)"
        @debug "outputs $(outputs)"
    end
    return outputs[end], codes, outputs
end


@test part1(parseInput("3,9,8,9,10,9,4,9,99,-1,8"), 8)[1] == 1
@test part1(parseInput("3,9,8,9,10,9,4,9,99,-1,8"), 7)[1] == 0

@test part1(parseInput("3,9,7,9,10,9,4,9,99,-1,8"), 9)[1] == 0
@test part1(parseInput("3,9,7,9,10,9,4,9,99,-1,8"), 8)[1] == 0
@test part1(parseInput("3,9,7,9,10,9,4,9,99,-1,8"), 7)[1] == 1

# # test jumping

@test part1(parseInput("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9"), 10)[1] == 1
@test part1(parseInput("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9"), 0)[1] == 0


@test part1(parseInput("3,3,1105,-1,9,1101,0,0,12,4,12,99,1"), 0)[1] == 0
@test part1(parseInput("3,3,1105,-1,9,1101,0,0,12,4,12,99,1"), 10)[1] == 1

@test part1(parseInput("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"), 7)[1] == 999

@test part1(parseInput("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"), 8)[1] == 1000

@test part1(parseInput("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"), 9)[1] == 1001


function run(s)
    input = parseInput(split(s, "\n")[1])
    return part1(input, 5)[1]
end

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time*1000)")
    println(res)
end

main()
