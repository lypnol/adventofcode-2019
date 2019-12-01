def run(s)
  s.map(&:to_i).reduce(0) do |sum, n|
    sum + n / 3 - 2
  end
=begin
  # Of course you can also do it explicitely, with similar performance
  sum = 0
  s.each do |line|
    line = Integer(line)
    sum += line / 3 - 2
  end
  sum
=end
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
