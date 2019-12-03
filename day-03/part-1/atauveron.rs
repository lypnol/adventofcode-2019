use std::env::args;
use std::time::Instant;

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
            },
            _ => panic!("Unknown vector {}", mov),
        };
    }
    // Second wire
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
            },
            _ => panic!("Unknown vector {}", mov),
        };
    }
    // Compute every intersection and find the minimum
    let mut min_local = isize::max_value();
    for (x1, y1) in &first_pos {
        for (x2, y2) in &second_pos {
            if x1 == x2 && y1 == y2 {
                let tmp = x1.abs() + y1.abs();
                if tmp < min_local {
                    min_local = tmp;
                }
            }
        }
    }
    // Your code goes here
    min_local
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83"),
            159
        )
    }
}
