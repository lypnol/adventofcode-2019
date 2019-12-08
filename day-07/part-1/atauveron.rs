use std::env::args;
use std::time::Instant;

use std::collections::{HashSet, VecDeque};

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> isize {
    let codes: Vec<isize> = input
        .split(',')
        .map(|x: &str| x.parse::<isize>().unwrap_or(0))
        .collect();
    // Generate all possible combinations for phases
    let mut candidates: HashSet<Vec<isize>> = HashSet::with_capacity(120);
    perm(&mut [0, 1, 2, 3, 4], 0, &mut candidates);
    // Find the highest possible output
    let mut max_thrust = 0;
    for candidate in candidates {
        let thrust = chain_runs(&codes, &candidate);
        if thrust > max_thrust {
            max_thrust = thrust;
        }
    }
    max_thrust
}

fn chain_runs(codes: &[isize], candidate: &[isize]) -> isize {
    let mut codes_a = Vec::from(codes);
    let mut codes_b = Vec::from(codes);
    let mut codes_c = Vec::from(codes);
    let mut codes_d = Vec::from(codes);
    let mut codes_e = Vec::from(codes);

    let mut input_a: VecDeque<isize> = VecDeque::from(vec![candidate[0], 0]);
    let output_a = run_codes(&mut codes_a, &mut input_a);

    let mut input_b: VecDeque<isize> = VecDeque::from(vec![candidate[1], output_a]);
    let output_b = run_codes(&mut codes_b, &mut input_b);

    let mut input_c: VecDeque<isize> = VecDeque::from(vec![candidate[2], output_b]);
    let output_c = run_codes(&mut codes_c, &mut input_c);

    let mut input_d: VecDeque<isize> = VecDeque::from(vec![candidate[3], output_c]);
    let output_d = run_codes(&mut codes_d, &mut input_d);

    let mut input_e: VecDeque<isize> = VecDeque::from(vec![candidate[4], output_d]);
    run_codes(&mut codes_e, &mut input_e)
}

fn run_codes(codes: &mut [isize], input: &mut VecDeque<isize>) -> isize {
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
                codes[arg as usize] = input.pop_front().unwrap();
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

fn perm(v: &mut [isize], i: usize, acc: &mut HashSet<Vec<isize>>) {
    // From https://www.cs.utexas.edu/users/djimenez/utsa/cs3343/lecture25.html
    // Generate permutations for element i to n-1

    if i == v.len() {
        acc.insert(Vec::from(v));
    } else {
        for j in i..v.len() {
            swap(v, i, j);
            perm(v, i + 1, acc);
            swap(v, i, j);
        }
    }
}

fn swap(v: &mut [isize], i: usize, j: usize) {
    let t = v[i];
    v[i] = v[j];
    v[j] = t;
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
    fn run_test_chain() {
        let candidate = [4, 3, 2, 1, 0];
        let codes = [
            3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0,
        ];
        assert_eq!(chain_runs(&codes, &candidate), 43210)
    }

    #[test]
    fn run_test() {
        assert_eq!(run("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"), 43210)
    }

    #[test]
    fn run_test_2() {
        assert_eq!(
            run("3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"),
            54321
        )
    }

    #[test]
    fn run_test_3() {
        assert_eq!(
            run("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"),
            65210
        )
    }
}
