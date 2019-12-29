def run(s)
  deck = (0..10006).to_a
  length = deck.length
  s.each do |order|
    throw :badOp if deck.length != length
    order = order.chomp
    if order == "deal into new stack"
      deck.reverse!
      next
    elsif order.start_with? "cut "
      n = order[4..].to_i
      if n < 0
        deck = deck[n..] + deck[0...length + n]
      else
        deck = deck[n..] + deck[0...n]
      end
    elsif order.start_with? "deal with increment "
      n = order[19..].to_i
      ndeck = Array.new length
      throw :badIncrement if length % n == 0
      (0..length).each do |i|
        ndeck[(i*n) % length] = deck[i]
      end
      deck = ndeck
    else
      throw :unknownOp
    end
  end
  # puts deck.inspect
  deck.index 2019
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].chomp.lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
