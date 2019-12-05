package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
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

func calcFOver(memF memo, b string) int {
	b = findFirstF(b)

	res := 1
	for i := 0; i < 6; i++ {
		res += calcF(memF, atoi(b[i])+1, 6-i)
	}
	return res
}

func findFirstF(b string) string {
	i := 1
	for i < 6 {
		if b[i-1] >= b[i] {
			break
		}
		i ++
	}
	if i == 6 {
		return b
	}
	res := b[:i]
	c := strconv.Itoa(atoi(b[i-1]))
	for j := i; j < 6; j++ {
		res += c
	}
	return res
}

func calcGOver(memG memo, b string) int {
	b = findFirstG(b)
	if b == "" {
		return 0
	}

	res := 1
	for i := 0; i < 6; i++ {
		res += calcG(memG, atoi(b[i])+1, 6-i)
	}

	return res
}

func findFirstG(b string) string {
	if atoi(b[0]) > 4 {
		return ""
	}
	i := 1
	for i < 6 {
		if atoi(b[i]) - i > 4 {
			break
		}
		if b[i-1] >= b[i] {
			break
		}
		i ++
	}
	if i == 6 {
		return b
	}
	res := ""
	if atoi(b[i]) - i > 4 {
		j := i - 1
		for j >= 0 {
			if atoi(b[j]) - j <= 3 {
				i = j
				break
			}
			j--
		}
		if j < 0 {
			return ""
		}
		res = b[:i]
		res += strconv.Itoa(atoi(b[i]) + 1)
		i++
	} else {
		res = b[:i]
	}
	a := atoi(res[i-1])
	for j := i; j < 6; j++ {
		a++
		if a > 9 {
			return ""
		}
		res += strconv.Itoa(a)
	}
	return res
}

func calcHOver(memF, memG memo, b string) int {
	return calcFOver(memF, b) - calcGOver(memG, b)
}

func calcF(mem memo, a, n int) int {
	if a > 9 {
		return 0
	}
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
	if a > 9 {
		return 0
	}
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
