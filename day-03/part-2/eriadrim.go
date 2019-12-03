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

const (

)

type direction struct {
	min int
	max int
	pos int
	steps int
	inv bool
}

type verticalDirections []direction

func (v verticalDirections) Len() int           { return len(v) }
func (v verticalDirections) Swap(i, j int)      { v[i], v[j] = v[j], v[i] }
func (v verticalDirections) Less(i, j int) bool { return v[i].pos < v[j].pos }

type horizontalDirections []direction

func (v horizontalDirections) Len() int           { return len(v) }
func (v horizontalDirections) Swap(i, j int)      { v[i], v[j] = v[j], v[i] }
func (v horizontalDirections) Less(i, j int) bool { return v[i].min < v[j].min }

func getDirections(rawInstructions []string) ([]direction, []direction) {
	verticalDirections := make([]direction, len(rawInstructions)/2 + 1)
	horizontalDirections := make([]direction, len(rawInstructions)/2 + 1)

	x := 0
	y := 0
	steps := 0
	for _, s := range rawInstructions {
		value, _ := strconv.Atoi(s[1:])
		if strings.HasPrefix(s, "U") {
			verticalDirections = append(verticalDirections, direction{
				min: y,
				max: y + value,
				pos: x,
				steps : steps,
				inv: false,
			})
			y += value
		} else if strings.HasPrefix(s, "L") {
			horizontalDirections = append(horizontalDirections, direction{
				min: x - value,
				max: x,
				pos: y,
				steps : steps,
				inv: true,
			})
			x -= value
		} else if strings.HasPrefix(s, "D") {
			verticalDirections = append(verticalDirections, direction{
				min: y - value,
				max: y,
				pos: x,
				steps : steps,
				inv: true,
			})
			y -= value
		} else if strings.HasPrefix(s, "R") {
			horizontalDirections = append(horizontalDirections, direction{
				min: x,
				max: x + value,
				pos: y,
				steps : steps,
				inv: false,
			})
			x += value
		}
		steps += value
	}

	return verticalDirections, horizontalDirections
}

func getMinDist(vert verticalDirections, hor horizontalDirections) int {
	sort.Sort(vert)
	sort.Sort(hor)

	dMin := -1
	for _, lineV := range vert {
		for _, lineH := range hor {
			if lineH.min > lineV.pos {
				break
			}
			if lineH.max < lineV.pos || lineV.min > lineH.pos || lineV.max < lineH.pos {
				continue
			}

			d := lineH.steps + lineV.steps
			if lineH.inv {
				d += lineH.max - lineV.pos
			} else {
				d += lineV.pos - lineH.min
			}

			if lineV.inv {
				d += lineV.max - lineH.pos
			} else {
				d += lineH.pos - lineV.min
			}

			if d > 0 && (dMin == -1 || d < dMin) {
				dMin = d
			}
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
