# adventOfCode

A list of all my solutions to advent of code through the years. The first year I completed all of the problems was 2022. I am working on building my solution bank for the years prior.

## Current Progress

I am attempted to complete the problems for 2019 through the days of November 2023 before the actual 2023 event.

## Helper code used

I use the advent-of-code-data library that is on pip. I have also made myself some helper functions, these are `startDay.py` and `copier.py`. `startDay.py` gets the data from the website and creates an `input.txt` file for me to get the data and a pre-written starter piece of code that allows me to both test and submit my code. `copier.py` allows me to streamline the writing of my solution to the second part, whilst keeping my part 1 solution. It copies all the important sections of code from my first solution whilst removing the parts no longer necessary.

## Things I want to add

- Solutions in other languages (Haskell, C, Rust)
- Run-time tester

## How to set up and run

### Set-up

Clone the repository then install the advent-of-code-data library via pip, using `python -m pip install advent-of-code-data`. Then install the local library copier using `python -m pip install -e copier`.

### Starting a day

Run the command `python startDay.py <year> <day>`, where year and day will default to the current date if not inputted. This will then create the corresponding folder and files to solve the days problem. It will also make a copy of the input in `input.txt` and create a blank `test.txt` file to input test data into.

### Running code

To run your solution you can run the command `python <year>/<day>/solution.py`, using arguments `-T=<test_answer>` to run from test file, `-R` to run from the input file and submit and `--log=<log_level>` to set the logging level of the 

On success a second file will be created called `solution2.py`, this has all your code copied into a new file so you can keep your old solution with minimal effort. This is called in a similar way to the first solution just changing `solution.py` to `solution2.py`.

### What to do if the copier fails

When the copier fails, you can run it manually via the command `python copier/copier.py <year> <day>` and it will create the `solution2.py` by itself, note that if the file already exists you will have to delete it in order for it to create a new one.
