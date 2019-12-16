def run(s)
  l = s[0].chars.map(&:to_i)
  offset = l[0...7].join.to_i
  throw :willTakeAges if offset < l.length * 5000
  l = (l * 10000)[offset..]
  # Here's the trick: since we're in the second half of the array, the next value is the sum
  # of the values from this value to the end of the array
  # Which means that at every iteration we can compute the whole sum then subtract the values one by one
  100.times do
    sum = l.reduce :+
    l.length.times do |i|
      p = l[i]
      l[i] = sum.abs % 10
      sum -= p
    end
  end
  l[0...8].join
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
