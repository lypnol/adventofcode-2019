package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

func run(s string) interface{} {
	programIni := make([]int, (len(s)-1)/2)
	for i, line := range strings.Split(s, ",") {
		val, _ := strconv.Atoi(line)
		programIni[i] = val
	}

	program := make([]int, (len(s)-1)/2)
	for noun := 0; noun < 100; noun++ {
		for verb := 0; verb < 100; verb++ {
			copy(program, programIni)
			program[1] = noun
			program[2] = verb
			if execute(program) == 19690720 {
				return 100*noun + verb
			}
		}
	}

	return 0
}

func execute(program []int) int {
	i := 0
	for i < len(program) {
		if program[i] == 99 {
			return program[0]
		}

		if i+3 >= len(program){
			return 0
		}
		if program[i+1] < 0 || program[i+1] >= len(program) {
			return 0
		}
		if program[i+2] < 0 || program[i+2] >= len(program) {
			return 0
		}
		if program[i+3] < 0 || program[i+3] >= len(program) {
			return 0
		}
		switch program[i] {
		case 1:
			program[program[i+3]] = program[program[i+1]] + program[program[i+2]]
		case 2:
			program[program[i+3]] = program[program[i+1]] * program[program[i+2]]
		default:
			return 0
		}

		i += 4
	}

	return 0
}

func main() {
	// Uncomment this line to disable garbage collection
	// debug.SetGCPercent(-1)

	// Read input from stdin
	input, err := ioutil.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}

	// Start resolution
	start := time.Now()
	result := run(string(input))

	// Print result
	fmt.Printf("_duration:%f\n", time.Now().Sub(start).Seconds()*1000)
	fmt.Println(result)
}
