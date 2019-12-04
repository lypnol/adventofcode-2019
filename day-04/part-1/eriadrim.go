package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

type memo [10][7]int

func run(s string) interface{} {

	var f, g memo
	for i := 0; i < 10; i++ {
		f[i][0] = 1
		f[i][1] = 10 - i
		g[i][0] = 1
		g[i][1] = 10 - i
	}

	splits := strings.Split(s, "-")
	b1 := splits[0]
	b2 := splits[1]

	return calcHOver(f, g, b1) - calcHOver(f, g, b2)
}

func atoi(n uint8) int {
	return int(n-48)
}

func calcHOver(memF, memG memo, b string) int {

	if atoi(b[0]) == 9 {
		return 1
	}
	if b[1] < b[0] {
		return calcH(memF, memG, atoi(b[0]), 6)
	}

	res := calcH(memF, memG, atoi(b[0])+1, 6)
	var wasEqual bool
	i := 1
	for i < 6 {
		if b[i] < b[i-1] {
			break
		}
		if atoi(b[i]) == 9 {
			res++
			break
		}
		a := atoi(b[i])
		if i == 5 || b[i+1] >= b[i] {
			a++
		}
		if wasEqual {
			res += calcF(memF, a, 6-i)
		} else {
			res += calcH(memF, memG, a, 6-i)
		}
		if b[i] == b[i-1] {
			wasEqual = true
		}
		i ++
	}
	if i == 6 {
		res++
	}
	return res
}

func calcF(mem memo, a, n int) int {
	if mem[a][n] != 0 {
		return mem[a][n]
	}
	s := 0
	for k := a; k < 10; k++ {
		s += calcF(mem, k, n-1)
	}
	mem[a][n] = s
	return s
}

func calcG(mem memo, a, n int) int {
	if mem[a][n] != 0 {
		return mem[a][n]
	}
	s := 0
	for k := a+1; k < 10; k++ {
		s += calcG(mem, k, n-1)
	}
	mem[a][n] = s
	return s
}

func calcH(memF, memG memo, a, n int) int {
	return calcF(memF, a, n) - calcG(memG, a, n)
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
