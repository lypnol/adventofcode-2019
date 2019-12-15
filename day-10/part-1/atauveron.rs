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

fn run(input: &str) -> usize {
    let mut asteroids: Vec<(isize, isize)> = Vec::new();
    let mut x = 0;
    for line in input.lines() {
        for (y, c) in line.char_indices() {
            if c == '#' {
                asteroids.push((x, y as isize));
            }
        }
        x += 1;
    }
    let mut count: Vec<usize> = Vec::new();
    for index in 0..asteroids.len() {
        count.push(count_visible(index, &asteroids));
    }
    // Find and return the maximum
    let mut max_loc = 0;
    for v in count {
        if v > max_loc {
            max_loc = v;
        }
    }
    max_loc
}

fn count_visible(index: usize, asteroids: &Vec<(isize, isize)>) -> usize {
    let (pos_x, pos_y) = asteroids[index];
    let mut directions: HashSet<(isize, isize)> = HashSet::new();
    for asteroid in asteroids {
        if asteroid.0 == pos_x && asteroid.1 == pos_y {
            continue;
        }
        let d_x = asteroid.0 - pos_x;
        let d_y = asteroid.1 - pos_y;
        let d = gcd(d_x.abs() as usize, d_y.abs() as usize) as isize;
        directions.insert((d_x / d, d_y / d));
    }
    directions.len()
}

fn gcd(first: usize, second: usize) -> usize {
    // variable names based off Euclidean division equation: a = b * q + r
    let (mut a, mut b) = if first > second {
        (first, second)
    } else {
        (second, first)
    };

    while b != 0 {
        let r = a % b;
        a = b;
        b = r;
    }

    a
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let input = "......#.#.\n#..#.#....\n..#######.\n.#.#.###..\n.#..#.....\n..#....#.#\n#..#....#.\n.##.#..###\n##...#..#.\n.#....####\n";
        assert_eq!(run(input), 33);
    }
}
