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
    perm(&mut [5, 6, 7, 8, 9], 0, &mut candidates);
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

    let mut index_a = 0;
    let mut input_a: VecDeque<isize> = VecDeque::from(vec![candidate[0], 0]);

    let mut index_b = 0;
    let mut input_b: VecDeque<isize> = VecDeque::from(vec![candidate[1]]);

    let mut index_c = 0;
    let mut input_c: VecDeque<isize> = VecDeque::from(vec![candidate[2]]);

    let mut index_d = 0;
    let mut input_d: VecDeque<isize> = VecDeque::from(vec![candidate[3]]);

    let mut index_e = 0;
    let mut input_e: VecDeque<isize> = VecDeque::from(vec![candidate[4]]);

    loop {
        let _status_a = run_codes(&mut codes_a, &mut index_a, &mut input_a, &mut input_b);

        let _status_b = run_codes(&mut codes_b, &mut index_b, &mut input_b, &mut input_c);

        let _status_c = run_codes(&mut codes_c, &mut index_c, &mut input_c, &mut input_d);

        let _status_d = run_codes(&mut codes_d, &mut index_d, &mut input_d, &mut input_e);

        let status_e = run_codes(&mut codes_e, &mut index_e, &mut input_e, &mut input_a);
        if status_e == 0 {
            break;
        }
    }
    input_a.pop_front().unwrap()
}

fn run_codes(
    codes: &mut [isize],
    index: &mut usize,
    input: &mut VecDeque<isize>,
    output: &mut VecDeque<isize>,
) -> isize {
    loop {
        let op = OpCode::from(codes[*index]);
        match op.code {
            1 => {
                // Add
                let left = codes[*index + 1];
                let lhs = if op.modes.get(0).unwrap_or(&0) == &1 {
                    left
                } else {
                    codes[left as usize]
                };
                let right = codes[*index + 2];
                let rhs = if op.modes.get(1).unwrap_or(&0) == &1 {
                    right
                } else {
                    codes[right as usize]
                };
                let res = codes[*index + 3];
                codes[res as usize] = lhs + rhs;
                *index += 4;
            }
            2 => {
                // Multiply
                let left = codes[*index + 1];
                let lhs = if op.modes.get(0).unwrap_or(&0) == &1 {
                    left
                } else {
                    codes[left as usize]
                };
                let right = codes[*index + 2];
                let rhs = if op.modes.get(1).unwrap_or(&0) == &1 {
                    right
                } else {
                    codes[right as usize]
                };
                let res = codes[*index + 3];
                codes[res as usize] = lhs * rhs;
                *index += 4;
            }
            3 => {
                // Write input
                let arg = codes[*index + 1];
                codes[arg as usize] = match input.pop_front() {
                    None => return 1,
                    Some(value) => value,
                };
                *index += 2;
            }
            4 => {
                // Write output
                let arg = codes[*index + 1];
                output.push_back(if op.modes.get(0).unwrap_or(&0) == &1 {
                    arg
                } else {
                    codes[arg as usize]
                });
                *index += 2;
            }
            5 => {
                // Jump if true
                let arg = codes[*index + 1];
                let decide = if op.modes.get(0).unwrap_or(&0) == &1 {
                    arg
                } else {
                    codes[arg as usize]
                };
                if decide != 0 {
                    let target = codes[*index + 2];
                    *index = if op.modes.get(1).unwrap_or(&0) == &1 {
                        target as usize
                    } else {
                        codes[target as usize] as usize
                    };
                } else {
                    *index += 3;
                }
            }
            6 => {
                // Jump if false
                let arg = codes[*index + 1];
                let decide = if op.modes.get(0).unwrap_or(&0) == &1 {
                    arg
                } else {
                    codes[arg as usize]
                };
                if decide == 0 {
                    let target = codes[*index + 2];
                    *index = if op.modes.get(1).unwrap_or(&0) == &1 {
                        target as usize
                    } else {
                        codes[target as usize] as usize
                    };
                } else {
                    *index += 3;
                }
            }
            7 => {
                // Less than
                let left = codes[*index + 1];
                let lhs = if op.modes.get(0).unwrap_or(&0) == &1 {
                    left
                } else {
                    codes[left as usize]
                };
                let right = codes[*index + 2];
                let rhs = if op.modes.get(1).unwrap_or(&0) == &1 {
                    right
                } else {
                    codes[right as usize]
                };
                let res = codes[*index + 3];
                codes[res as usize] = if lhs < rhs { 1 } else { 0 };
                *index += 4;
            }
            8 => {
                // Equals
                let left = codes[*index + 1];
                let lhs = if op.modes.get(0).unwrap_or(&0) == &1 {
                    left
                } else {
                    codes[left as usize]
                };
                let right = codes[*index + 2];
                let rhs = if op.modes.get(1).unwrap_or(&0) == &1 {
                    right
                } else {
                    codes[right as usize]
                };
                let res = codes[*index + 3];
                codes[res as usize] = if lhs == rhs { 1 } else { 0 };
                *index += 4;
            }
            99 => return 0,
            _ => panic!("Unknown op code {} at index {}", codes[*index], index),
        }
    }
    // We should never reach this part
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
    fn run_test_chain_1() {
        let codes = [
            3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1,
            28, 1005, 28, 6, 99, 0, 0, 5,
        ];
        let candidate = [9, 8, 7, 6, 5];
        assert_eq!(chain_runs(&codes, &candidate), 139629729)
    }

    #[test]
    fn run_test_chain_2() {
        let codes = [
            3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54,
            -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4,
            53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10,
        ];
        let candidate = [9, 7, 8, 5, 6];
        assert_eq!(chain_runs(&codes, &candidate), 18216)
    }
    #[test]
    fn run_test_1() {
        let input =
            "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5";
        assert_eq!(run(input), 139629729);
    }

    #[test]
    fn run_test_2() {
        let input = "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10";
        assert_eq!(run(input), 18216);
    }
}
