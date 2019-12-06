def run(s)
    orbits_herited = Hash.new(0)
    s.each do |line|
        line = line.strip.split(')')
        orbits_herited[line[1]] = line[0]
    end
    key = orbits_herited['SAN']
    l = 0
    while orbits_herited[key] != 0
        next_key = orbits_herited[key]
        orbits_herited[key] = l
        l += 1
        key = next_key
    end
    key = orbits_herited['YOU']
    l = 0
    until orbits_herited[key].is_a? Integer
        l += 1
        key = orbits_herited[key]
    end
    l + orbits_herited[key]
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
