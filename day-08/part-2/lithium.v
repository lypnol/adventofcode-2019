import os
#include <time.h> // The Vlib time library only supports second precision

fn C.clock() f64

fn get_time() f64{
	return C.clock()
}

fn run(input string) string{
	mut out := ""
	mut tmp_i := 0
	for i := 0; i < 150; i++ {
		tmp_i = i
		for (input[tmp_i] == `2`){
			tmp_i += 150
		}
		out += input[tmp_i..tmp_i+1]
	}
	return out
}

fn main() {
	start := get_time()
	answer := run(os.args[1])
	elapsed := ((get_time() - start) * 1000) / C.CLOCKS_PER_SEC
	println("_duration:$elapsed\n$answer")
}
