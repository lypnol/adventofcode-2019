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

func calcKOver(memG memo, b string) int {
	num, _ := strconv.Atoi(b)

	res := 0
	// case aaaXYZ
	{
		c1 := atoi(b[0])
		if c1 * 111111 < num {
			c1++
		}
		for k := c1; k < 10; k++ {
			res += calcG(memG, k, 1) + calcG(memG, k+1, 1) + calcG(memG, k+1, 2) + calcG(memG, k+1, 3)
		}
	}

	// case XaaaYZ
	{
		c1 := atoi(b[0])
		for k := c1 + 1; k < 10; k++ {
			if c1 * 100000 + k * 11111 < num {
				res += (k - c1 - 1) * (calcG(memG, k, 2) + 1)
			} else {
				res += (k - c1) * (calcG(memG, k, 2) + 1)
			}
		}
	}

	// case XYaaaZ
	{
		c1 := atoi(b[0])
		c2 := atoi(b[1])
		if c2 <= c1 {
			c2 = c1 + 1
		}
		threshold := c1 * 100000 + c2 * 10000
		for k := c1 + 2; k < 10; k++ {
			mult := 0
			if k > c2 {
				mult += k - c2
			}
			if k - 2 > c1 {
				mult += (k-c1-1)*(k-c1-2)/2
			}
			if mult <= 0 {
				continue
			}
			if k > c2 && threshold + k * 1111 < num {
				res += (mult - 1) * (10 - k)
			} else {
				res += mult * (10 - k)
			}
		}
	}

	// case XYZaaa
	{
		c1 := atoi(b[0])
		c2 := atoi(b[1])
		c3 := atoi(b[2])
		if c3 <= c2 {
			c3 = c2 + 1
		}
		if c2 <= c1 {
			c2 = c1 + 1
			c3 = c1 + 2
		}
		threshold := c1*100000 + c2*10000 + c3*1000
		for k := c1 + 3; k < 10; k++ {
			if 1000 * ((k-3) * 100 + (k-2) * 10 + k-1) < threshold {
				continue
			}
			mult := 0
			if k > c3 {
				mult += k-c3
			}
			if k - 2 > c2 {
				mult += (k-c2-1)*(k-c2-2)/2
			}
			for j := c1+1; j < k-2; j++{
				mult += (k-j-2)*(k-j-1)/2
			}
			if mult <= 0 {
				continue
			}
			if k > c3 && threshold+k*111 < num {
				res += mult - 1
			} else {
				res += mult
			}
		}
	}

	return res
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

func calcGOver(memG memo, b string, max int) int {
	b = findFirstG(b, max)
	if b == "" {
		return 0
	}

	res := 1
	for i := 0; i < max; i++ {
		res += calcG(memG, atoi(b[i])+1, max-i)
	}

	return res
}

func findFirstG(b string, max int) string {
	if atoi(b[0]) > (10-max) {
		return ""
	}
	i := 1
	for i < max {
		if atoi(b[i]) - i > (10-max) {
			break
		}
		if b[i-1] >= b[i] {
			break
		}
		i ++
	}
	if i == max {
		return b
	}
	res := ""
	if atoi(b[i]) - i > (10-max) {
		j := i - 1
		for j >= 0 {
			if atoi(b[j]) - j <= (9-max) {
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
	for j := i; j < max; j++ {
		a++
		res += strconv.Itoa(a)
	}
	return res
}

func calcHOver(memF, memG memo, b string) int {
	return calcFOver(memF, b) - calcGOver(memG, b, 6) - calcKOver(memG, b)
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
