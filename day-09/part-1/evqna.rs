use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> isize {
    let mut mem: Vec<isize> = input
        .split(',')
        .map(|n| n.parse().unwrap())
        .collect();
    mem.resize(10_000, 0);

    let mut computer = Computer::new(&mut mem);
    computer.run()
}

#[derive(Debug)]
#[derive(PartialEq)]
enum Op {
    Add,
    Mul,
    Input,
    Output,
    JumpTrue,
    JumpFalse,
    Leq,
    Eq,
    AdjustBase,
    Exit,
}

#[derive(Debug, Copy, Clone)]
#[derive(PartialEq)]
enum Mode {
    Position,
    Immediate,
    Relative,
}

#[derive(Debug)]
struct Operation { opcode: Op, operands: Vec<Operand> }

#[derive(Debug)]
struct Operand { mode: Mode, operand: isize }

struct Computer<'a> {
    ip: usize,
    relative_base: isize,
    mem: &'a mut [isize],
    outputs: Vec<isize>,
}

const INPUT: isize = 1;

impl Computer<'_> {
    fn new(mem: &mut [isize]) -> Computer {
        Computer {
            ip: 0, relative_base: 0,
            mem, outputs: Vec::new(),
        }
    }

    fn run(&mut self) -> isize {
        self.ip = 0;
        loop {
            let op = parse_op(&self.mem[self.ip..]);
//            println!("{:?}", op);
            if op.opcode == Op::Exit {
                break;
            }

            let last_ip = self.ip;
            self.run_op(&op);
            if self.ip == last_ip {
                self.ip += op.operands.len() + 1;
            }
        }
        *self.outputs.last().unwrap()
    }

    fn run_op(&mut self, op: &Operation) {
        match op.opcode {
            Op::Add => {
                let (a, b, c) = self.resolve_binary_operands(&op.operands);
                *c = a + b;
            }
            Op::Mul => {
                let (a, b, c) = self.resolve_binary_operands(&op.operands);
                *c = a * b;
            }
            Op::Input => {
                let a = self.get_write_operand_ref(&op.operands[0]);
                *a = INPUT;
            }
            Op::Output => {
                let a = self.get_read_operand_value(&op.operands[0]);
//                println!("{}", a);
                self.outputs.push(a);
            }
            Op::JumpTrue => {
                let a = self.get_read_operand_value(&op.operands[0]);
                let b = self.get_read_operand_value(&op.operands[1]);
                if a != 0 {
                    self.ip = b as usize;
                }
            }
            Op::JumpFalse => {
                let a = self.get_read_operand_value(&op.operands[0]);
                let b = self.get_read_operand_value(&op.operands[1]);
                if a == 0 {
                    self.ip = b as usize;
                }
            }
            Op::Leq => {
                let (a, b, c) = self.resolve_binary_operands(&op.operands);
                *c = if a < b { 1 } else { 0 };
            }
            Op::Eq => {
                let (a, b, c) = self.resolve_binary_operands(&op.operands);
                *c = if a == b { 1 } else { 0 };
            }
            Op::AdjustBase => {
                let a = self.get_read_operand_value(&op.operands[0]);
                self.relative_base += a;
            }
            Op::Exit => {}
        }
    }

    fn get_read_operand_value(&self, operand: &Operand) -> isize {
        match operand.mode {
            Mode::Immediate => operand.operand as isize,
            Mode::Position => self.mem[operand.operand as usize],
            Mode::Relative => self.mem[(operand.operand + self.relative_base) as usize],
        }
    }

    fn get_write_operand_ref(&mut self, operand: &Operand) -> &mut isize {
        match operand.mode {
            Mode::Position => &mut self.mem[operand.operand as usize],
            Mode::Relative => &mut self.mem[(operand.operand + self.relative_base) as usize],
            _ => panic!("Invalid operand write mode"),
        }
    }

    fn resolve_binary_operands(&mut self, operands: &[Operand]) -> (isize, isize, &mut isize) {
        let a = self.get_read_operand_value(&operands[0]);
        let b = self.get_read_operand_value(&operands[1]);
        let c = self.get_write_operand_ref(&operands[2]);
        (a, b, c)
    }
}

fn parse_op(mem_slice: &[isize]) -> Operation {
    let instr = mem_slice[0] as usize;
    let (opcode, nb_operands) = match instr % 100 {
        1 => (Op::Add, 3),
        2 => (Op::Mul, 3),
        3 => (Op::Input, 1),
        4 => (Op::Output, 1),
        5 => (Op::JumpTrue, 2),
        6 => (Op::JumpFalse, 2),
        7 => (Op::Leq, 3),
        8 => (Op::Eq, 3),
        9 => (Op::AdjustBase, 1),
        99 => (Op::Exit, 0),
        n => panic!("Invalid opcode {}", n),
    };
    let modes = parse_modes(instr / 100, nb_operands);
    let operands = (0..nb_operands)
        .map(|i| Operand { operand: mem_slice[i + 1], mode: modes[i]})
        .collect();

    Operation { opcode, operands }
}

fn parse_modes(mut encoded_modes: usize, n: usize) -> Vec<Mode> {
    let mut modes = Vec::new();
    for _ in 0..n {
        match encoded_modes % 10 {
            0 => modes.push(Mode::Position),
            1 => modes.push(Mode::Immediate),
            2 => modes.push(Mode::Relative),
            n => panic!("Invalid operation mode {}", n),
        }
        encoded_modes /= 10;
    }
    modes
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,\
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,\
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"), 999);
        assert_eq!(run("1102,34915192,34915192,7,4,7,99,0"), 1219070632396864);
        assert_eq!(run("104,1125899906842624,99"), 1125899906842624);
        assert_eq!(run("109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"), 99);
    }
}
