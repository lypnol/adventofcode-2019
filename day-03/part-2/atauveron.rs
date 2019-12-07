use std::env::args;
use std::time::Instant;

use std::collections::HashSet;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> isize {
    let mut lines = input.lines();
    let first = lines.next().unwrap().split(",");
    let second = lines.next().unwrap().split(",");
    // First wire
    let mut first_pos: Vec<(isize, isize)> = Vec::new();
    let mut pos = (0, 0);
    for mov in first {
        let dir = mov.chars().nth(0).unwrap();
        let dist = mov[1..].parse::<isize>().unwrap_or(0);
        match dir {
            'R' => {
                for _ in 0..dist {
                    pos.0 += 1;
                    first_pos.push(pos);
                }
            }
            'L' => {
                for _ in 0..dist {
                    pos.0 -= 1;
                    first_pos.push(pos);
                }
            }
            'U' => {
                for _ in 0..dist {
                    pos.1 += 1;
                    first_pos.push(pos);
                }
            }
            'D' => {
                for _ in 0..dist {
                    pos.1 -= 1;
                    first_pos.push(pos);
                }
            }
            _ => panic!("Unknown vector {}", mov),
        };
    }

    // Second wire and intersection search
    let mut second_pos: Vec<(isize, isize)> = Vec::new();
    let mut pos = (0, 0);
    for mov in second {
        let dir = mov.chars().nth(0).unwrap();
        let dist = mov[1..].parse::<isize>().unwrap_or(0);
        match dir {
            'R' => {
                for _ in 0..dist {
                    pos.0 += 1;
                    second_pos.push(pos);
                }
            }
            'L' => {
                for _ in 0..dist {
                    pos.0 -= 1;
                    second_pos.push(pos);
                }
            }
            'U' => {
                for _ in 0..dist {
                    pos.1 += 1;
                    second_pos.push(pos);
                }
            }
            'D' => {
                for _ in 0..dist {
                    pos.1 -= 1;
                    second_pos.push(pos);
                }
            }
            _ => panic!("Unknown vector {}", mov),
        };
    }

    // Find the intersections
    let mut first_set: HashSet<(isize, isize)> = HashSet::new();
    for (x, y) in &first_pos {
        first_set.insert((*x, *y));
    }
    let mut second_set: HashSet<(isize, isize)> = HashSet::new();
    for (x, y) in &second_pos {
        second_set.insert((*x, *y));
    }
    let mut min_local = usize::max_value();
    for (x, y) in first_set.intersection(&second_set) {
        let score = first_pos.iter().position(|&tmp| tmp == (*x, *y)).unwrap()
            + second_pos.iter().position(|&tmp| tmp == (*x, *y)).unwrap();
        if score < min_local {
            min_local = score;
        }
    }
    // +1 because of the inclusive range
    // +1 because index 0 is step 1 (and not step 0 at (0,0))
    min_local as isize + 2
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83"),
            610
        );
        assert_eq!(
            run(
                "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
            ),
            410
        );
    }
}
