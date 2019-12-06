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
    let mut neighbours: HashMap<String, HashSet<String>> = HashMap::new();
    for line in input.lines() {
        let mut it = line.split(')');
        let center = it.next().unwrap();
        let obj = it.next().unwrap();
        if neighbours.contains_key(center) {
            neighbours.get_mut(center).unwrap().insert(obj.to_string());
        } else {
            let mut tmp = HashSet::new();
            tmp.insert(obj.to_string());
            neighbours.insert(center.to_string(), tmp);
        }
        if neighbours.contains_key(obj) {
            neighbours.get_mut(obj).unwrap().insert(center.to_string());
        } else {
            let mut tmp = HashSet::new();
            tmp.insert(center.to_string());
            neighbours.insert(obj.to_string(), tmp);
        }
    }
    // Compute the distance
    // Minus two  for the first and last jumps
    dijkstra("YOU", "SAN", &neighbours) - 2
}

fn dijkstra(origin: &str, dest: &str, graph: &HashMap<String, HashSet<String>>) -> usize {
    // Initialise
    let mut distances: HashMap<String, usize> = HashMap::new();
    for vertex in graph.keys() {
        distances.insert(vertex.to_string(), usize::max_value());
    }
    *distances.get_mut(origin).unwrap() = 0;

    let mut to_visit: HashSet<String> = HashSet::new();
    for vertex in graph.keys() {
        to_visit.insert(vertex.to_string());
    }
    // Loop
    while !to_visit.is_empty() {
        let mut min_loc = usize::max_value();
        let mut selected = String::new();
        for vertex in &to_visit {
            if distances.get(vertex).unwrap() < &min_loc {
                min_loc = *distances.get(vertex).unwrap();
                selected = vertex.to_string();
            }
        }
        to_visit.remove(&selected);
        let new_dist = distances.get(&selected).unwrap() + 1;
        for vertex in graph.get(&selected).unwrap().intersection(&to_visit) {
            if new_dist < *distances.get(vertex).unwrap() {
                *distances.get_mut(vertex).unwrap() = new_dist;
            }
        }
    }
    // Return
    *distances.get(dest).unwrap()
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
