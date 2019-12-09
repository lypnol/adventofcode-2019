use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

const WIDTH: usize = 25;
const HEIGHT: usize = 6;

fn run(input: &str) -> usize {
    let layers = input.as_bytes()
        .chunks_exact(WIDTH * HEIGHT);

    let min_layer = layers
        .min_by_key(|&layer| {
            layer.iter().filter(|&&x| x == b'0').count()
        })
        .unwrap();

    layer_value(min_layer)
}

fn layer_value(layer: &[u8]) -> usize {
    // Filter
    let ones = layer.iter().filter(|&&x| x == b'1').count();
    let twos = layer.iter().filter(|&&x| x == b'2').count();

    // Fold
//    let (ones, twos) = layer.iter().fold((0,0), |(ones, twos), &n| {
//        if n == b'1' { (ones+1,twos) } else if n == b'2' { (ones,twos+1) } else { (ones,twos) }
//    });

    // Loop
//    let (mut ones, mut twos) = (0, 0);
//    for &n in layer {
//        if n == b'1' {
//            ones += 1;
//        }
//        else if n == b'2' {
//            twos += 1;
//        }
//    }

    ones * twos
}
