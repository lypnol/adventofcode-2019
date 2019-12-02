use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!(
        "_duration:{}.{}",
        elapsed.as_secs() * 1000 + u64::from(elapsed.subsec_millis()),
        elapsed.subsec_micros() - (elapsed.subsec_millis() * 1000)
    );
    println!("{}", output);
}

fn run(input: &str) -> usize {
    let mut codes: Vec<usize> = input
        .split(",")
        .map(|x: &str| x.parse::<usize>().unwrap_or(0))
        .collect();
    // Init
    codes[1] = 12;
    codes[2] = 2;
    // Run
    run_codes(&mut codes);
    codes[0]
}

fn run_codes(codes: &mut [usize]) -> () {
    let mut index: usize = 0;
    loop {
        match &codes[index] {
            1 => {
                let left = codes[index + 1];
                let right = codes[index + 2];
                let res = codes[index + 3];
                codes[res] = codes[left] + codes[right];
                index += 4;
            }
            2 => {
                let left = codes[index + 1];
                let right = codes[index + 2];
                let res = codes[index + 3];
                codes[res] = codes[left] * codes[right];
                index += 4;
            }
            99 => break,
            _ => panic!("Unknown op code {} at index {}", codes[index], index),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let mut data = [1, 0, 0, 0, 99];
        run_codes(&mut data);
        assert_eq!(data, [2, 0, 0, 0, 99]);
        let mut data = [1, 1, 1, 4, 99, 5, 6, 0, 99];
        run_codes(&mut data);
        assert_eq!(data, [30, 1, 1, 4, 2, 5, 6, 0, 99]);
    }
}
