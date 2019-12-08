use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> usize {
    const WIDTH: usize = 25;
    const HEIGHT: usize = 6;
    const SIZE: usize = WIDTH * HEIGHT;
    let pixels: Vec<u8> = input
        .chars()
        .map(|c| c.to_digit(10).unwrap_or(0) as u8)
        .collect();

    let layers = input.len() / SIZE;
    let mut zeros: Vec<usize> = vec![0; layers];
    let mut ones: Vec<usize> = vec![0; layers];
    let mut twos: Vec<usize> = vec![0; layers];

    let mut index = 0;
    let mut layer = 0;
    for pixel in pixels {
        match pixel {
            0 => zeros[layer] += 1,
            1 => ones[layer] += 1,
            2 => twos[layer] += 1,
            _ => (),
        };
        index += 1;
        if index == SIZE {
            index = 0;
            layer += 1;
        }
    }

    let mut index_min = 0;
    let mut min_loc = usize::max_value();
    for index in 0..zeros.len() {
        if zeros[index] < min_loc {
            min_loc = zeros[index];
            index_min = index;
        }
    }
    ones[index_min] * twos[index_min]
}
