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

type step struct {
	i        int
	distance int
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
	manhattan := map[posT]step{}
	var distance int
	var totDistance int
	var x posT
	for i, line := range strings.Split(s, "\n") {
		x = posT{0, 0}
		totDistance = 0
		for _, mov := range strings.Split(line, ",") {
			distance, _ = strconv.Atoi(mov[1:])
			for j := 1; j < distance; j++ {
				p, ok := manhattan[getNextPoint(x, j, mov[0])]
				if !ok {
					manhattan[getNextPoint(x, j, mov[0])] = step{i + 1, totDistance + j}
				} else {
					manhattan[getNextPoint(x, j, mov[0])] = step{p.i + i + 1, p.distance + totDistance + j}
				}
			}
			totDistance += distance
			x = getNextPoint(x, distance, mov[0])
		}
	}

	min := 10000000000
	var cur int
	manhattan[posT{0, 0}] = step{0, 0}
	for _, value := range manhattan {
		if value.i == 3 {
			cur = value.distance
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
