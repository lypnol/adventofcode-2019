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

fn check_valid(&pwd: &usize) -> bool {
    let digits = get_digits(pwd);
    let mut increasing_digits = true;
    let mut has_double = false;
    let mut p = 0;
    let mut consecutive_equal = 1;
    for d in digits {
        if d == p {
            consecutive_equal += 1;
        }
        else if consecutive_equal == 2 {
            has_double = true;
            consecutive_equal = 1;
        } else {
            consecutive_equal = 1;
        }

        if d < p {
            increasing_digits = false;
        }
        p = d;
    }
    if consecutive_equal == 2 {
        has_double = true;
    }
    increasing_digits && has_double
}

fn run(input: &str) -> usize {
    let nums: Vec<usize> = input
        .split('-')
        .map(|s| s.parse().unwrap_or(0))
        .collect();

    let (min, max) = (nums[0], nums[1]);
    (min..max+1)
        .filter(&check_valid)
        .map(|n| println!("{}", n))
        .count()
}

 #[cfg(test)]
 mod tests {
     use super::*;

     #[test]
     fn run_test() {
         assert_eq!(check_valid(&777788), true);
     }
 }
