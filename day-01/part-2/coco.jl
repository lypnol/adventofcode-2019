function run(s)
    total = 0
    for line in split(s, "\n")
        mass = parse(Int, line)
        fuelneeded = 0
        while fuelneeded >= 0
            total += fuelneeded
            fuelneeded = mass ÷ 3 - 2
            mass = fuelneeded
        end 
    end
    return total
end

function main()
    res, time, memory = @timed run(ARGS[1])
    # println(time)
    println("_duration:$(time*1000)")
    println(res)
end

main()
