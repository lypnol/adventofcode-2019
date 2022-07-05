use std::env::args;
use std::time::Instant;

use std::collections::HashMap;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn indirect_orbits(orbits: &HashMap<&str, Vec<&str>>, depth: usize, root: &str) -> usize {
    if !orbits.contains_key(root) {
        return 0;
    }

    orbits[root].iter()
        .fold(0, |acc, orbiter| acc + depth + indirect_orbits(&orbits, depth + 1, orbiter))
}

fn run(input: &str) -> usize {
    let orbits = input
        .split_whitespace()
        .map(|line| line.split(')').collect::<Vec<_>>());

    let mut orbited_by: HashMap<&str, Vec<&str>> = HashMap::new();
    for objects in orbits {
        let (center, orbiter) = (objects[0], objects[1]);
        orbited_by.entry(center).or_default().push(orbiter);
    }

    indirect_orbits(&orbited_by, 1, "COM")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L"), 42)
    }
}
