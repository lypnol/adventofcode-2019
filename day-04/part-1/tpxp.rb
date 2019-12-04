def run(s)
    s = s[0].split '-'
    (s[0]..s[1]).inject(0) do |acc, digits|
        next acc if digits.length != 6
        success = false
        5.times do |i|
            success = true if digits[i] === digits[i+1]
            if digits[i] > digits[i+1]
                success = false
                break
            end
        end
        success ? acc+1 : acc
    end
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
