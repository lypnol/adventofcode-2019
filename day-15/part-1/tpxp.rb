class GameRunner
  def initialize(prgm)
    @input = prgm.clone
    # @input[0] = 2
    @i = 0
    @relative_base = 0
    @pos_x = 0
    @pos_y = 0
    @to_explore = [[0,1], [1,0], [0, -1], [-1, 0]]
    @map = Hash.new { |h,k| h[k] = Hash.new }
    @map[0][0] = 'O'
  end

  def run(inputValue)
    # throw :tooMuchInput if @inputvals.length > 2
    loop do
      a = @input[@i..@i+3] + [0,0,0,0]
      code = a[0] % 100
      modes = 3.times.to_a.map { |i| (a[0] / (10 ** (i+2))) % 10}

      v = 3.times.to_a.map { |i|
        r = a[i+1].to_i
        r = @input[r] if modes[i] == 0
        r = @input[@relative_base + r] if modes[i] == 2
        r.to_i
      }
      case code
      when 99
        throw :haltAndCatchFire
      when 1
        @input[modes[2] == 0 ? a[3] : @relative_base + a[3]] = v[0] + v[1]
        @i += 4
      when 2
        @input[modes[2] == 0 ? a[3] : @relative_base + a[3]] = v[0] * v[1]
        @i += 4
      when 3
        @input[modes[0] == 0 ? a[1] : @relative_base + a[1]] = inputValue
        #print_map
        @i += 2
      when 4
        @i += 2
        return v[0]
      when 5
        @i = v[0] != 0 ? v[1] : @i + 3
      when 6
        @i = v[0] == 0 ? v[1] : @i + 3
      when 7
        @input[modes[2] == 0 ? a[3] : @relative_base + a[3]] = v[0] < v[1] ? 1 : 0
        @i += 4
      when 8
        @input[modes[2] == 0 ? a[3] : @relative_base + a[3]] = v[0] == v[1] ? 1 : 0
        @i += 4
      when 9
        @relative_base += v[0]
        @i += 2
      else
        throw :unknownCode
      end
    end
    throw :didNotOutput
  end

  def maybe_add_explore(pos_y, pos_x)
    @to_explore.push [pos_y, pos_x] unless @map[pos_y][pos_x]
  end

  def play
    loop do
      throw :onlyWalls if @to_explore.length == 0
      target = @to_explore.shift
      path = path_finder target
      #output = nil
      while @pos_x != target[1] or @pos_y != target[0]
        next_pos = path.pop
        dy = next_pos[0] <=> @pos_y
        dx = next_pos[1] <=> @pos_x
        cmd = 1 if dy == -1
        cmd = 2 if dy == 1
        cmd = 3 if dx == -1
        cmd = 4 if dx == 1
        # puts "Command is #{cmd}"
        output = run cmd
        @pos_y += dy
        @pos_x += dx
        # puts "Output is #{output}"
        break if @pos_x == target[1] and @pos_y == target[0]
        throw :unexpectedOutput if output != 1
      end
      if output == 0
        @map[@pos_y][@pos_x] = '#'
        @pos_x -= dx
        @pos_y -= dy
      elsif output == 1
        @map[@pos_y][@pos_x] = '.'
        [-1, 1].each { |dy| maybe_add_explore @pos_y + dy, @pos_x }
        [-1, 1].each { |dx| maybe_add_explore @pos_y, @pos_x + dx }
      else
        @map[@pos_y][@pos_x] = 'X'
      end
      break if output == 2
    end
    # How to get back home ?
    # puts [@pos_y, @pos_x].inspect
    # print_map
    path = path_finder [0, 0]
    path.length
  end

  def print_map
    # Debug code
    bound_x0 = 0
    bound_x1 = 0
    bound_y0, bound_y1 = @map.keys.minmax
    @map.keys.each do |y|
      a,b = @map[y].keys.minmax
      bound_x0 = a if a < bound_x0
      bound_x1 = b if b > bound_x1
    end
    (bound_y0..bound_y1).each do |y|
      (bound_x0..bound_x1).each do |x|
        print(@map[y][x] ? @map[y][x] : " ")
      end
      puts
    end
  end

  def path_finder(target)
    # Dijkstra algorithm
    @queue = [[@pos_y, @pos_x]]
    @prev_map = Hash.new
    @path_map = Hash.new
    @path_map[@queue[0]] = 0
    explore until @prev_map[target]
    path = []
    while @prev_map[target]
      path.push target
      target = @prev_map[target]
    end
    path
  end
  def explore
    throw :nothingToExplore if @queue.length == 0
    y, x = @queue.shift
    d = @path_map[[y, x]] + 1
    return unless @map[y][x]
    return if @map[y][x] == '#'
    [-1, 1].each do |dx|
      next if @path_map[[y, x + dx]]
      @path_map[[y, x + dx]] = d
      @prev_map[[y, x + dx]] = [y,x]
      @queue.push [y,x + dx]
    end
    [-1, 1].each do |dy|
      next if @path_map[[y + dy, x]]
      @path_map[[y + dy, x]] = d
      @prev_map[[y + dy, x]] = [y,x]
      @queue.push [y + dy, x]
    end
  end
end

def run_sol(s)
  prgm = s[0].split(',').map &:to_i
  robot = GameRunner.new prgm
  robot.play
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run_sol(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"