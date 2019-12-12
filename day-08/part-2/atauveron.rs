use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> String {
    const WIDTH: usize = 25;
    const HEIGHT: usize = 6;
    const SIZE: usize = WIDTH * HEIGHT;
    let pixels: Vec<PixelColour> = input
        .chars()
        .map(|c| PixelColour::from(c.to_digit(10).unwrap_or(0)))
        .collect();

    let mut res: Vec<PixelColour> = vec![PixelColour::Transparent; SIZE];

    let mut index = 0;
    for pixel in pixels {
        if res[index] == PixelColour::Transparent && pixel != PixelColour::Transparent {
            res[index] = pixel;
        }
        index += 1;
        if index == SIZE {
            index = 0;
        }
    }

    res.iter().map(|p| char::from(*p)).collect::<String>()
}

#[derive(Clone, Copy, PartialEq, Eq)]
enum PixelColour {
    Black,
    White,
    Transparent,
}

impl From<u32> for PixelColour {
    fn from(val: u32) -> Self {
        match val {
            0 => PixelColour::Black,
            1 => PixelColour::White,
            2 => PixelColour::Transparent,
            _ => panic!("Unknown value for PixelColour"),
        }
    }
}

impl From<PixelColour> for char {
    fn from(val: PixelColour) -> Self {
        match val {
            PixelColour::Black => '0',
            PixelColour::White => '1',
            PixelColour::Transparent => '2',
        }
    }
}
