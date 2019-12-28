def score(map)
  map = map.join
  res = 0
  map.length.times do |i|
    res += 2**i if map[i] == '#'
  end
  res
end

def adjacent_bugs(map, x, y)
  res = 0
  [-1, 1].each do |dx|
    next if x+dx < 0 or x+dx >= map[y].length
    res += 1 if map[y][x+dx] == '#'
  end
  [-1, 1].each do |dy|
    next if y+dy < 0 or y+dy >= map.length
    res += 1 if map[y+dy][x] == '#'
  end
  res
end

def run(map)
  seen = {}
  seen[score map] = true
  loop do
    nmap = []
    map.length.times do |y|
      line = ""
      map[y].length.times do |x|
        if map[y][x] == "#"
          line += adjacent_bugs(map, x, y) == 1 ? "#" : "."
        else
          line += ([1,2].include? adjacent_bugs(map, x, y)) ? "#" : "."
        end
      end
      nmap.push line
    end
    map = nmap
    s = score map
    return s if seen[s]
    seen[s] = true
  end
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].chomp.lines.map &:chomp)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
