use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn get_digits(mut n: usize) -> Vec<usize> {
    let mut digits = Vec::new();
    while n > 0 {
        digits.push(n % 10);
        n /= 10;
    }
    digits.reverse();
    digits
}

fn check_valid(pwd: usize) -> bool {
    let digits = get_digits(pwd);
    let mut increasing_digits = true;
    let mut has_double = false;
    let mut p = 0;
    for d in digits {
        if d < p {
            increasing_digits = false;
        }
        if d == p {
            has_double = true;
        }
        p = d;
    }
    increasing_digits && has_double
}

fn run(input: &str) -> usize {
    let nums: Vec<usize> = input
        .split('-')
        .map(|s| s.parse().unwrap())
        .collect();

    let (min, max) = (nums[0], nums[1]);
    let count = (min..max+1)
        .filter(|&n| check_valid(n))
        .count();
    count
}
