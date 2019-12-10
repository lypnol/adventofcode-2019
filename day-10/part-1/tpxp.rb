def reduce(dx,dy)
    l = [dx, dy].map(&:abs).reject{ |n| n == 0 }.min
    if dx % l == 0 and dy % l == 0
        dx /= l
        dy /= l
    end
    [dx, dy]
end

def how_many_visible_from(x, y, map)
    map_width = map.length
    map_height = map[0].length
    r_max = [map_width, map_height].max
    blocked = Hash.new { |h,k| h[k] = Hash.new false }
    visible = 0
    (1...r_max).each do |i|
        # puts ["q", i, visible].inspect
        [-i, +i].each do |dx|
            (-i..+i).each do |dy|
                nx = x + dx
                ny = y + dy
                # Out of bounds
                next if nx < 0 or ny < 0
                next if map[nx] == nil or map[nx][ny] == nil
                # Make it irreductible
                dx, dy = reduce(dx, dy)
                #puts [nx, ny].inspect
                next if blocked[dx][dy]
                next if map[nx][ny] != '#'
                blocked[dx][dy] = true
                visible += 1
            end
        end
        #puts "next"
        # So basically this is a copy paste from the above but with dx and dy inverted
        [-i, +i].each do |dy|
            (-i..+i).each do |dx|
                nx = x + dx
                ny = y + dy
                # Out of bounds
                next if nx < 0 or ny < 0
                next if map[nx] == nil or map[nx][ny] == nil
                # Make it irreductible
                dx, dy = reduce(dx, dy)
                #puts [nx, ny].inspect
                next if blocked[dx][dy]
                next if map[nx][ny] != '#'
                blocked[dx][dy] = true
                visible += 1
            end
        end
    end
    visible
end

def run(map)
    #puts 'NEW RUN'
    v = 0
    map.length.times do |x|
        map[x].length.times do |y|
            next if map[x][y] == '.'
            #puts 'yo'
            #puts [x,y].inspect
            n = how_many_visible_from(x, y, map)
            v = n if n > v
        end
    end
    v
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
