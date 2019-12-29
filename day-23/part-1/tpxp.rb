class IntCodeInterpreter
  def initialize(prgm, input_value = [])
    prgm = prgm[0].split(',').map &:to_i
    @prgm = prgm
    reset
    @input_value = input_value
  end

  def reset
    @input = @prgm.clone
    @i = 0
    @relative_base = 0
  end

  def add_input(input = [])
    @input_value += input
  end

  def run(input_value = [])
    @input_value += input_value
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
        throw :noInput if @input_value.length == 0
        # @input_value = gets.chars.map &:ord if @input_value.length == 0
        @input[modes[0] == 0 ? a[1] : @relative_base + a[1]] = @input_value.shift
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

class Solution
  def run(source)
    @runner = 50.times.to_a.map {|i| IntCodeInterpreter.new source, [i] }
    queue = Array.new(50) { [] }
    loop do
      50.times do |i|
        input = queue[i] || [-1]
        input = [-1] if input.empty?
        queue[i] = []
        @runner[i].add_input input
        res = []
        catch :noInput do loop do
          res.push @runner[i].run
        end end
        (res.length / 3).times do |j|
          dest, x, y = res[3*j...3*(j+1)]
          return y if dest == 255
          queue[dest] += [x,y]
        end
      end
    end
  end
end

starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = Solution.new
answer = answer.run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
