def run(s)
    input = s[0].split(',').map &:to_i
    inputvals = [5]
    i = 0
    outputs = []
    loop do
        a0, a1, a2, a3 = input[i..i+3]
        code = a0 % 100
        v1 = a0 / 100 % 10 == 1 ? a1 : input[a1].to_i
        v2 = a0 / 1000 % 10 == 1 ? a2 : input[a2].to_i
        v3 = a0 / 10000 == 1 ? a3 : input[a3].to_i
        case code
            when 99
                break
            when 1
                input[a3] = v1 + v2
                i += 4
            when 2
                input[a3] = v1 * v2
                i += 4
            when 3
                input[a1] = inputvals.shift
                i += 2
            when 4
                return v1 unless v1 == 0
                i += 2
            when 5
                i = v1 != 0 ? v2 : i + 3
            when 6
                i = v1 == 0 ? v2 : i + 3
            when 7
                input[a3] = v1 < v2 ? 1 : 0
                i += 4
            when 8
                input[a3] = v1 == v2 ? 1 : 0
                i += 4
            else
                throw :unknownCode
        end
    end
    input[0]
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
