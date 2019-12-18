import os
#include <time.h> // The Vlib time library only supports second precision

fn C.clock() f64

fn get_time() f64{
	return C.clock()
}

fn run(input string) int{
	//25 pixels wide and 6 pixels tall --> 150 chars
	layer_length := 150
	mut layer_idx := 0
	mut current_idx := 0
	mut zero_counts := []int
	mut one_counts := []int
	mut two_counts := []int
	mut current_zero_count := 0
	mut current_one_count := 0
	mut current_two_count := 0


	for c in input{
		if c == `0`{
			current_zero_count ++
		}
		else if c == `1` {
			current_one_count ++
		}
		else if c == `2` {
			current_two_count ++
		}
		current_idx ++
		if current_idx == layer_length{
			zero_counts << current_zero_count
			one_counts << current_one_count
			two_counts << current_two_count
			layer_idx ++
			current_idx = 0
			current_zero_count = 0
			current_one_count = 0
			current_two_count = 0
		}
	}
	current_zero_count = 151
	layer_idx = -1
	for i, count in zero_counts{
		if count < current_zero_count{
			current_zero_count = count
			layer_idx = i
		}
	}
	return one_counts[layer_idx] * two_counts[layer_idx]
}

fn main() {
	start := get_time()
	answer := run(os.args[1])
	elapsed := ((get_time() - start) * 1000) / C.CLOCKS_PER_SEC
	println("_duration:$elapsed\n$answer")
}
