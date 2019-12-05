function run(s)
    total = 0
    for line in split(s, "\n")
        mass = parse(Int, line)
        fuel = mass ÷ 3 - 2
        total += fuel
    end
    return total
end

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time*1000)")
    println(res)
end

main()
