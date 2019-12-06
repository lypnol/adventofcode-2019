using Test

function check(n)
    d = reverse(digits(n))
    double = false

    for i in 1:length(d)-1
        if d[i] > d[i+1]
            return false
        end
        if  d[i] == d[i+1]  # we have a double
            if i == 1
                if d[i+1] ≠ d[i+2]
                    double = true
                end
            elseif i == length(d) - 1
                if d[i-1] ≠ d[i]
                    double = true
                end
            else
                if d[i-1] ≠ d[i] && d[i+1] ≠ d[i+2]
                    double = true
                end
            end
        end
    end
    return double
end


function run(s)
    # println(s)
    n1, n2 = parse.(Int, (split(s, "-")))
    total = 0
    return sum(check.(n1:n2))
end

@test check(112233) == true
@test check(223334) == true
@test check(123444) == false
@test check(111122) == true


##############################

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time*1000)")
    println(res)
end

main()
