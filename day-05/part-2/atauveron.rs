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
    run_codes(&mut codes, 5)
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
            5 => {
                // Jump if true
                let arg = codes[index + 1];
                let decide = if op.modes.get(0).unwrap_or(&0) == &1 {
                    arg
                } else {
                    codes[arg as usize]
                };
                if decide != 0 {
                    let target = codes[index + 2];
                    index = if op.modes.get(1).unwrap_or(&0) == &1 {
                        target as usize
                    } else {
                        codes[target as usize] as usize
                    };
                } else {
                    index += 3;
                }
            }
            6 => {
                // Jump if false
                let arg = codes[index + 1];
                let decide = if op.modes.get(0).unwrap_or(&0) == &1 {
                    arg
                } else {
                    codes[arg as usize]
                };
                if decide == 0 {
                    let target = codes[index + 2];
                    index = if op.modes.get(1).unwrap_or(&0) == &1 {
                        target as usize
                    } else {
                        codes[target as usize] as usize
                    };
                } else {
                    index += 3;
                }
            }
            7 => {
                // Less than
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
                codes[res as usize] = if lhs < rhs { 1 } else { 0 };
                index += 4;
            }
            8 => {
                // Equals
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
                codes[res as usize] = if lhs == rhs { 1 } else { 0 };
                index += 4;
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
    fn run_test_equal() {
        let mut codes = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8];
        assert_eq!(run_codes(&mut codes, 1), 0);
        assert_eq!(run_codes(&mut codes, 8), 1);
    }

    #[test]
    fn run_test_less_than() {
        let mut codes = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8];
        assert_eq!(run_codes(&mut codes, 1), 1);
        assert_eq!(run_codes(&mut codes, 8), 0);
        assert_eq!(run_codes(&mut codes, 10), 0);
    }

    #[test]
    fn run_test_long() {
        let mut codes = [
            3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0,
            0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4,
            20, 1105, 1, 46, 98, 99,
        ];
        assert_eq!(run_codes(&mut codes, 5), 999);
        assert_eq!(run_codes(&mut codes, 8), 1000);
        assert_eq!(run_codes(&mut codes, 15), 1001);
    }
}
