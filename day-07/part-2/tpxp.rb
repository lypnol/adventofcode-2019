class StatefulRunner

  def initialize(prgm, inputvals)
    @input = prgm.clone
    @cur_ptr = 0
    @inputvals = inputvals
  end

  def run(inputvals)
    @inputvals += inputvals
    throw :tooMuchInput if @inputvals.length > 2
    loop do
      a0, a1, a2, a3 = @input[@cur_ptr..@cur_ptr+3] + [0,0,0] # Hack to make sure we set all variables to integers
      code = a0 % 100
      v1 = a0 / 100 % 10 == 1 ? a1 : @input[a1].to_i
      v2 = a0 / 1000 % 10 == 1 ? a2 : @input[a2].to_i
      v3 = a0 / 10000 == 1 ? a3 : @input[a3].to_i
      case code
      when 99
        throw :haltAndCatchFire
        break
      when 1
        @input[a3] = v1 + v2
        @cur_ptr += 4
      when 2
        @input[a3] = v1 * v2
        @cur_ptr += 4
      when 3
        @input[a1] = @inputvals.shift
        throw :noInput if @input[a1].nil?
        @cur_ptr += 2
      when 4
        # Don't forget to increase the instruction pointer so that we don't return the same value next time we're called
        @cur_ptr += 2
        return v1
      when 5
        @cur_ptr = v1 != 0 ? v2 : @cur_ptr + 3
      when 6
        @cur_ptr = v1 == 0 ? v2 : @cur_ptr + 3
      when 7
        @input[a3] = v1 < v2 ? 1 : 0
        @cur_ptr += 4
      when 8
        @input[a3] = v1 == v2 ? 1 : 0
        @cur_ptr += 4
      else
        throw :unknownCode
      end
    end
    throw :didNotOutput
  end
end

def run(s)
  prgm = s[0].split(',').map &:to_i
  max = 0
  (5..9).to_a.permutation do |phases|
    val = 0
    last_final = 0
    runners = (0..4).map { |i| StatefulRunner.new prgm, [phases[i]] }
    catch :haltAndCatchFire do
      loop do
        5.times do |i|
          val = runners[i].run([val])
        end
        last_final = val
      end
    end
    max = last_final if last_final > max
  end
  max
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"