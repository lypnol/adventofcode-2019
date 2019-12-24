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
    # Sort keys by area
    @keys_by_area = 4.times.to_a.map { [] }
    @key_pos.keys.each do |k|
      next if k == k.upcase
      n = 0
      n += 1 if @key_pos[k][1] > @start_pos[1]
      n += 2 if @key_pos[k][0] > @start_pos[0]
      @keys_by_area[n].push k
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
    # Any obvious solutions?
    4.times do |i|
      catch :notObvious do
        puts @keys_by_area[i].inspect
        @keys_by_area[i].each do |k|
          next unless @req[@key_pos[k]]
          puts @req[@key_pos[k]].inspect
          @req[@key_pos[k]].each do |l|
            puts l
            throw :notObvious unless @keys_by_area[i].include? l.downcase
          end
        end
        puts "#{i} seems obvious"
      end
    end
    throw :stop
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
    # We're starting in a corner now, not at the middle
    d = a == '@' ? d - 2 : d
    @d_cache[[a,b]] = d
    @d_cache[[b,a]] = d
    d
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
    end
    p = @key_pos[b]
    d = 0
    while p do
      return d + precs[p] if precs[p]
      d += 1
      p = @prec[p]
    end
    throw :noPathFound
  end

  def run
    solutions = Hash.new {|h,k| h[k] = []}
    solutions[0] = [["@" * 4]]
    keys_length = @key_pos.filter{|k| k == k.downcase}.length - 1
    explored = Hash.new Float::INFINITY
    loop do
      d = solutions.keys.min
      sols = solutions[d]
      solutions.delete d
      sols.each do |sol|
        positions = sol.pop
        return d if sol.length == keys_length # Don't forget the positions
        4.times do |i|
          # puts sol.inspect
          # puts [d, sol.length].inspect
          l = positions[i]
          @keys_by_area[i].each do |k|
            next if sol.include? k
            dep = @req[@key_pos[k]]
            # next unless dep # Enable this if your examples have less than 26 letters
            catch :missingKey do
              dep.each do |door|
                throw :missingKey unless sol.include? door.downcase
              end
              msol = sol.clone
              msol.push k
              n_p = positions.clone
              n_p[i] = k
              z = msol.sort
              z.push n_p
              msol.push n_p
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
end

starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
sol = Solution.new ARGV[0].chomp.lines
answer = sol.run
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
