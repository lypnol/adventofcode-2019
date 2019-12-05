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
    let mut codes: Vec<isize> = input
        .split(',')
        .map(|x: &str| x.parse::<isize>().unwrap_or(0))
        .collect();
    run_codes(&mut codes, 1)
}

fn run_codes(codes: &mut [isize], input: isize) -> isize {
    let mut output: isize = 0;
    let mut index: usize = 0;
    loop {
        let op = OpCode::from(codes[index]);
        match op.code {
            1 => {
                // Add
                let left = codes[index + 1];
                let lhs = if op.modes.get(0).unwrap_or(&0) == &1 {
                    left
                } else {
                    codes[left as usize]
                };
                let right = codes[index + 2];
                let rhs = if op.modes.get(1).unwrap_or(&0) == &1 {
                    right
                } else {
                    codes[right as usize]
                };
                let res = codes[index + 3];
                codes[res as usize] = lhs + rhs;
                index += 4;
            }
            2 => {
                // Multiply
                let left = codes[index + 1];
                let lhs = if op.modes.get(0).unwrap_or(&0) == &1 {
                    left
                } else {
                    codes[left as usize]
                };
                let right = codes[index + 2];
                let rhs = if op.modes.get(1).unwrap_or(&0) == &1 {
                    right
                } else {
                    codes[right as usize]
                };
                let res = codes[index + 3];
                codes[res as usize] = lhs * rhs;
                index += 4;
            }
            3 => {
                // Write input
                let arg = codes[index + 1];
                codes[arg as usize] = input;
                index += 2;
            }
            4 => {
                // Read output
                let arg = codes[index + 1];
                output = if op.modes.get(0).unwrap_or(&0) == &1 {
                    arg
                } else {
                    codes[arg as usize]
                };
                index += 2;
            }
            99 => break,
            _ => panic!("Unknown op code {} at index {}", codes[index], index),
        }
    }
    output
}

#[derive(Debug)]
struct OpCode {
    code: isize,
    modes: Vec<isize>,
}

impl OpCode {
    fn from(value: isize) -> OpCode {
        if value < 100 {
            OpCode {
                code: value,
                modes: Vec::new(),
            }
        } else {
            let tmp = value.to_string();
            let mut digits = tmp
                .chars()
                .rev()
                .map(|x: char| x.to_digit(10).unwrap_or(0) as isize);
            digits.nth(1);
            OpCode {
                code: value % 100,
                modes: { digits.collect() },
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("3,0,4,0,99"), 1)
    }

    #[test]
    fn run_test_neg() {
        assert_eq!(run("1101,100,-1,4,0"), 0)
    }

    #[test]
    fn run_test_ret() {
        assert_eq!(run("1002,4,3,4,33"), 0)
    }
}
