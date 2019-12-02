def run(s)
    input = s[0].split(',').map &:to_i
    input[1] = 12
    input[2] = 2
    i = 0
    loop do
        code, a, b, target = input[i..i+3]
        a = input[a]
        b = input[b]
        case code
            when 99
                break
            when 1
                input[target] = a + b
            when 2
                input[target] = a * b
        end
        i += 4
    end
    input[0]
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
