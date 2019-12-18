require 'set'
class GameRunner
  def initialize(prgm)
    @prgm = prgm
    reset
    @map = Hash.new { |h,k| h[k] = Hash.new }
    @inputValue = []
  end

  def reset
    @input = @prgm.clone
    @i = 0
    @relative_base = 0
  end

  def run(inputValue = [])
    @inputValue += inputValue
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
        throw :noInput if @inputValue.length == 0
        @input[modes[0] == 0 ? a[1] : @relative_base + a[1]] = @inputValue.shift
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

  def play
    res = ""
    catch :haltAndCatchFire do loop do
      res += run.chr
    end end
    res = res.chomp!.lines.map &:chomp
    @to_explore = 0
    robot_pos = nil
    (0...res.length).each do |i|
      (0...res[i].length).each do |j|
        robot_pos = [i,j] if %w(v ^ > <).include? res[i][j]
        next if res[i][j] == '.'
        # How many
        @to_explore += 1
      end
    end
    # puts res
    @map = res
    throw :couldNotFindTheRobot unless robot_pos
    # puts robot_pos.inspect
    @dx, @dy = [0,0]
    @pos_y, @pos_x = robot_pos
    case res[robot_pos[0]][robot_pos[1]]
    when '^'
      @dy = -1
    when 'v'
      @dy = 1
    when '<'
      @dx = -1
    when '>'
      @dx = 1
    else
      throw :couldNotDetermineTheRobotOrientation
    end
    @actions = []
    find_path
    #puts @actions.inspect
    # puts @map
    #puts @actions.length
    # Our path, we want to optimize this
    @actions = @actions.join
    # puts @actions
    # puts @actions
    # puts @repeating
    @functions = []
    catch :foundIt do backtracking_solution end
    # puts "functions are"
    # puts @functions.inspect
    # puts "actions are"
    # puts @actions
    input = @actions.chars.join ','
    input += "\n"
    input += @functions.join "\n"
    input += "\nn\n"
    # puts input
    reset
    throw :unexpectedFirstValue if @input[0] != 1
    @input[0] = 2
    @inputValue = input.chars.map &:ord
    v = nil
    catch :haltAndCatchFire do loop { v = run} end
    v
  end

  def max_d
    [1].each do |i|
      return i-1 if (@pos_y + @dy * i < 0 or @pos_y + @dy * i >= @map.length)
      return i-1 if (@pos_x + @dx * i < 0 or @pos_x + @dx * i >= @map[0].length)
      return i-1 if @map[@pos_y + @dy * i][@pos_x + @dx * i] == '.'
    end
    1
  end

  def find_path
    d = max_d
    loop do
      # Go straight as far as we can
      while d > 0
        d = max_d
        @actions.push d if d > 0
        @pos_y += d * @dy
        @pos_x += d * @dx
        # puts @map
        @map[@pos_y][@pos_x] = 'x'
      end
      # Is there something on the left ?
      simulate 'L'
      d = max_d
      if d == 0
        # Oops, reverse and try on the right
        simulate 'R'
        simulate 'R'
        d = max_d
        return if d == 0
        @actions.push 'R'
      else
        @actions.push 'L'
      end
    end
  end

  def simulate(move)
    if move == 'L'
      @dx, @dy = [@dy, -@dx]
    elsif move == 'R'
      @dx, @dy = [-@dy, @dx]
    else
      move.to_i.times do
        @pos_x += @dx
        @pos_y += @dy
        throw :badSolution if @pos_y < 0 or @pos_y > @map.length
        throw :badSolution if @pos_x < 0 or @pos_x > @map[0].length
        throw :badSolution if @map[@pos_y][@pos_x] == '.'
      end
      @explored += move.to_i
      throw :foundIt if @explored == @to_explore
    end
  end

  def simulate_function(f)
    f.each { |move| simulate move }
  end

  # A first attempt at a backtracking algorithm
=begin
  def explore
    # If all functions are defined, see if we can add one
    if @functions.length >= 3
      if @chain.length >= 20
        throw :badSolution
      end
      @functions.each do |f|
        @chain.push f
        dx, dy, px, py, explored = [@dx, @dy, @pos_x, @pos_y, @explored]
        catch :badSolution do
          simulate_function f
          explore
        end
        @dx, @dy, @pos_x, @pos_y, @explored = [dx, dy, px, py, explored]
        @chain.pop
      end
      throw :badSolution
    end
    # Function generator - could probably be smarter, like by starting as far as possible
    20.times do |i|
      %w(L R 1 2 3 4 5 6 7 8 9).repeated_permutation(i) do |f|
        @functions.push f
        catch :badSolution do
          explore
        end
        @functions.pop
      end
    end
  end
functions are
["R8L91L93R4", "R8L93R4R4", "R8L91R8"]
actions are
ABACABCBCB

=end

  def compress_function (function)
    res = []
    function.chars.each do |v|
      unless %w(L R).include? v
        v = v.to_i
        v += res.pop if res[-1].is_a? Numeric
      end
      res.push v
    end
    res.join ','
  end

  # Find correct functions
  def backtracking_solution
    if /^[ABC]+$/.match? @actions
      throw :foundIt if @actions.length <= 20
      throw :badSolution
    end
    throw :badSolution if @functions.length >= 3
    prev = @actions
    rank = @functions.length
    # Where do we start?
    i = 0
    while %w(A B C).include? @actions[i]
      i += 1
    end
    # Until where do we go?
    (i..@actions.length).reverse_each do |j|
      # Try a new function
      f = @actions[i..j]
      next if /[ABC]/.match? f
      c = compress_function(f)
      next if c.length > 20
      letter = (@functions.length + 'A'.ord).chr
      @functions.append c
      @actions = @actions.gsub f, letter
      catch :badSolution do
        backtracking_solution
      end
      # That didn't work
      @actions = prev
      @functions.pop
    end
    throw :badSolution
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