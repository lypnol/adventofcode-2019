class Solution
  def find_portals
    # Skip spaces and #,.
    to_skip = %w(\  # .)
    @map.length.times do |y|
      @map[y].length.times do |x|
        next if to_skip.include? @map[y][x]
        label = @map[y][x]
        # See if it's a portal
        # Our strategy to avoid duplicates is to look for other letters on the right or below
        if not @map[y][x+1] or to_skip.include? @map[y][x+1]
          next if not @map[y+1] or not @map[y+1][x] or to_skip.include? @map[y+1][x]
          label += @map[y+1][x]
          [-1, 2].each do |dy|
            next unless @map[y+dy] and @map[y+dy][x]
            next if @map[y+dy][x] != '.'
            @portals[label].push [y+dy, x]
            @pos_to_portal[[y+dy, x]] = label
            break
          end
          next
        end
        label += @map[y][x+1]
        [-1, 2].each do |dx|
          next unless @map[y][x+dx]
          next if @map[y][x+dx] != '.'
          @portals[label].push [y, x+dx]
          @pos_to_portal[[y, x+dx]] = label
          break
        end
      end
    end
  end

  def initialize(map)
    @map = map
    @portals = Hash.new {|h,k| h[k] = []}
    @pos_to_portal = Hash.new
    find_portals
    # puts @portals.inspect
    # puts @pos_to_portal.inspect
  end

  def dimension_delta(x,y)
    return -1 if y < 10
    return -1 if y > @map.length - 10
    return -1 if x < 10
    return -1 if x > @map[5].length - 10
    +1
  end

  def run
    @to_explore = [@portals['AA'][0] + [0]]
    @dist = Hash.new Float::INFINITY
    throw :noStart unless @to_explore[0]
    @dist[@to_explore[0]] = -1
    while @to_explore.length > 0
      pos = @to_explore.shift
      y,x, dimension = pos
      d = @dist[pos] + 1
      [-1,1].each do |dx|
        r = explore_pos d, x+dx, y, dx, 0, dimension
        return r if r
      end
      [-1,1].each do |dy|
        r = explore_pos d, x, y+dy, 0, dy, dimension
        return r if r
      end
    end
  end

  def explore_pos(d, x,y, dx, dy, dimension)
    return if x < 0 or y < 0
    return unless @map[y] and @map[y][x]
    return if @map[y][x] == '#'
    if @map[y][x] == '.'
      return if @dist[[y,x, dimension]] <= d
      @dist[[y,x, dimension]] = d
      @to_explore.push [y,x, dimension]
    else
      # Portal
      label = @pos_to_portal[[y-dy,x-dx]]
      throw :couldNotFindPortal unless label
      return if label == 'AA'
      return d if label == 'ZZ' and dimension == 0
      return if label == 'ZZ'
      other_end = @portals[label].filter {|a| a != [y-dy, x-dx]}
      throw :badEnd if other_end.length != 1
      other_end = other_end[0]
      other_end += [dimension + dimension_delta(y-dy, x-dx)]
      return if other_end[-1] < 0
      return if other_end[-1] > 30 # Prevent too much recursion - increase if needed
      return if @dist[other_end] <= d
      @dist[other_end] = d
      @to_explore.push other_end
    end
    nil
  end
end

starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = Solution.new ARGV[0].chomp.lines.map &:chomp
answer = answer.run
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
