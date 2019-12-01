use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output: i32 = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!(
        "_duration:{}.{}",
        elapsed.as_secs() * 1000 + u64::from(elapsed.subsec_millis()),
        elapsed.subsec_micros() - (elapsed.subsec_millis() * 1000)
    );
    println!("{}", output);
}

fn compute_fuel(fuel: i32) -> i32 {
    let extra = (fuel / 3 as i32) -2;
    if extra > 0 {
        fuel + compute_fuel(extra)
    } else {
        fuel
    }
}

fn run(input: &str) -> i32 {
    let mut total_fuel: i32 = 0;
    let weights = input.split_whitespace();
    for weight in weights {
        let fuel = (weight.parse::<i32>().unwrap_or(0) / 3 as i32) - 2;
        total_fuel += compute_fuel(fuel);
    }
    total_fuel
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("12\n1969\n"), 968)
    }
}
