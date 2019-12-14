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

  def reverse_product(product)
    return if product == 'ORE'
    return if @remains[product] < @quantities[product]
    n = @remains[product] / @quantities[product]
    @remains[product] -= n * @quantities[product]
    @ingredients_for[product].each do |k, v|
      @remains[k] += v * n
      reverse_product k
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
    ore = 10**12
    n = 0
    i = 10
    glob_rem = Hash.new(0)
    while i > 1 do
      # Make a gross calculation
      q = how_many_ore_for('FUEL', 1)
      i = ore / q
      ore -= q * i
      n += i
      # Make sure we don't recycle FUEL
      @remains['FUEL'] = 0
      # Now it's time to recycle the remaining products!
      @remains.transform_values! {|v| v * i}
      # Reverse transformations we can to get a bit more ore
      @remains.keys.each { |k| reverse_product k }
      ore += @remains['ORE']
      @remains['ORE'] = 0
      @remains.each {|k,v| glob_rem[k] += v}
      @remains = Hash.new 0
    end
    # Recycling
    @remains = glob_rem
    @remains['ORE'] = ore
    @remains['FUEL'] = 0
    @remains.keys.each { |k| reverse_product k }
    while how_many_ore_for('FUEL', 1) == 0
      n += 1
    end
    n
  end
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
o = Day14solution.new
answer = o.run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"