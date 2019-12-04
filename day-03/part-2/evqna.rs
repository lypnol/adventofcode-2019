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

#[derive(Debug)]
struct WirePos {
    wire_length: isize,
    x: isize, y: isize,
}

fn run(input: &str) -> isize {
    let wires: Vec<Vec<&str>> = input
        .split_whitespace()
        .map(|w| w.split(',').collect())
        .collect();
    
    let turns_A = build_turns(&wires[0]);
    let turns_B = build_turns(&wires[1]);
    let mut intersections = build_intersections(&turns_A, &turns_B);
    intersections.sort_by_key(|x| x.wire_length);

    intersections[1].wire_length    // Skip the origin
}

fn build_turns(wire: &Vec<&str>) -> Vec<WirePos> {
    let (mut x, mut y) = (0, 0);
    let mut wire_length = 0;

    let mut positions = vec![WirePos { x, y, wire_length}];
    for segment in wire {
        let direction = segment.chars().next().unwrap();
        let length: isize = segment[1..].parse().unwrap();
        match direction {
            'L' => x -= length,
            'R' => x += length,
            'U' => y += length,
            'D' => y -= length,
            _ => println!("Wrong direction"),
        }
        wire_length += length;
        positions.push(WirePos { x, y, wire_length});
    }
    positions
}

// Computes intersection [x, y] of segments [a, b] and [c, d] in 1D
// Input segments must be sorted (a <= b and c <= d)
// If intersection is empty result will have x > y
fn segment_overlap(a: isize, b:isize, c:isize, d:isize) -> (isize, isize) {
    (cmp::max(a, c), cmp::min(b, d))
}

#[derive(Debug)]
enum Axis {
    X, Y,
}

fn length_to_intersection(origin: &WirePos, x: isize, y: isize, axis: &Axis) -> isize {
    match axis {
        Axis::Y => origin.wire_length + (x - origin.x).abs(),
        Axis::X => origin.wire_length + (y - origin.y).abs(),
    }
}

fn build_intersections(turns_A: &Vec<WirePos>, turns_B: &Vec<WirePos>) -> Vec<WirePos> {
    let mut intersections: Vec<WirePos> = Vec::new();
    // Du sale
    for (a, b) in turns_A.iter().tuple_windows() {
        let main_axis = if a.x == b.x { Axis::X } else { Axis::Y };
        // Reorder segments for easier comparisons
        let orig_a = a;
        let (a, b) = if a.x <= b.x && a.y <= b.y { (a,b) } else { (b,a) };
        for (c, d) in turns_B.iter().tuple_windows() {
            let orig_c = c;
            let axis_2 = if c.x == d.x { Axis::X } else { Axis::Y };
            
            if a.x == b.x {
                let x = a.x;
                if c.y == d.y {
                    let y = c.y;
                    let (c, d) = if c.x <= d.x { (c,d) } else { (d,c) };
                    if (a.y <= y && y <= b.y) && (c.x <= x && x <= d.x) {
                        let wire_length = length_to_intersection(orig_a, x, y, &main_axis)
                            + length_to_intersection(orig_c, x, y, &axis_2);
                        intersections.push(WirePos { x, y, wire_length });
                    }
                }
                else if c.x == x {
                    let (c, d) = if c.y <= d.y { (c,d) } else { (d,c) };
                    let (y_min, y_max) = segment_overlap(a.y, b.y, c.y, d.y);
                    for y in y_min..y_max+1 {
                        let wire_length = length_to_intersection(orig_a, x, y, &main_axis)
                            + length_to_intersection(orig_c, x, y, &axis_2);
                        intersections.push(WirePos { x, y, wire_length });
                    }
                }
            }
            else if a.y == b.y {
                let y = a.y;
                if c.x == d.x {
                    let x = c.x;
                    let (c, d) = if c.y <= d.y { (c,d) } else { (d,c) };
                    if (a.x <= x && x <= b.x) && (c.y <= y && y <= d.y) {
                        let wire_length = length_to_intersection(orig_a, x, y, &main_axis)
                            + length_to_intersection(orig_c, x, y, &axis_2);
                        intersections.push(WirePos { x, y, wire_length });
                    }
                }
                else if c.y == y {
                    let (c, d) = if c.x <= d.x { (c,d) } else { (d,c) };
                    let (x_min, x_max) = segment_overlap(a.x, b.x, c.x, d.x);
                    for x in x_min..x_max+1 {
                        let wire_length = length_to_intersection(orig_a, x, y, &main_axis)
                            + length_to_intersection(orig_c, x, y, &axis_2);
                        intersections.push(WirePos { x, y, wire_length });
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
        assert_eq!(run("R8,U5,L5,D3\nU7,R6,D4,L4\n"), 30);
        assert_eq!(run("R75,D30,R83,U83,L12,D49,R71,U7,L72\n
            U62,R66,U55,R34,D71,R55,D58,R83\n"), 610);
        assert_eq!(run("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\n
            U98,R91,D20,R16,D67,R40,U7,R15,U6,R7\n"), 410);
    }
}
