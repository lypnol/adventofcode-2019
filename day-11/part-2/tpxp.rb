class StatefulRunner
    def initialize(prgm, inputvals)
      @input = prgm.clone
      @i = 0
      @inputvals = inputvals
      @relative_base = 0
    end
  
    def run(inputvals)
      @inputvals = inputvals
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
    map = Hash.new {|h,k| h[k] = Hash.new }
    map[0][0] = 1
    robot = StatefulRunner.new(prgm, [])
    x, y = [0,0]
    dx, dy = [0,-1]
    catch :haltAndCatchFire do
        loop do
            o = robot.run([(map[x][y] or 0)])
            map[x][y] = o if o != (map[x][y] or 0)
            case robot.run([])
                when 0
                    dx, dy = [dy, -dx]
                when 1
                    dx, dy = [-dy, dx]
                else
                    throw :unknownOutput
            end
            x += dx
            y += dy
        end
    end
    x1, x2 = map.keys.filter{|k|
      map[k].values.min.to_i > 0
    }.minmax
    y1, y2 = [0, 0]
    map.each_value do |val|
        y3, y4 = val.keys.minmax
        next if !y3 or !y4
        y1 = y3 if y3 < y1
        y2 = y4 if y4 > y2
    end

    res = ""
    (y1..y2).each do |y|
        (x1..x2).each do |x|
          res += (map[x][y] or 0).to_s
        end
        # Just so that the output is accepted by the parser
        res += "0"
    end
    res
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"