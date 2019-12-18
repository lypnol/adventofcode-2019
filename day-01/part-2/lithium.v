import os
#include <time.h> // The Vlib time library only supports second precision

fn C.clock() f64

fn get_time() f64{
	return C.clock()
}

fn run(input string) int{
	split := input.split("\n")
    mut counter := 0
    mut fuel := 0

	for i := 0; i < split.len; i++ {
		fuel = (split[i].int() / 3) - 2
		for fuel > 0{
			counter += fuel
			fuel = (fuel / 3) - 2
		}
	}
	return counter
}

fn main() {
	start := get_time()
	answer := run(os.args[1])
	elapsed := ((get_time() - start) * 1000) / C.CLOCKS_PER_SEC
	println("_duration:$elapsed\n$answer")
}
