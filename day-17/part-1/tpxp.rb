class GameRunner
  def initialize(prgm)
    @input = prgm.clone
    @i = 0
    @relative_base = 0
    @map = Hash.new { |h,k| h[k] = Hash.new }
  end

  def run(inputValue = 0)
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
        throw :noInput
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

  def play
    res = ""
    catch :haltAndCatchFire do loop do
      res += run.chr
    end end
    res = res.lines.map &:chomp
    sum = 0
    (1...res.length - 1).each do |i|
      (1...res[i].length - 1).each do |j|
        next if res[i][j] == '.'
        next if res[i+1][j] == '.'
        next if res[i-1][j] == '.'
        next if res[i][j-1] == '.'
        next if res[i][j+1] == '.'
        sum += i * j
      end
    end
    sum
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