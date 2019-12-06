use std::env::args;
use std::time::Instant;

use std::collections::{HashMap, LinkedList};

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> usize {
    // Map of direct orbits (key: objects in orbit; value: center)
    let mut parents: HashMap<String, String> = HashMap::new();
    for line in input.lines() {
        let mut it = line.split(')');
        let center = it.next().unwrap();
        let obj = it.next().unwrap();
        parents.insert(obj.to_string(), center.to_string());
    }
    let you = ancestors("YOU", &parents);
    let santa = ancestors("SAN", &parents);
    // Compute the distance
    let mut common: usize = 0;
    let mut it_you = you.iter();
    let mut it_santa = santa.iter();
    while it_you.next() == it_santa.next() {
        common += 1
    }
    // Minus two for the first and last jumps
    you.len() + santa.len() - 2 * common
}

fn ancestors(object: &str, parents: &HashMap<String, String>) -> LinkedList<String> {
    match object {
        "COM" => LinkedList::new(),
        _ => {
            let parent = parents.get(object).unwrap();
            let mut tmp = ancestors(parent, parents);
            tmp.push_back(parent.to_string());
            tmp
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN"),
            4
        )
    }
}
