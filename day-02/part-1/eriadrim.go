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

	program := make([]int, (len(s)-1)/2)
	for i, line := range strings.Split(s, ",") {
		val, _ := strconv.Atoi(line)
		program[i] = val
	}

	program[1] = 12
	program[2] = 2

	return execute(program)
}

func execute(program []int) int {
	i := 0
	for i < len(program) {
		switch program[i] {
		case 1:
			program[program[i+3]] = program[program[i+1]] + program[program[i+2]]
		case 2:
			program[program[i+3]] = program[program[i+1]] * program[program[i+2]]
		case 99:
			break
		}

		i += 4
	}

	return program[0]
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
