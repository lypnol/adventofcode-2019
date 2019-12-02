use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!(
        "_duration:{}.{}",
        elapsed.as_secs() * 1000 + u64::from(elapsed.subsec_millis()),
        elapsed.subsec_micros() - (elapsed.subsec_millis() * 1000)
    );
    println!("{}", output);
}

fn run(input: &str) -> usize {
    let codes: Vec<usize> = input
        .split(",")
        .map(|x: &str| x.parse::<usize>().unwrap_or(0))
        .collect();
    for i in 0..100 {
        for j in 0..100 {
            let mut local_codes = codes.clone();
            local_codes[1] = i;
            local_codes[2] = j;
            let res = run_codes(&mut local_codes);
            if res == 19690720 {
                return 100 * i + j;
            }
        }
    }
    panic!("No solution found");
}

fn run_codes(codes: &mut [usize]) -> usize {
    let mut index: usize = 0;
    loop {
        match &codes[index] {
            1 => {
                let left = codes[index + 1];
                let right = codes[index + 2];
                let res = codes[index + 3];
                let lhs = codes[left];
                let rhs = codes[right];
                codes[res] = lhs + rhs;
                index += 4;
            }
            2 => {
                let left = codes[index + 1];
                let right = codes[index + 2];
                let res = codes[index + 3];
                let lhs = codes[left];
                let rhs = codes[right];
                codes[res] = lhs * rhs;
                index += 4;
            }
            99 => break,
            _ => panic!("Unknown op code {} at index {}", codes[index], index),
        }
    }
    codes[0]
}
