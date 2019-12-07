function parseInput(input)
    chars = split(input, ",")
    chars = parse.(Int, chars)
    return chars
end

function part1(codes)
    i = 1
    while codes[i] != 99
        operation = codes[i]
        pos1 = codes[i+1] + 1
        pos2 = codes[i+2] + 1
        dest = codes[i+3] + 1
        if operation == 1
            codes[dest] = codes[pos1] + codes[pos2]
        elseif operation == 2
            codes[dest] = codes[pos1] * codes[pos2]
        end
        i += 4
    end
    return codes
end


function run(s)
    input = parseInput(split(s, "\n")[1])
    input[2] = 12
    input[3] = 2
    return part1(input)[1]
end

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time*1000)")
    println(res)
end

main()
