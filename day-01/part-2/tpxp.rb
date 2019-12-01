def run(s)
  s.map(&:to_i).reduce(0) do |sum, n|
    loop do
      n = n / 3 - 2
      break if n <= 0
      sum += n
    end
    sum
  end
=begin
  # You can also do it explictely, both methods have similar performance
  sum = 0
  s.each do |line|
    weight = Integer(line)
    loop do
      weight = weight / 3 - 2
      break if weight <= 0
      sum += weight
    end
  end
  sum
=end
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
