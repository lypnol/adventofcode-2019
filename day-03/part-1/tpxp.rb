def get_dx_dy(dir)
    case dir
        when 'U'
            dx, dy = [0,-1]
        when 'D'
            dx, dy = [0,1]
        when 'L'
            dx, dy = [-1, 0]
        when 'R'
            dx, dy = [1, 0]
    end
    [dx,dy]
end

def run(s)
    map = Hash.new { |h,k| h[k] = Hash.new(0) }
    x,y = [0,0]
    s[0].split(',').each do |command|
        dx, dy = get_dx_dy(command[0])
        length = command[1..].to_i
        length.times do |index|
            x += dx
            y += dy
            map[x][y] = 1
        end
    end
    x,y = [0,0]
    min_dist = Float::INFINITY
    s[1].split(',').each do |command|
        dx, dy = get_dx_dy(command[0])
        length = command[1..].to_i
        length.times do |index|
            x += dx
            y += dy
            if map[x][y] === 1
                min_dist = x.abs + y.abs if min_dist > x.abs + y.abs
            end
        end
    end
    min_dist
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
