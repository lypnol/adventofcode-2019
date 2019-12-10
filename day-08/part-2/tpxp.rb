WIDTH = 25
HEIGHT = 6
def run(s)
  s = s[0]
  img = Array.new WIDTH * HEIGHT, "2"
  (s.length / (WIDTH*HEIGHT)).times do |i|
    l = s[i * HEIGHT * WIDTH...(i+1)*WIDTH * HEIGHT]
    l.length.times do |j|
      img[j] = l[j] if img[j] == "2"
    end
  end
=begin
  HEIGHT.times do |i|
    puts img[i*WIDTH...(i+1)*WIDTH].join ''
  end
=end
  puts img.join
end

starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000
puts "_duration:#{elapsed}\n#{answer}" 
