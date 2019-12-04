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
	rawCodes := strings.Split(s, ",")
	codes := make([]int, len(rawCodes))
	for i, rawCode := range rawCodes {
		val, _ := strconv.Atoi(rawCode)
		codes[i] = val
	}

	codes[1] = 12
	codes[2] = 2

	for i := 0; i < len(codes)/4; i++ {
		opcode := codes[i*4]
		loc1 := codes[i*4+1]
		loc2 := codes[i*4+2]
		loc3 := codes[i*4+3]
		switch opcode {
		case 1:
			codes[loc3] = codes[loc1] + codes[loc2]
		case 2:
			codes[loc3] = codes[loc1] * codes[loc2]
		case 99:
			break
		}
	}
	return codes[0]
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
