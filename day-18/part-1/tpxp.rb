require 'set'

class Solution
  def initialize(map)
    map = map.map &:chomp
    @map = map
    # Find out where the keys (and doors) are
    @key_pos = Hash.new
    @prec = Hash.new
    @dist = Hash.new
    @req = Hash.new
    @start_pos = nil
    (0...map.length).each do |y|
      (0...map[y].length).each do |x|
        next if %w(# .).include? map[y][x]
        @start_pos = [y,x] if map[y][x] == '@'
        @key_pos[map[y][x]] = [y,x]
      end
    end
    first_explore
    throw :noStart unless @start_pos
    @d_cache = Hash.new
=begin
    ("a".."z").each do |l|
      puts l
      puts @req[@key_pos[l]]
    end
=end
  end

  def first_explore
    @to_explore = [@start_pos]
    @dist[@start_pos] = 0
    @req[@start_pos] = Set.new
    explore while @to_explore.length > 0
  end

  def explore
    y,x = @to_explore.shift
    d = @dist[[y,x]] + 1
    throw :unexpectedDistance unless d
    req = @req[[y,x]]
    throw :unexpectedReq unless req
    [-1,1].each do |dy|
      next if y + dy < 0 or y + dy >= @map.length
      next if @map[y+dy][x] == '#'
      next if @dist[[y+dy,x]] and @dist[[y+dy,x]] <= d
      r = Set.new req
      r.add @map[y+dy][x] if "A" <= @map[y+dy][x] and "Z" >= @map[y+dy][x]
      @req[[y+dy,x]] = r
      @prec[[y+dy,x]] = [y,x]
      @dist[[y+dy,x]] = d
      @to_explore.push [y+dy,x]
    end
    [-1,1].each do |dx|
      next if x + dx < 0 or x + dx >= @map[y].length
      next if @map[y][x+dx] == '#'
      next if @dist[[y,x+dx]] and @dist[[y,x+dx]] <= d
      r = Set.new req
      r.add @map[y][x+dx] if "A" <= @map[y][x+dx] and "Z" >= @map[y][x+dx]
      @req[[y,x+dx]] = r
      @prec[[y,x+dx]] = [y,x]
      @dist[[y,x+dx]] = d
      @to_explore.push [y,x+dx]
    end
  end

  # An optimization to the distance computation
  def distance_between (a,b)
    return @d_cache[[a,b]] if @d_cache[[a,b]]
    d = _distance_between(a,b)
    @d_cache[[a,b]] = d
    @d_cache[[b,a]] = d
    d
  end

  def is_close_to_start(p)
    return false unless p
    return false if (p[0] - @start_pos[0]).abs > 1
    (p[1] - @start_pos[1]).abs < 2
  end

  def _distance_between (a,b)
    # Note : a and b are interchangeable
    precs = {}
    d = 0
    p = @key_pos[a]

    while p do
      precs[p] = d
      d += 1
      p = @prec[p]
      break if is_close_to_start p
    end
    d_start = d
    pos_start = p
    p = @key_pos[b]
    d = 0
    while p do
      return d + precs[p] if precs[p]
      d += 1
      p = @prec[p]
      # Workaround for cases where you don't have to go through the start position since there's an empty square around
      if is_close_to_start p and pos_start
        return d_start + d + (pos_start[0] - p[0]).abs + (pos_start[1] - p[1]).abs
      end
    end
    throw :noPathFound
  end

  def run
    solutions = Hash.new {|h,k| h[k] = []}
    solutions[0] = [["@"]]
    keys_length = @key_pos.filter{|k| k == k.downcase}.length - 1
    letters = ("a".."z")
    explored = Hash.new Float::INFINITY
    loop do
      d = solutions.keys.min
      puts d
      sols = solutions[d]
      solutions.delete d
      sols.each do |sol|
        # puts sol.inspect
        return d if sol.length == keys_length+1 # Don't forget the "@"
        # puts [d, sol.length].inspect
        l = sol.last
        letters.each do |k|
          next if sol.include? k # Includes k == l
          dep = @req[@key_pos[k]]
          next unless dep # Enable this if your examples have less than 26 letters
          catch :missingKey do
            dep.each do |door|
              throw :missingKey unless sol.include? door.downcase
            end
            msol = sol.clone
            msol.push k
            # At first, I wanted to use [z,k] as a key but that's quite inefficient
            z = sol.sort
            z.push k
            nd = d + distance_between(l,k)
            next if explored[z] <= nd
            explored[z] = nd
            solutions[nd].push msol
          end
        end
      end
    end
  end
end

starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
sol = Solution.new ARGV[0].chomp.lines
answer = sol.run
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
