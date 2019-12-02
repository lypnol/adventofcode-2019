use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run_program(mem: &mut Vec<usize>) -> usize {
    let mut ip = 0;
    loop {
        let op = mem[ip];
        if op == 99 {
            break;
        }

        let (a, b, c) = (mem[ip + 1], mem[ip + 2], mem[ip + 3]);
        if op == 1 {
            mem[c] = mem[a] + mem[b];
        } else {
            mem[c] = mem[a] * mem[b];
        }
        ip += 4;
    };

    mem[0]
}

fn run(input: &str) -> i32 {
    let mut mem: Vec<usize> = input
        .split(',')
        .map(|n| n.parse().unwrap_or(0))
        .collect();

    mem[1] = 12;
    mem[2] = 02;

    run_program(&mut mem) as i32
}

// #[cfg(test)]
// mod tests {
//     use super::*;

//     #[test]
//     fn run_test() {
//         assert_eq!(run("1,1,1,4,99,5,6,0,99"), 30)
//     }
// }
