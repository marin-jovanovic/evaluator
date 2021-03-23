##########
# Constants
##########

t = [line[:-1] for line in open("log.txt").readlines()]

PROGRAM_PATH = t[0]
TESTS_PATH = t[1]

TEST_COUNT = 1
PASSED_TESTS = 0

INPUT_FILES_PATH = "test.a"
OUTPUT_FILES_PATH = "test.b"

UPPER_TIME_BOUND = "10" # in seconds