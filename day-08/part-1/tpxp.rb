def run(s)
  s = s[0]
  m = Float::INFINITY
  layer = nil
  (s.length / (25*6)).times do |i|
    l = s[i * 25 * 6...(i+1)*25*6]
    c = l.count "0"
    if c < m
      m = c
      layer = l
    end
  end
  (layer.count "1") * (layer.count "2")
end

starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000
puts "_duration:#{elapsed}\n#{answer}" 
