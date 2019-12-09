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

    run_program(&mut mem)
}

#[derive(Debug)]
#[derive(PartialEq)]
enum Op {
    Add,
    Mul,
    Input,
    Output,
    Exit,
}

#[derive(Debug, Copy, Clone)]
#[derive(PartialEq)]
enum Mode {
    Position,
    Immediate,
}

#[derive(Debug)]
struct Operation { opcode: Op, operands: Vec<Operand> }

#[derive(Debug)]
struct Operand { mode: Mode, operand: usize }

fn run_program(mem: &mut [isize]) -> isize {
    let mut ip = 0;
    let mut last_output = 0;
    loop {
        let op = parse_op(&mem[ip..]);
//        println!("{} {:?}", ip, op);

        if op.opcode == Op::Exit {
            return last_output;
        }

        last_output = run_op(&op, mem).unwrap_or(last_output);
        ip += 1 + op.operands.len();
    }
}

fn run_op(op: &Operation, mem: &mut [isize]) -> Option<isize> {
    match op.opcode {
        Op::Add => {
            let a = get_read_operand_value(mem, &op.operands[0]);
            let b = get_read_operand_value(mem, &op.operands[1]);
            let c = get_write_operand_ref(mem, &op.operands[2]);
            *c = a + b;
        }
        Op::Mul => {
            let a = get_read_operand_value(mem, &op.operands[0]);
            let b = get_read_operand_value(mem, &op.operands[1]);
            let c = get_write_operand_ref(mem, &op.operands[2]);
            *c = a * b;
        }
        Op::Input => {
            let a = get_write_operand_ref(mem, &op.operands[0]);
            *a = 1;
        }
        Op::Output => {
            let a = get_read_operand_value(mem, &op.operands[0]);
            return Option::from(a);
        }
        Op::Exit => {}
    }
    Option::None
}

fn get_read_operand_value(mem: &[isize], operand: &Operand) -> isize {
    match operand.mode {
        Mode::Immediate => operand.operand as isize,
        Mode::Position => mem[operand.operand],
    }
}

fn get_write_operand_ref<'a>(mem: &'a mut [isize], operand: &Operand) -> &'a mut isize {
    assert_eq!(operand.mode, Mode::Position);
    &mut mem[operand.operand]
}

fn parse_op(mem_slice: &[isize]) -> Operation {
    let instr = mem_slice[0] as usize;
    let (opcode, nb_operands) = match instr % 100 {
        1 => (Op::Add, 3),
        2 => (Op::Mul, 3),
        3 => (Op::Input, 1),
        4 => (Op::Output, 1),
        99 => (Op::Exit, 0),
        n => panic!("Invalid opcode {}", n),
    };
    let modes = parse_modes(instr / 100, nb_operands);
    let operands = (0..nb_operands)
        .map(|i| Operand { operand: mem_slice[i + 1] as usize, mode: modes[i]})
        .collect();
    
    Operation { opcode, operands }
}

fn parse_modes(mut encoded_modes: usize, n: usize) -> Vec<Mode> {
    let mut modes = Vec::new();
    for _ in 0..n {
        match encoded_modes % 10 {
            0 => modes.push(Mode::Position),
            1 => modes.push(Mode::Immediate),
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
         assert_eq!(run("1002,4,3,4,33"), 0)
     }
 }
