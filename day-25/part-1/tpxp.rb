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
    @input_value = []
  end

  def run(input_value = [])
    @input_value += input_value
    loop do
      a = @input[@i..@i+3] + [0,0,0,0]
      code = a[0] % 100
      modes = 3.times.to_a.map { |i| (a[0] / (10 ** (i+2))) % 10}

      v = 3.times.to_a.map do |i|
        r = a[i+1].to_i
        r = @input[r] if modes[i] == 0
        r = @input[@relative_base + r] if modes[i] == 2
        r.to_i
      end
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
        @input_value = gets.chars.map &:ord if @input_value.length == 0
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

Reverse_direction = {
    "north" => "south",
    "south" => "north",
    "east" => "west",
    "west" => "east"
}

class Solution
  def parse_output output
    room = nil
    mode = nil
    items = []
    doors = []
    output.lines.each do |line|
      line = line.chomp
      r = /^== ([A-Za-z ]+) ==$/.match line
      if r
        # Room is reset!
        room = r[1]
        items = []
        doors = []
        next
      end
      if line == "Doors here lead:"
        mode = :doors
        next
      end
      if line == "Items here:"
        mode = :items
        next
      end
      r = /\- ([a-z 0-9A-Z]+)/.match line
      if r
        doors.push r[1] if mode == :doors
        items.push r[1] if mode == :items
        next
      end
    end
    {
        "name" => room,
        "items" => items,
        "doors" => doors,
    }
  end

  def explore path = []
    @runner.reset
    output = @runner.run((path.join("\n") + "\n").chars.map &:ord).chr
    catch :noInput do loop do
      output += @runner.run.chr
    end end
    room = parse_output output
    return if @rooms.has_key? room['name']
    room['path'] = path
    @rooms[room['name']] = room
    doors = room['doors'].filter {|d| d != Reverse_direction[path[-1]]}
    doors.each do |d|
      @to_explore.push path + [d]
    end
  end

  def find_rooms
    @to_explore = []
    @rooms = {}
    # We don't know the direction first, let's run the game without any input
    explore
    explore @to_explore.shift until @to_explore.empty?
  end

  def determine_bad_items
    bad_items = []
    @rooms.filter { |key, value| not value['items'].empty? }.each do |name, room|
      room['items'].each do |item|
        @runner.reset
        # A "good enough" approach: see if the the room name changed after we picked our item and tried to go back
        # (a.k.a "Can we still move after picking up our item?")
        output = @runner.run((room['path'].join("\n") + "\ntake #{item}\n#{Reverse_direction[room['path'][-1]]}\n").chars.map &:ord).chr
        catch :goodItem do
          catch :haltAndCatchFire do
            catch :noInput do loop do
              output += @runner.run.chr
              throw :haltAndCatchFire if output.length > 10000
            end end
            res = parse_output output
            throw :goodItem if res['name'] != room['name']
          end
          bad_items.push item
        end
      end
    end
    bad_items
  end

  def run(source)
    @runner = IntCodeInterpreter.new source
    # ARGV.clear
    find_rooms
    bad_items = determine_bad_items
    # puts bad_items.inspect
    # Time to pick all items
    items_we_have = []
    input = ""
    @rooms.values.each do |room|
      items_to_get = room['items'] - bad_items
      next if items_to_get.empty?
      items_we_have += items_to_get
      input += room['path'].join "\n"
      input += "\n"
      input += items_to_get.map{|item| "take #{item}\n"}.join
      input += room['path'].reverse.map{|d| Reverse_direction[d] }.join "\n"
      input += "\n"
    end
    @runner.reset
    @runner.run input.chars.map &:ord
    sec_room = @rooms["Security Checkpoint"]
    throw :couldNotFindCheckpoint unless sec_room
    try_check = sec_room['doors'] - [Reverse_direction[sec_room['path'][-1]]]
    throw :unknownCheckDirection if try_check.length != 1
    try_check = try_check[0] + "\n"
    try_check = try_check.chars.map &:ord
    # Now, go to the security checkpoint
    @runner.run (sec_room['path'].join "\n").chars.map &:ord
    @runner.run [10] # That's a newline
    # Drop all items
    @runner.run items_we_have.map{|item| "drop #{item}\n"}.join.chars.map &:ord
    # Consume the output
    catch :noInput do loop do @runner.run end end
    output = ""
=begin Debug: did we get all items?
    output = @runner.run("inv\n".chars.map &:ord).chr
    catch :noInput do loop do output += @runner.run.chr end end
    puts output
=end
    # Possible optimization: check if there items that are too heavy alone
    catch :haltAndCatchFire do
      (1..items_we_have.length).each do |length|
        items_we_have.combination length do |items|
          output = @runner.run(items.map{|item| "take #{item}\n"}.join.chars.map &:ord).chr
          output += @runner.run(try_check).chr
          catch :noInput do loop do output += @runner.run.chr end end
          room = parse_output output
          # puts items.inspect
          throw :foundIt if room['name'] != sec_room['name']
          # Drop the items
          @runner.run items.map{|item| "drop #{item}\n"}.join.chars.map &:ord
          catch :noInput do loop do @runner.run end end
        end
      end
    end
    code = /typing (\d+) on the keypad/.match output
    throw :missingCode unless code
    code[1]
  end
end

starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = Solution.new
answer = answer.run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
