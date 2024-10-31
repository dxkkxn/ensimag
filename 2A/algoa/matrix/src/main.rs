use rand::rngs::StdRng;
use rand::{Rng, SeedableRng};
use rayon::prelude::*;

fn main() {
    let mut matrix: Vec<Vec<u32>> = vec![vec![0; 10]; 10];
    // rng.gen_range(1..=100);
    matrix.par_iter_mut().for_each(|l| {
        let mut rng = StdRng::from_seed([0; 32]);
        l.par_iter_mut()
         .for_each(|element| {
             *element = rng.gen_range(0..=100)} )
    });
    println!("Hello, world! {:?}", matrix);
}
