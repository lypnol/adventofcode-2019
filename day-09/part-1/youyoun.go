package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

type Program struct {
	intCode    map[int]int
	pointer    int
	pointerRef int
	inputValue int
	outputs    []int
	end        int
}

var OpNArgsMap = map[int]int{
	1:  3,
	2:  3,
	3:  1,
	4:  1,
	5:  2,
	6:  2,
	7:  3,
	8:  3,
	9:  1,
	99: 0,
}

func parseInstruction(instr int) (int, []int) {
	op := instr % 100
	intModes := instr / 100
	modes := []int{0, 0, 0}
	for i := 0; i < 3; i++ {
		modes[i] = intModes % 10
		intModes /= 10
	}
	return op, modes
}

func (p Program) param(pos int, mode int) int {
	switch mode {
	case 0:
		return p.intCode[p.pointer+pos]
	case 1:
		return p.pointer + pos
	case 2:
		return p.pointerRef + p.intCode[p.pointer+pos]
	default:
		panic("Invalid param mode")
	}
}

func (p *Program) runInstructions() {
	instr := p.intCode[p.pointer]
	opcode, modes := parseInstruction(instr)
	switch opcode {
	case 1:
		p.intCode[p.param(3, modes[2])] = p.intCode[p.param(2, modes[1])] + p.intCode[p.param(1, modes[0])]
	case 2:
		p.intCode[p.param(3, modes[2])] = p.intCode[p.param(2, modes[1])] * p.intCode[p.param(1, modes[0])]
	case 3:
		p.intCode[p.param(1, modes[0])] = p.inputValue
	case 4:
		p.outputs = append(p.outputs, p.intCode[p.param(1, modes[0])])
	case 5:
		if p.intCode[p.param(1, modes[0])] != 0 {
			p.pointer = p.intCode[p.param(2, modes[1])]
			return
		}
	case 6:
		if p.intCode[p.param(1, modes[0])] == 0 {
			p.pointer = p.intCode[p.param(2, modes[1])]
			return
		}
	case 7:
		if p.intCode[p.param(1, modes[0])] < p.intCode[p.param(2, modes[1])] {
			p.intCode[p.param(3, modes[2])] = 1
		} else {
			p.intCode[p.param(3, modes[2])] = 0
		}
	case 8:
		if p.intCode[p.param(1, modes[0])] == p.intCode[p.param(2, modes[1])] {
			p.intCode[p.param(3, modes[2])] = 1
		} else {
			p.intCode[p.param(3, modes[2])] = 0
		}
	case 9:
		p.pointerRef += p.intCode[p.param(1, modes[0])]
	case 99:
		p.end = 1
		return
	default:
		panic("Invalid OP code")
	}
	p.pointer += OpNArgsMap[opcode] + 1
}

func run(s string) interface{} {
	intCode := make(map[int]int)
	for ind, val := range strings.Split(s, ",") {
		intCode[ind], _ = strconv.Atoi(val)
	}
	prog := Program{
		intCode:    intCode,
		inputValue: 1,
	}
	for {
		prog.runInstructions()
		if prog.end == 1 {
			break
		}
	}
	return prog.outputs[0]
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
