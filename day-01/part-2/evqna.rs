use std::env::args;
use std::time::Instant;

fn main() {
    let input = args().nth(1).expect("Please provide an input");
    let now = Instant::now();
    let output = run(&input);
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn fuel_requirement(mut mass: i32) -> i32 {
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

fn run(input: &str) -> i32 {
    let modules = input.split_whitespace().map(|l| l.parse().unwrap_or(0));
    modules.map(fuel_requirement).sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("12\n1969\n"), 968)
    }
}
