use std::fs;
use std::vec::Vec;

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Input does not exist!");

    let split = contents.split('\n');

    let mut total: i32 = 0;

    for line in split {
        let mut nums = Vec::new();
        for c in line.bytes() {
            if (c <= 57) && (c >= 48) {
                nums.push(c - 48)
            }
        }

        let first = nums[0] as i32;
        let last = nums[nums.len() - 1] as i32;

        total += first * 10 + last;
    }

    println!("Answer: {total}")
}
