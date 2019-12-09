def run_prgm(prgm, inputvals)
    input = prgm.clone
    i = 0
    relative_base = 0
    loop do
        a = input[i..i+3]
        code = a[0] % 100
        modes = 3.times.to_a.map { |i| (a[0] / (10 ** (i+2))) % 10}

        v = 3.times.to_a.map { |i|
            r = a[i+1]
            r = input[r] if modes[i] == 0
            r = input[relative_base + r] if modes[i] == 2
            r.to_i
        }

        case code
        when 99
            throw :haltAndCatchFire
        when 1
            input[modes[2] == 0 ? a[3] : relative_base + a[3]] = v[0] + v[1]
            i += 4
        when 2
            input[modes[2] == 0 ? a[3] : relative_base + a[3]] = v[0] * v[1]
            i += 4
        when 3
            throw :noInput if inputvals.length == 0
            input[modes[0] == 0 ? a[1] : relative_base + a[1]] = inputvals.shift
            i += 2
        when 4
            return v[0]
            # i += 2
        when 5
            i = v[0] != 0 ? v[1] : i + 3
        when 6
            i = v[0] == 0 ? v[1] : i + 3
        when 7
            input[modes[2] == 0 ? a[3] : relative_base + a[3]] = v[0] < v[1] ? 1 : 0
            i += 4
        when 8
            input[modes[2] == 0 ? a[3] : relative_base + a[3]] = v[0] == v[1] ? 1 : 0
            i += 4
        when 9
            relative_base += v[0]
            i += 2
        else
            throw :unknownCode
        end
    end
end

def run(s)
    prgm = s[0].split(',').map &:to_i
    run_prgm(prgm, [1])
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"