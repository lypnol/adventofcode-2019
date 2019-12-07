using Test

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
        # pos1, pos2, dest = codes[i+1:i+3]
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
    for i in 1:99
        for j in 1:99
            input = parseInput(split(s, "\n")[1])
            input[2] = i
            input[3] = j
            output = part1(input)
            if output[1] == 19690720
                return 100 * i + j
            end
        end
    end
end

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time*1000)")
    println(res)
end

main()
