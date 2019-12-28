MAP_SIZE = 5

def adjacent_bugs(bugs, x, y, l)
  res = 0
  [-1, 1].each do |dx|
    next if x+dx < 0 or x+dx >= MAP_SIZE
    res += 1 if bugs[[x+dx, y, l]]
  end
  [-1, 1].each do |dy|
    next if y+dy < 0 or y+dy >= MAP_SIZE
    res += 1 if bugs[[x, y+dy, l]]
  end
  # Is it on the outside?
  if [0,4].include? x
    x_to_inspect = x == 0 ? 1 : 3
    res += 1 if bugs[[x_to_inspect, 2, l-1]]
  end
  if [0,4].include? y
    y_to_inspect = y == 0 ? 1 : 3
    res += 1 if bugs[[2, y_to_inspect, l-1]]
  end
  # Is it on the inside?
  if [[2,1], [2,3]].include? [x,y]
    y_to_inspect = y == 1 ? 0 : 4
    MAP_SIZE.times do |x|
      res += 1 if bugs[[x, y_to_inspect, l+1]]
    end
  end
  if [[1,2], [3,2]].include? [x,y]
    x_to_inspect = x == 1 ? 0 : 4
    MAP_SIZE.times do |y|
      res += 1 if bugs[[x_to_inspect, y, l+1]]
    end
  end
  res
end

def run(map)
  bugs = {}
  map.length.times do |y|
    map[y].length.times do |x|
      bugs[[x, y, 0]] = true if map[y][x] == '#'
    end
  end
  200.times do |i|
    nbugs = {}
    bugs.keys.each do |x,y,l|
      # Does the bug survive?
      nbugs[[x,y,l]] = true if adjacent_bugs(bugs, x, y, l) == 1
      # Do we create neighbors?
      [-1, 1].each do |dx|
        dl = 0
        dy = 0
        if [x+dx, y+dy] == [2,2]
          nx = 2 - 2*dx
          5.times do |ny|
            next if bugs[[nx, ny, l+1]] or nbugs[[nx, ny, l+1]]
            nbugs[[nx, ny, l+1]] = true if [1,2].include? adjacent_bugs(bugs, nx, ny, l+1)
          end
          next
        end
        if x+dx < 0
          dl = -1
          dx = 1 - x
          dy = 2 - y
        end
        if x+dx >= MAP_SIZE
          dl = -1
          dx = 3 - x
          dy = 2 - y
        end
        next if bugs[[x+dx, y+dy, l+dl]] or nbugs[[x+dx, y+dy, l+dl]]
        nbugs[[x+dx, y+dy, l+dl]] = true if [1,2].include? adjacent_bugs(bugs, x+dx, y+dy, l+dl)
      end
      [-1, 1].each do |dy|
        dl = 0
        dx = 0
        if [x+dx, y+dy] == [2,2]
          ny = 2 - 2*dy
          5.times do |nx|
            next if bugs[[nx, ny, l+1]] or nbugs[[nx, ny, l+1]]
            nbugs[[nx, ny, l+1]] = true if [1,2].include? adjacent_bugs(bugs, nx, ny, l+1)
          end
          next
        end
        if y+dy < 0
          dl = -1
          dx = 2 - x
          dy = 1 - y
        end
        if y+dy >= MAP_SIZE
          dl = -1
          dx = 2 - x
          dy = 3 - y
        end
        next if bugs[[x+dx, y+dy, l+dl]] or nbugs[[x+dx, y+dy, l+dl]]
        nbugs[[x+dx, y+dy, l+dl]] = true if [1,2].include? adjacent_bugs(bugs, x+dx, y+dy, l+dl)
      end
    end
    bugs = nbugs
  end
  bugs.length
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].chomp.lines.map &:chomp)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
