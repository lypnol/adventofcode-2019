def run(s)
  l = s[0].chars.map &:to_i
  pattern = [0,1,0,-1]
  100.times do
    # Number to compute
    l.length.times do |i|
      # Sum computation
      s = 0
      (i...l.length).each do |j|
        s += pattern[(j+1)/(i+1) % pattern.length] * l[j]
      end
      # Okay since the computation uses 0 factors for numbers before i
      l[i] = s.abs % 10
    end
  end
  l[0...8].join
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
