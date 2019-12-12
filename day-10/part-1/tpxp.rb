def reduce(dx,dy)
    l = dx.gcd(dy)
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
        [-i, +i].each do |gdx|
            (-i..+i).each do |gdy|
                nx = x + gdx
                ny = y + gdy
                # Out of bounds
                next if nx < 0 or ny < 0
                next if map[nx] == nil or map[nx][ny] == nil
                next if map[nx][ny] != '#'
                # Make it irreductible
                # Careful, if you set gdx here it will be used for the rest!
                dx, dy = reduce(gdx, gdy)
                next if blocked[dx][dy]
                blocked[dx][dy] = true
                visible += 1
            end
        end
        # So basically this is a copy paste from the above but with gdx and gdy inverted
        [-i, +i].each do |gdy|
            (-i..+i).each do |gdx|
                nx = x + gdx
                ny = y + gdy
                # Out of bounds
                next if nx < 0 or ny < 0
                next if map[nx] == nil or map[nx][ny] == nil
                next if map[nx][ny] != '#'
                # Make it irreducible
                dx, dy = reduce(gdx, gdy)
                next if blocked[dx][dy]
                blocked[dx][dy] = true
                visible += 1
            end
        end
    end
    visible
end

def run(map)
    # Sanitization: remove the line break at the end of lines
    map = map.map &:strip
    v = 0
    map.length.times do |x|
        map[x].length.times do |y|
            next if map[x][y] == '.'
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
