def run(s)
    global_pos = s.map do |line|
        res = /<x=(-?[0-9]+), y=(-?[0-9]+), z=(-?[0-9]+)>/.match line
        throw :badInput if res == nil
        res.captures.map &:to_i
    end
    history = Hash.new
    # Idea: simulate each axis independently
    # You can compare lists directly
    zeros = [0] * global_pos.length
    3.times.reduce(1) do |val, j|
        start_pos = global_pos.length.times.map { |i| global_pos[i][j] }
        pos = start_pos.clone
        v = [0] * start_pos.length

        n_repeat = 0
        catch :repeated do
            9999999.times do |iter|
                if pos == start_pos and v == zeros and iter > 0
                    n_repeat = iter
                    throw :repeated
                end
                # Gravity
                (0...pos.length).to_a.combination(2).each do |a,b|
                    v[a] += pos[a] > pos[b] ? -1 : +1 if pos[a] != pos[b]
                    v[b] -= pos[a] > pos[b] ? -1 : +1 if pos[a] != pos[b] # The same but with a minus at the beginning
                end
                # Positions
                pos.length.times do |i|
                    pos[i] += v[i]
                end
            end
            throw :didNotRepeat
        end
        # Here is the main trick: we know a cycle duration for 1 dimension, let's find the cycle duration for this
        # dimension with the other cycles we found until know
        val.lcm(n_repeat)
    end
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
