# Recommended read: https://codeforces.com/blog/entry/72593
def run(s)
  # Now we can't really track all cards this time, so let's just track the position of card 2020 instead
  # pos = 2020
  length = 119315717514047
  a = 1
  b = 0
  s.each do |order|
    order = order.chomp
    if order == "deal into new stack"
      a *= -1
      b *= -1
      b -= 1
    elsif order.start_with? "cut "
      n = order[4..].to_i
      b -= n
    elsif order.start_with? "deal with increment "
      n = order[19..].to_i
      a *= n
      b *= n
    else
      throw :unknownOp
    end
  end
  a %= length
  b %= length
  # At every run, a card in position u_n ends up in position u_(n+1) = a*u_n + b % length
  # This is a "suite arithmético-géométrique"
  # https://fr.wikipedia.org/wiki/Suite_arithm%C3%A9tico-g%C3%A9om%C3%A9trique
  # We want to work with u_n, so we compute a^n (z here)
  n = 101741582076661

  # Quick exponentiation but with a pinch of % length
  z = a
  zz = 1
  while n > 1
    zz *= z if (n % 2) == 1
    n /= 2
    z = (z ** 2) % length # *(1-a) - not needed anymore
  end
  z = (z * zz) % length
  # If we were to track the 2020 card, we could make computations modulo length*(1-a) so that
  # the division for r is exact
  # c = (z * (pos*(1-a) - b) + b)
  # throw :notExact if c%(1-a) != 0
  # l is not the position of card 2020
  # l = (c / (1-a)) % length
  # ... Except we actually want to know what's written on card at position 2020,
  # which means finding u_0 given u_n (a.k.a inverse the relation above)
  # This implies the use of modular inverse instead of a division (both work but we can't have an exact division here)
  (((2020 * (1-a) - b) * modular_inverse(z,length) + b)* modular_inverse(1-a, length)) % length
end

def modular_inverse(a,b)
  # Extended euclidean algorithm (thanks Wikipedia)
  r,u,v,rr,uu,vv = [a,1,0,b,0,1]
  while rr != 0
    q = r/rr
    r,u,v,rr,uu,vv = [rr, uu, vv, r-q*rr, u-q*uu, v-q*vv]
  end
  u % b
end

starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].chomp.lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
