use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn fuel_requirement(mut mass: isize) -> isize {
    let mut total_fuel = 0;
    loop {
        let extra_fuel = mass / 3 - 2;
        mass = extra_fuel;
        if extra_fuel <= 0 {
            break total_fuel
        }
        total_fuel += extra_fuel;
    }
}

fn run(input: &str) -> isize {
    input
        .split_whitespace()
        .map(|w| {
            let mass: isize = w.parse().unwrap();
            fuel_requirement(mass)
        })
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("12\n1969\n"), 968)
    }
}
