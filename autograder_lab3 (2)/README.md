## Lab Assignments Autograder 

This repository contains code used for evaluating lab assignments in the "Introduction to Artificial Intelligence" course at FER.

Autograder is implemented as a Python script that iterates through students' solutions, runs the tests for a given assignment, and outputs the log file containing evalatuion results.

For each lab assignment the text files used as input as well as JSON descriptors of tests which should be run, are given in a separate subfolder inside the `data` folder.
Files for all new assignments should be placed in a new subfolder inside the `data` folder. Each assignment folder should contain two subfolders: (1) `files`, with all the input files that will be passed to the solution during evaluation, and (2) `test_suites`, with all the JSON files in which evaluation tests are defined.

## Arguments

The autograder script accepts the following arguments:
* name of the folder inside the `data` folder, indicating which lab assignment is being evaluated,
* `-solutions`: path to the folder containing students' solutions,
* `-test_files`: name of the folder inside `data/lab[x]` folder containing files to be used as input,
* `-test_suites`: name of the folder inside `data/lab[x]` folder containing JSON test suites to be run,
* `-evaluation_log`: name of the file in which complete log for all solutions is printed,
* `-for_jmbag`: JMBAG or name of the student which solution should be evaluated (used for evaluating single solution in a folder),
* `--root`: flag indicating that solutions folder contains subfolders with students' solutions.

## Running

Steps for obtaining autograder output for archived solution:

1. Place the zip archive with solution in a folder named after your JMBAG, and place that folder inside `solutions/` folder. 
For example, if your JMBAG is `0123456789`, you should first create a zip archive titled `0123456789.zip` following the instructions for the assignment, 
and then place that archive inside `01234566789/` folder, which should finally be placed in the `solutions/` folder. 
The full path to the zip archive should then be: `solutions/0123456789/0123456789.zip`.
An example folder with a zip archive containing (non-working) solution is given in the `solutions/` folder.

2. Run the following command to obtain the results for the solution to the first lab assignment:

```python
python autograder.py lab1
```
3. Check out the general output in `full.log` file and a more detailed output (in case of failed tests) in the log files inside each student's folder inside `solutions/` folder.

The autograder will perform three steps when evaluating your solution in the following order:
1. validating that the folder structure is as requested,
2. attempting to compile the solution,
3. evaluating the solution against the provided test cases.
If steps 1 or 2 fail, the subsequent step(s) are not executed.

The autograder's general output will be printed in a single file for all solutions provided inside the `solutions/` folder.
In addition, a detailed output for each provided solution will be printed inside that solution's folder in the `solutions/` folder.

## Prerequisites

The code for autograder was tested with Python 3.7.4.

We suggest you use `conda` for creating a virtual environment with that specific version of Python. 
Instructions for installing conda are available here: https://docs.conda.io/en/latest/miniconda.html

Once you install conda, you can run the following command to create a Python 3.7.4 environment:

```bash
conda create -n autograder_env python=3.7.4
```

Once the environment is created, you can activate it using:

```bash
conda activate autograder_env
```

Then you can run the above given command for obtaining autograder's output.