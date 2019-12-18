import os
#include <time.h> // The Vlib time library only supports second precision

fn C.clock() f64

fn get_time() f64{
	return C.clock()
}

fn run(input string) int{
	// Compute all orbits
	mut orbiting := map[string]string
	for orbit in input.split("\n"){
		orbiting[orbit[4..7]] = orbit[0..3] 
	}

	mut cur_distance := -1
	mut cur := "YOU"

	mut distance_to_you := map[string]int

	for (cur in orbiting){
		distance_to_you[cur] = cur_distance
		cur_distance ++
		cur = orbiting[cur]
	}

	cur = "SAN"
	cur_distance = -1

	for (cur in orbiting){
		if cur in distance_to_you{
			return cur_distance + distance_to_you[cur]
		}
		cur_distance ++
		cur = orbiting[cur]
	}
	
	// oops
	return -1
}

fn main() {
	start := get_time()
	answer := run(os.args[1])
	elapsed := ((get_time() - start) * 1000) / C.CLOCKS_PER_SEC
	println("_duration:$elapsed\n$answer")
}
