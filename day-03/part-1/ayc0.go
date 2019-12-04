package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

type posT struct {
	x int
	y int
}

func getNextPoint(origin posT, offset int, direction byte) posT {
	switch direction {
	case 'L':
		origin.x -= offset
	case 'R':
		origin.x += offset
	case 'U':
		origin.y += offset
	case 'D':
		origin.y -= offset
	}
	return origin
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func run(s string) interface{} {
	manhattan := map[posT]int{}
	var distance int
	var x posT
	for i, line := range strings.Split(s, "\n") {
		x = posT{0, 0}

		for _, mov := range strings.Split(line, ",") {
			distance, _ = strconv.Atoi(mov[1:])
			for j := 1; j < distance; j++ {
				manhattan[getNextPoint(x, j, mov[0])] += i + 1
			}
			x = getNextPoint(x, distance, mov[0])
		}
	}

	min := 10000000
	var cur int
	manhattan[posT{0, 0}] = 0
	for pos, value := range manhattan {
		if value == 3 {
			cur = abs(pos.x) + abs(pos.y)
			if cur < min {
				min = cur
			}
		}
	}
	return min
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
