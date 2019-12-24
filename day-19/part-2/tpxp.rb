require 'set'
class IntCodeInterpreter
  def initialize(prgm)
    prgm = prgm[0].split(',').map &:to_i
    @prgm = prgm
    reset
    @input_value = []
  end

  def reset
    @input = @prgm.clone
    @i = 0
    @relative_base = 0
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
        @input[modes[0] == 0 ? a[1] : @relative_base + a[1]] = @input_value.shift
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
end

class Solution
  def query(i,j)
    @runner.reset
    @runner.run([i,j])
  end

  def run(source)
    @runner = IntCodeInterpreter.new source
    start = [0]
    final = [0]
    (100..9999).each do |i|
      j = start.last
      loop do
        break if query(i,j) == 1
        j += 1
      end
      start.push j
      k = [j+1, final[-1]].max
      loop do
        break if query(i,k) == 0
        k += 1
      end
      final.push k-1
      # Hold on, is this a correct corner?
      if k-j > 100
        # Our square proposal is [i,k-100], [i, k-1], [i,k-100], [i+99, k-1], [i+99, j]
        return (i*10000 + k-100) if query(i+99, k-1) == 1 and query(i+99, k-100) == 1 # and query(i,k-1) == 1 and query(i,j) == 1
      end
    end
    throw :notFound
  end
end

starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = Solution.new
answer = answer.run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
