use std::env::args;
use std::time::Instant;

use std::str;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

const WIDTH: usize = 25;
const HEIGHT: usize = 6;

fn run(input: &str) -> String {
    let mut image = [0 as u8; WIDTH * HEIGHT];

    input.as_bytes()
        .chunks_exact(WIDTH * HEIGHT)
        .for_each(|layer| {
            for (p, b) in image.iter_mut().zip(layer) {
                if *p == 0 && *b != b'2' {
                    *p = *b;
                }
            }
        });
//    print_dbg(&image);
    str::from_utf8(&image).unwrap().to_string()
}

fn print_dbg(image: &[u8; WIDTH * HEIGHT]) {
    for line in 0..HEIGHT {
        for &n in &image[line*WIDTH..(line+1)*WIDTH] {
            if n == b'1' {
                print!("#");
            } else {
                print!(" ");
            }
        }
        print!("\n");
    }
}
