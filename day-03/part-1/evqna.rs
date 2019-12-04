use std::env::args;
use std::time::Instant;

extern crate itertools;
use itertools::Itertools;
use std::cmp;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

type Coords = Vec<(isize, isize)>;

fn manhattan_norm(x: (isize, isize)) -> isize {
    x.0.abs() + x.1.abs()
}

fn run(input: &str) -> isize {
    let wires: Vec<Vec<&str>> = input
        .split_whitespace()
        .map(|w| w.split(',').collect())
        .collect();
    
    let turns_A = build_turns(&wires[0]);
    let turns_B = build_turns(&wires[1]);
    let mut intersections = build_intersections(&turns_A, &turns_B);
    intersections.sort_by_key(|x| manhattan_norm(*x));
    manhattan_norm(intersections[1])    // Skip the origin
}

fn build_turns(wire: &Vec<&str>) -> Coords {
    let mut pos = (0, 0);
    let mut turn_coords = vec![pos];

    for segment in wire {
        let direction = segment.chars().next().unwrap();
        let length: isize = segment[1..].parse().unwrap();
        match direction {
            'L' => pos.0 -= length,
            'R' => pos.0 += length,
            'U' => pos.1 += length,
            'D' => pos.1 -= length,
            _ => println!("Wrong direction"),
        }
        turn_coords.push(pos);
    }

    turn_coords
}

// Computes intersection [x, y] of segments [a, b] and [c, d] in 1D
// Input segments must be sorted (a <= b and c <= d)
// If intersection is empty result will have x > y
fn segment_overlap(a: isize, b:isize, c:isize, d:isize) -> (isize, isize) {
    (cmp::max(a, c), cmp::min(b, d))
}

fn build_intersections(turns_A: &Coords, turns_B: &Coords) -> Coords {
    let mut intersections: Coords = Vec::new();
    // Du sale
    for (a, b) in turns_A.iter().tuple_windows() {
        // Reorder segments for easier comparisons
        let (a, b) = if a.0 <= b.0 && a.1 <= b.1 { (a,b) } else { (b,a) };
        for (c, d) in turns_B.iter().tuple_windows() {
            if a.0 == b.0 {
                let x_1 = a.0;
                if c.1 == d.1 {
                    let y_2 = c.1;
                    let (c, d) = if c.0 <= d.0 { (c,d) } else { (d,c) };
                    if (a.1 <= y_2 && y_2 <= b.1) && (c.0 <= x_1 && x_1 <= d.0) {
                        intersections.push((x_1, y_2));
                    }
                }
                else if c.0 == x_1 {
                    let (c, d) = if c.1 <= d.1 { (c,d) } else { (d,c) };
                    let (y_min, y_max) = segment_overlap(a.1, b.1, c.1, d.1);
                    for y in y_min..y_max+1 {
                        intersections.push((x_1, y));
                    }
                }
            }
            else if a.1 == b.1 {
                let y_1 = a.1;
                if c.0 == d.0 {
                    let x_2 = c.0;
                    let (c, d) = if c.1 <= d.1 { (c,d) } else { (d,c) };
                    if (a.0 <= x_2 && x_2 <= b.0) && (c.1 <= y_1 && y_1 <= d.1) {
                        intersections.push((x_2, y_1));
                    }
                }
                else if c.1 == y_1 {
                    let (c, d) = if c.0 <= d.0 { (c,d) } else { (d,c) };
                    let (x_min, x_max) = segment_overlap(a.0, b.0, c.0, d.0);
                    for x in x_min..x_max+1 {
                        intersections.push((x, y_1));
                    }
                }
            }
        }
    }
    intersections
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("R8,U5,L5,D3\nU7,R6,D4,L4\n"), 6);
        assert_eq!(run("R75,D30,R83,U83,L12,D49,R71,U7,L72\n
            U62,R66,U55,R34,D71,R55,D58,R83\n"), 159);
        assert_eq!(run("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\n
            U98,R91,D20,R16,D67,R40,U7,R15,U6,R7\n"), 135);
    }
}
