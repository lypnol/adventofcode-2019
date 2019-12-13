package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

type moon struct {
	x, y, z, vx, vy, vz int
}

func abs(a int) int {
	if a < 0 {
		return a
	}
	return -a
}

func (m moon) energy() int {
	return (abs(m.x) + abs(m.y) + abs(m.z)) * (abs(m.vx) + abs(m.vy) + abs(m.vz))
}

func parseMoons(s string) []*moon {
	res := []*moon{}

	for _, line := range strings.Split(s, "\n") {
		m := &moon{}
		fields := strings.Split(line, ", ")
		m.x, _ = strconv.Atoi(strings.Split(fields[0], "=")[1])
		m.y, _ = strconv.Atoi(strings.Split(fields[1], "=")[1])
		m.z, _ = strconv.Atoi(strings.Trim(strings.Split(fields[2], "=")[1], ">"))

		res = append(res, m)
	}

	return res
}

func cmp(a, b int) int {
	if a > b {
		return 1
	} else if a < b {
		return -1
	} else {
		return 0
	}
}

func applyGravity(moons []*moon) {
	for i, m := range moons {
		for j, m2 := range moons {
			if i == j {
				continue
			}

			m.vx += cmp(m2.x, m.x)
			m.vy += cmp(m2.y, m.y)
			m.vz += cmp(m2.z, m.z)
		}
	}
}

func move(moons []*moon) {
	for _, m := range moons {
		m.x += m.vx
		m.y += m.vy
		m.z += m.vz
	}
}

func step(moons []*moon) {
	applyGravity(moons)
	move(moons)
}

func run(s string) interface{} {
	// Your code goes here
	moons := parseMoons(s)

	for i := 0; i < 1000; i++ {
		step(moons)
	}

	total := 0
	for _, m := range moons {
		total += m.energy()
	}

	return total
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
