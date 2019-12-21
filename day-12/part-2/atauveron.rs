use std::env::args;
use std::time::Instant;

type Vec3D = (isize, isize, isize);

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> isize {
    let lines = input.lines();
    let mut positions: Vec<Vec3D> = Vec::with_capacity(4);
    for line in lines {
        let coords: Vec<&str> = line.split(',').map(|s| s.trim()).collect();

        let tmp: Vec<&str> = coords[0].split('=').collect();
        let x = tmp[1].parse::<isize>().unwrap();
        let tmp: Vec<&str> = coords[1].split('=').collect();
        let y = tmp[1].parse::<isize>().unwrap();
        let tmp: Vec<&str> = coords[2].split('=').collect();
        let z = tmp[1][..tmp[1].len() - 1].parse::<isize>().unwrap();

        positions.push((x, y, z));
    }

    let positions_x: Vec<isize> = positions.iter().map(|p| p.0).collect();
    let repeat_x = find_repeat(positions_x);

    let positions_y: Vec<isize> = positions.iter().map(|p| p.1).collect();
    let repeat_y = find_repeat(positions_y);

    let positions_z: Vec<isize> = positions.iter().map(|p| p.2).collect();
    let repeat_z = find_repeat(positions_z);

    let tmp = lcm(repeat_x, repeat_y);
    lcm(tmp, repeat_z)
}

fn find_repeat(positions_init: Vec<isize>) -> isize {
    let mut positions = positions_init.clone();
    let speeds_init = vec![0; 4];
    let mut speeds = speeds_init.clone();

    let mut steps = 0;

    loop {
        steps += 1;
        let acc = compute_acceleration(&positions);
        for i in 0..4 {
            speeds[i] += acc[i];
        }
        for i in 0..4 {
            positions[i] += speeds[i];
        }
        if positions == positions_init && speeds == speeds_init {
            break;
        }
    }

    steps
}

fn compute_acceleration(positions: &[isize]) -> Vec<isize> {
    let mut accelerations: Vec<isize> = vec![0; 4];
    for i in 0..4 {
        for j in i + 1..4 {
            if positions[i] < positions[j] {
                accelerations[i] += 1;
                accelerations[j] -= 1;
            } else if positions[i] > positions[j] {
                accelerations[i] -= 1;
                accelerations[j] += 1;
            }
        }
    }
    accelerations
}

fn lcm(a: isize, b: isize) -> isize {
    a * b / gcd(a, b)
}

// From https://codereview.stackexchange.com/questions/186382/rust-compute-gcd-modularity-references
fn gcd(mut a: isize, mut b: isize) -> isize {
    while b != 0 {
        let tmp = a;
        a = b;
        b = tmp % b;
    }
    a
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let input = "<x=-1, y=0, z=2>\n<x=2, y=-10, z=-7>\n<x=4, y=-8, z=8>\n<x=3, y=5, z=-1>";
        assert_eq!(run(input), 2772)
    }
}
