def run(s)
    s = s[0].split '-'
    (s[0]..s[1]).inject(0) do |acc, digits|
        next acc if digits.length != 6
        found_2_eq = -20
        5.times do |i|
            if digits[i] == digits[i+1]
                n = digits[i].to_i
                if found_2_eq.abs == n
                    found_2_eq = -n
                    next
                end
                next if found_2_eq > 0
                found_2_eq = n
            end
            if digits[i] > digits[i+1]
                found_2_eq = -20
                break
            end
        end
        found_2_eq > 0 ? acc+1 : acc
    end
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
