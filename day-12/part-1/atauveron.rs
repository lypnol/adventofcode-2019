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
    let mut speeds: Vec<Vec3D> = vec![(0, 0, 0); 4];
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

    for _ in 0..1000 {
        let acc = compute_acceleration(&positions);
        for i in 0..4 {
            speeds[i].0 += acc[i].0;
            speeds[i].1 += acc[i].1;
            speeds[i].2 += acc[i].2;
        }
        for i in 0..4 {
            positions[i].0 += speeds[i].0;
            positions[i].1 += speeds[i].1;
            positions[i].2 += speeds[i].2;
        }
    }

    compute_energy(&positions, &speeds)
}

fn compute_acceleration(positions: &[Vec3D]) -> Vec<Vec3D> {
    let mut accelerations: Vec<Vec3D> = vec![(0, 0, 0); 4];
    for i in 0..4 {
        for j in i + 1..4 {
            if positions[i].0 < positions[j].0 {
                accelerations[i].0 += 1;
                accelerations[j].0 -= 1;
            } else if positions[i].0 > positions[j].0 {
                accelerations[i].0 -= 1;
                accelerations[j].0 += 1;
            }
            if positions[i].1 < positions[j].1 {
                accelerations[i].1 += 1;
                accelerations[j].1 -= 1;
            } else if positions[i].1 > positions[j].1 {
                accelerations[i].1 -= 1;
                accelerations[j].1 += 1;
            }
            if positions[i].2 < positions[j].2 {
                accelerations[i].2 += 1;
                accelerations[j].2 -= 1;
            } else if positions[i].2 > positions[j].2 {
                accelerations[i].2 -= 1;
                accelerations[j].2 += 1;
            }
        }
    }
    accelerations
}

fn compute_energy(positions: &[Vec3D], speeds: &[Vec3D]) -> isize {
    let mut energy = 0;
    for i in 0..4 {
        let potential = positions[i].0.abs() + positions[i].1.abs() + positions[i].2.abs();
        let kinetic = speeds[i].0.abs() + speeds[i].1.abs() + speeds[i].2.abs();
        energy += potential * kinetic;
    }
    energy
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_step() {
        let mut positions = Vec::new();
        positions.push((-1, 0, 2));
        positions.push((2, -10, -7));
        positions.push((4, -8, 8));
        positions.push((3, 5, -1));
        let mut speeds = vec![(0, 0, 0); 4];

        for _ in 0..10 {
            let acc = compute_acceleration(&positions);
            for i in 0..4 {
                speeds[i].0 += acc[i].0;
                speeds[i].1 += acc[i].1;
                speeds[i].2 += acc[i].2;
            }
            for i in 0..4 {
                positions[i].0 += speeds[i].0;
                positions[i].1 += speeds[i].1;
                positions[i].2 += speeds[i].2;
            }
        }

        assert_eq!(positions[0], (2, 1, -3));
        assert_eq!(positions[1], (1, -8, 0));
        assert_eq!(positions[2], (3, -6, 1));
        assert_eq!(positions[3], (2, 0, 4));

        assert_eq!(compute_energy(&positions, &speeds), 179);
    }
}
