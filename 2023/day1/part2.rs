use std::fs;
use std::vec::Vec;

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Input does not exist!");

    let split = contents.split('\n');

    let mut total: i32 = 0;

    let numbers = [
        "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    ];

    for line in split {
        let mut nums: Vec<i32> = Vec::new();
        for i in 0..line.len() {
            for (j, num) in numbers.iter().enumerate() {
                let cur_char = line.bytes().nth(i).unwrap();

                if cur_char <= 57 && cur_char >= 48 {
                    nums.push((cur_char - 48) as i32);
                    continue;
                }
                if num.len() + i > line.len() {
                    continue;
                }

                let other = &line[i..(i + num.len())];
                if &num[..] == other {
                    nums.push((j + 1) as i32);
                }
            }
        }

        if nums.len() >= 2 {
            let first = nums[0] as i32;
            let last = nums[nums.len() - 1] as i32;

            total += first * 10 + last;
        }
    }

    println!("Answer: {total}")
}
