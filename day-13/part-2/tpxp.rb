class GameRunner
  def initialize(prgm)
    @input = prgm.clone
    @input[0] = 2
    @i = 0
    @relative_base = 0
    @score = 0
    @map = Hash.new {|h,k| h[k] = Hash.new(0) }
    @ball = nil
    @bar = nil
  end

  def run
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
        # Our strategy is simply to follow the ball - perhaps not optimal but works
        @input[modes[0] == 0 ? a[1] : @relative_base + a[1]] = (@ball - @bar)/([(@bar - @ball).abs, 1].max)
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
    loop do
      x = run
      y = run
      t = run
      @map[y][x] = t unless x == -1 and y == 0
      @score = t if x == -1 and y == 0
      @bar = x if t == 3
      @ball = x if t == 4
    end
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
    (bound_y0...bound_y1).each do |y|
      (bound_x0...bound_x1).each do |x|
        print(@map[y][x] == 0 ? " " : @map[y][x])
      end
      puts
    end
  end

  def score
    @score
  end
end

def run(s)
  prgm = s[0].split(',').map &:to_i
  robot = GameRunner.new prgm
  catch :haltAndCatchFire do
    robot.play
  end
  robot.score
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"