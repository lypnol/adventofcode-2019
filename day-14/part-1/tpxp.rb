class Day14solution
  def how_many_ore_for(product, how_many)
    if @remains[product] >= how_many
      @remains[product] -= how_many
      return 0
    end
    return how_many if product == 'ORE'
    n_reacts = ((how_many - @remains[product]).to_f / @quantities[product]).ceil
    @remains[product] += n_reacts * @quantities[product] - how_many
    @ingredients_for[product].reduce(0) do |acc, kv|
      n,q = kv
      acc + how_many_ore_for(n, q * n_reacts)
    end
  end

  def run(s)
    @remains = Hash.new(0)
    @ingredients_for = Hash.new {|h,k| h[k] = Hash.new 0}
    @quantities = Hash.new 1
    s.each do |formula|
      ingredients, target = formula.split ' => '
      quantity, target = target.split
      @quantities[target] = quantity.to_i
      ingredients.split(', ').each do |ingredient|
        q,n = ingredient.split
        @ingredients_for[target][n] = q.to_i
      end
    end
    how_many_ore_for('FUEL', 1)
  end
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
o = Day14solution.new
answer = o.run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
