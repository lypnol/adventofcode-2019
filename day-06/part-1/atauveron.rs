use std::env::args;
use std::time::Instant;

use std::collections::{HashMap, HashSet};

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> usize {
    // Map of direct orbits (key: center; value: objects in orbit around it)
    let mut orbits: HashMap<String, HashSet<String>> = HashMap::new();
    for line in input.lines() {
        let mut it = line.split(')');
        let center = it.next().unwrap();
        let obj = it.next().unwrap();
        if orbits.contains_key(center) {
            orbits.get_mut(center).unwrap().insert(obj.to_string());
        } else {
            let mut tmp = HashSet::new();
            tmp.insert(obj.to_string());
            orbits.insert(center.to_string(), tmp);
        }
    }
    // Traverse the tree
    count_orbits("COM", 1, &orbits)
}

fn count_orbits(current: &str, depth: usize, orbits: &HashMap<String, HashSet<String>>) -> usize {
    match orbits.get(current) {
        None => 0,
        Some(objects) => {
            let sum: usize = objects
                .iter()
                .map(|obj| count_orbits(obj, depth + 1, orbits))
                .sum();
            depth * objects.len() + sum
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L"),
            42
        )
    }
}
