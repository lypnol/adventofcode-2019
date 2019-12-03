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

fn run(input: &str) -> isize {
    input
        .split_whitespace()
        .map(|w| {
            let mass = w.parse().unwrap_or(0);
            mass / 3 - 2
        })
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("12\n14\n"), 4)
    }
}
