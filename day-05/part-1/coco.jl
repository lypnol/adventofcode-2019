using Test

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

function part1(codes)
    i = 1
    outputs = []
    while codes[i] != 99
        operation = codes[i]
        numbers = digits(operation, pad=5)
        instruction = numbers[1] + 10*numbers[2]
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
            codes[dest] = 1
            i += 2
        elseif instruction == 4
            dest = codes[i+1] + 1
            append!(outputs, codes[dest])
            i += 2
        end
    end
    return codes, outputs
end

function run(s)
    input = parseInput(split(s, "\n")[1])
    # input[2] = 12
    # input[3] = 2
    return part1(input)[2][end]
end

@test part1(parseInput("1002,4,3,4,33"))[1] == [1002, 4, 3, 4, 99]

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time*1000)")
    println(res)
end

main()
