import os
#include <time.h> // The Vlib time library only supports second precision

fn C.clock() f64

fn get_time() f64{
	return C.clock()
}

fn run(input string) int{
	mut orbiting := map[string]string
	for orbit in input.split("\n"){
		orbiting[orbit[4..7]] = orbit[0..3] 
	}

	// Our total orbit count
	mut count := 0

	// If we already processed this depth, might as well cache it
	mut quick := {
		"COM": 0
	}

	for b in orbiting.keys(){
		// a)b <-- b orbits a
		mut a := orbiting[b]

		// We start at 1 because only COM is at 0
		mut curdepth := 1
		for (!(a in quick)){
			// While the parent is not in the lookup table
			a = orbiting[a]
			curdepth ++
		}
		// Finally, add the pre-computed depth
		curdepth += quick[a]
		// Cache the result
		quick[b] = curdepth
		
		// And count now, so we don't loop over all keys another time
		count += curdepth
	}
	return count
}

fn main() {
	start := get_time()
	answer := run(os.args[1])
	elapsed := ((get_time() - start) * 1000) / C.CLOCKS_PER_SEC
	println("_duration:$elapsed\n$answer")
}
