def run(s)
    orbits_herited = Hash.new(0)
    s.each do |line|
        line = line.strip.split(')')
        orbits_herited[line[1]] = line[0]
    end
    total = 0
    orbits_herited.each do |key, value|
        l = 0
        while orbits_herited[key] != 0 do
            l += 1
            key = orbits_herited[key]
        end
        total += l
    end
    total
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
