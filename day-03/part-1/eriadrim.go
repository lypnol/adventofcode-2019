package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"sort"
	"strconv"
	"strings"
	"time"
)

type direction struct {
	min int
	max int
	pos int
}

type directions []direction

func (v directions) Len() int           { return len(v) }
func (v directions) Swap(i, j int)      { v[i], v[j] = v[j], v[i] }
func (v directions) Less(i, j int) bool { return abs(v[i].pos) < abs(v[j].pos) }

func getDirections(rawInstructions []string) ([]direction, []direction) {
	verticalDirections := make([]direction, len(rawInstructions)/2 + 1)
	horizontalDirections := make([]direction, len(rawInstructions)/2 + 1)

	x := 0
	y := 0
	for _, s := range rawInstructions {
		value, _ := strconv.Atoi(s[1:])
		if strings.HasPrefix(s, "U") {
			verticalDirections = append(verticalDirections, direction{
				min: y,
				max: y + value,
				pos: x,
			})
			y += value
			continue
		}
		if strings.HasPrefix(s, "L") {
			horizontalDirections = append(horizontalDirections, direction{
				min: x - value,
				max: x,
				pos: y,
			})
			x -= value
			continue
		}
		if strings.HasPrefix(s, "D") {
			verticalDirections = append(verticalDirections, direction{
				min: y - value,
				max: y,
				pos: x,
			})
			y -= value
			continue
		}
		if strings.HasPrefix(s, "R") {
			horizontalDirections = append(horizontalDirections, direction{
				min: x,
				max: x + value,
				pos: y,
			})
			x += value
			continue
		}
	}

	return verticalDirections, horizontalDirections
}

func abs(a int) int {
	if a > 0 {
		return a
	}
	return -a
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func getMinDist(vert directions, hor directions) int {
	sort.Sort(vert)
	sort.Sort(hor)

	dMin := -1
	for _, lineV := range vert {
		if dMin != -1 && dMin < abs(lineV.pos) {
			return dMin
		}
		limit := max(abs(lineV.min), abs(lineV.max))
		for _, lineH := range hor {
			if (dMin != -1 && dMin < abs(lineV.pos) + abs(lineH.pos)) || limit < abs(lineH.pos) {
				break
			}
			if lineH.min > lineV.pos || lineH.max < lineV.pos || lineV.min > lineH.pos || lineV.max < lineH.pos {
				continue
			}

			d := abs(lineH.pos) + abs(lineV.pos)

			if d > 0 && (dMin == -1 || d < dMin) {
				dMin = d
			}
			break
		}
	}

	return dMin
}

func run(s string) interface{} {
	lines := strings.Split(s, "\n")
	rawInstructions1 := strings.Split(lines[0], ",")
	rawInstructions2 := strings.Split(lines[1], ",")

	vertDir1, horDir1 := getDirections(rawInstructions1)
	vertDir2, horDir2 := getDirections(rawInstructions2)

	d1 := getMinDist(vertDir1, horDir2)
	d2 := getMinDist(vertDir2, horDir1)

	if d1 < d2 {
		return d1
	}
	return d2
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
