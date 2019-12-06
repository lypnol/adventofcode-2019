using Test

function check(n)
    d = reverse(digits(n))
    increasing = true
    double = false
    for i in 1:length(d)-1
        increasing = increasing && d[i] <= d[i+1]
        double = double || d[i] == d[i+1]
    end
    return increasing && double
end


function run(s)
    # println(s)
    n1, n2 = parse.(Int, (split(s, "-")))
    total = 0
    return sum(check.(n1:n2))
end

@test check(111111) == true
@test check(113456) == true
@test check(223450) == false
@test check(123789) == false


##############################

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time*1000)")
    println(res)
end

main()
