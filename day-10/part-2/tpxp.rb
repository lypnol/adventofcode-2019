def reduce(dx,dy)
    l = dx.gcd(dy)
    if dx % l == 0 and dy % l == 0
        dx /= l
        dy /= l
    end
    [dx, dy]
end

class Day10Sol
    def initialize(map)
        @map = map
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
                    # Make it irreductible
                    dx, dy = reduce(gdx, gdy)
                    next if blocked[dx][dy]
                    blocked[dx][dy] = true
                    visible += 1
                end
            end
        end
        visible
    end

=begin
    def laser(x, y)
        dx, dy = reduce(x - @X, y - @Y)
        px, py = [@X, @Y]
        while px > 0 and py > 0 and @map[px] != nil and @map[px][py] != nil and @map[px][py] != '#'
            px += dx
            py += dy
        end
        return if not @map[px] or not @map[px][py]
        if @map[px][py] == '#'
            @n += 1
            @map[px][py] = "*"
        end
        if @n == 200
            @lastPos = [px, py]
            throw :shot200th
        end
    end
=end
    def run()
        v = 0
        p = nil
        map = @map
        map.length.times do |x|
            map[x].length.times do |y|
                next if map[x][y] == '.'
                n = how_many_visible_from(x, y, @map)
                p = [x,y] if n > v
                v = n if n > v
            end
        end
        @X, @Y = p
        #puts p.inspect
        map[@X][@Y] = "A"
=begin
        @n = 0
        catch :shot200th do
            loop do
                # UP
                lx = 0
                (@Y...map[0].length).each { |ly| self.laser(lx, ly) }

                # RIGHT
                ly = map[0].length - 1
                (0...map.length).each { |lx| self.laser(lx, ly)}

                # BOTTOM
                lx = map.length - 1
                (0...map[0].length).each { |ly| self.laser(lx, ly) }

                # LEFT
                ly = 0
                (0...map.length).each { |lx| self.laser(lx, ly)}

                # UP (end)
                lx = 0
                (0...@Y).each { |ly| self.laser(lx, ly) }

                puts "======"
                puts @map
                puts "======"
            end
        end
=end
        # A better approach: start by noting all angles for the asteroids
        angles = Hash.new {|h,k| h[k] = []}
        (0...map.length).each do |x|
            (0...map[x].length).each do |y|
                next if map[x][y] != '#'
=begin
                dy = x - @X
                dx = y - @Y
                if dy == 0
                    angle = dx > 0 ? Math::PI/2 : Math::PI*3/2
                else
                    angle = Math::atan(dx/dy)
                end
                angle += Math::PI if dy < 0
                angle += 2*Math::PI if dy > 0 and dx < 0
=end
                angle = Math::atan2(x - @X, y - @Y)
                angles[angle].push([x,y])
            end
        end
        angles.each_pair { |k, val| angles[k] = val.sort_by { |x,y| (x - @X).abs + (y-@Y).abs }}
        corr_angles = Hash.new
        angles.each_key { |k| corr_angles[k < - Math::PI/2 ? k + Math::PI*2: k] = angles[k]}
        angles_in_order = corr_angles.keys.sort
        n = 0
        last = nil
        catch :shot200th do
            loop do
                angles_in_order.each do |a|
                    last = corr_angles[a].shift
                    next unless last

                    # map[last[0]][last[1]] = 'x'
                    n += 1
                    throw :shot200th if n == 200
                end
            end
        end
        last[1] * 100 + last[0]
    end
end

def run(map)
    # Sanitization: remove the line break at the end of lines
    map = map.map &:chomp

    sol = Day10Sol.new(map)

    sol.run
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
