class StatefulRunner
  def initialize(prgm, inputvals)
    @input = prgm.clone
    @i = 0
    @inputvals = inputvals
    @relative_base = 0
  end

  def run(inputvals = [])
    @inputvals += inputvals
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
        throw :noInput if @inputvals.length == 0
        @input[modes[0] == 0 ? a[1] : @relative_base + a[1]] = @inputvals.shift
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
end

def run(s)
  prgm = s[0].split(',').map &:to_i
  map = Hash.new {|h,k| h[k] = Hash.new(0) }
  robot = StatefulRunner.new(prgm, [])
  catch :haltAndCatchFire do
    loop do
      x = robot.run
      y = robot.run
      t = robot.run
      map[y][x] = t
    end
  end
  # puts map
  k = map.values.reduce(0) do |a, v|
    a + v.values.reduce(0) { |b,w| b + (w == 2 ? 1:0)}
  end
=begin
  bound_x0 = 0
  bound_x1 = 0
  bound_y0, bound_y1 = map.keys.minmax
  map.keys.each do |y|
    a,b = map[y].keys.minmax
    bound_x0 = a if a < bound_x0
    bound_x1 = b if b > bound_x1
  end
  (bound_y0...bound_y1).each do |y|
    (bound_x0...bound_x1).each do |x|
      print (map[y][x] == 0 ? " " : map[y][x])
    end
    puts
  end
=end
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"