import os
# import constants

##########
# Constants
##########

# PATH = "C:/.../test/"
# PATH = "C:/Users/PC/Desktop/fer/5_semestar/prevodenje_programskih_jezika/lab/laksi/lab1/testovi0/"

TESTS_PATH = "C:/Users/PC/Desktop/fer/5_semestar/prevodenje_programskih_jezika/lab/laksi/lab1/testovi0/"

# PROGRAM_NAME = "C:\\...\\solution.py"
PROGRAM_PATH = "C:\\git\\evaluator\\solution.py"


IS_CODE_IN_JAVA = False

TEST_COUNT = 0
FLAG_ADD_ZERO = True
PASSED_TESTS = 0

INPUT_FILES_PATH = "test.in"
OUTPUT_FILES_PATH = "test.out"

##########
# Subroutines
##########


def test():
  global TEST_COUNT

  # java programs
  # program_output_lines = os.popen("java -cp bin ClassName < " + PATH + str(TEST_COUNT) + "\\primjer.in").read().split(
  #   "\n")

  program_output_lines = os.popen("py " + PROGRAM_PATH + " < \"" + TESTS_PATH + str(TEST_COUNT) +
                                  "/" +INPUT_FILES_PATH + "\"").read().split("\n")
  correct_output_lines = open(TESTS_PATH + str(TEST_COUNT) + "/" + OUTPUT_FILES_PATH, 'r').read().split("\n")

  if str(program_output_lines) != str(correct_output_lines):
    print("program's output " + str(program_output_lines))
    print("correct output   " + str(correct_output_lines))

  TEST_COUNT += 1
  max_length = 0
  for correct_output_line in correct_output_lines:
    if len(correct_output_line) > max_length:
      max_length = len(correct_output_line)

  if correct_output_lines == program_output_lines:
    global PASSED_TESTS
    PASSED_TESTS += 1
    return True
  else:
    try:
      print(open(TESTS_PATH + str(TEST_COUNT - 1) + "/test.in", 'r').read())
    except:
      print(open(TESTS_PATH + str("00") + "/test.in", 'r').read())

    print("lijevo je tocno")
    print("lijevo je tocno")
    counter = 0
    for correct_output_line in correct_output_lines:

      temp_len = max_length - len(correct_output_line)
      try:
        if counter < 10:
          print(str(counter) + "  " + correct_output_line +
                (temp_len + 2) * " " + program_output_lines[counter])
        else:
          print(str(counter) + " " + correct_output_line +
                (temp_len + 2) * " " + program_output_lines[counter])
      except:
        print("error")
        break
      counter += 1

    print("error occured in following lines:")
    counter = 0
    for program_output_line in program_output_lines:
      if program_output_line != correct_output_lines[counter]:
        print(str(counter) + "; " + str(program_output_line))

      counter += 1
    return False


def test_programs_path():
  from os import path
  if not path.exists(PROGRAM_PATH):
    print("Error occured during opening program\nCheck program's path constant")
    import sys
    sys.exit()


if __name__ == '__main__':
  from os import path
  if not path.exists(TESTS_PATH + str(TEST_COUNT) + "/test.out"):
    print("Error occured during opening test\nCheck tests path constant")

  test_programs_path()

  # kolko testova ima
  for file in os.listdir(TESTS_PATH):
    print(file)

  # import sys
  # sys.exit()

  while True:

    try:
      print("try: " + str(TEST_COUNT).rjust(2))
      if test():
        pass
      else:
        print("incorrect")
        print()

    except:
      print("error: main")
      print(str(PASSED_TESTS) + " / " + str(TEST_COUNT))
      break
