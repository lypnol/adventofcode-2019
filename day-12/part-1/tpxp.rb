def run(s)
    pos = s.map do |line|
        res = /<x=(-?[0-9]+), y=(-?[0-9]+), z=(-?[0-9]+)>/.match line
        throw :badInput if res == nil
        res.captures.map &:to_i
    end
    v = pos.length.times.map { [0,0,0] }
    1000.times do
        # Gravity
        (0...pos.length).to_a.combination(2).each do |a,b|
            3.times do |i|
                v[a][i] += pos[a][i] > pos[b][i] ? -1 : +1 if pos[a][i] != pos[b][i]
                v[b][i] -= pos[a][i] > pos[b][i] ? -1 : +1 if pos[a][i] != pos[b][i] # The same but with a minus at the beginning
            end
        end
        # Positions
        pos.length.times do |i|
            3.times do |j|
                pos[i][j] += v[i][j]
            end
        end

    end
    pos.length.times.reduce (0) do |a,i|
        potential = pos[i].reduce (0) { |a, v| a + v.abs }
        kinetic = v[i].reduce (0) { |a, v| a + v.abs }
        a + potential * kinetic
    end
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
