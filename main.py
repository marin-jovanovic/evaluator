##########
# Constants
##########
import constants
import os


##########
# Subroutines
##########


# def test():
#   # global TEST_COUNT
#
#   # java programs
#   # program_output_lines = os.popen("java -cp bin ClassName < " + PATH + str(TEST_COUNT) + "\\primjer.in").read().split(
#   #   "\n")
#
#   program_output_lines = os.popen("py " + PROGRAM_PATH + " < \"" + TESTS_PATH + str(TEST_COUNT) +
#                                   "/" +INPUT_FILES_PATH + "\"").read().split("\n")
#   correct_output_lines = open(TESTS_PATH + str(TEST_COUNT) + "/" + OUTPUT_FILES_PATH, 'r').read().split("\n")
#
#   if str(program_output_lines) != str(correct_output_lines):
#     print("program's output " + str(program_output_lines))
#     print("correct output   " + str(correct_output_lines))
#
#   TEST_COUNT += 1
#   max_length = 0
#   for correct_output_line in correct_output_lines:
#     if len(correct_output_line) > max_length:
#       max_length = len(correct_output_line)
#
#   if correct_output_lines == program_output_lines:
#     global PASSED_TESTS
#     PASSED_TESTS += 1
#     return True
#   else:
#     try:
#       print(open(TESTS_PATH + str(TEST_COUNT - 1) + "/test.in", 'r').read())
#     except:
#       print(open(TESTS_PATH + str("00") + "/test.in", 'r').read())
#
#     print("left is correct")
#     counter = 0
#     for correct_output_line in correct_output_lines:
#
#       temp_len = max_length - len(correct_output_line)
#       try:
#         if counter < 10:
#           print(str(counter) + "  " + correct_output_line +
#                 (temp_len + 2) * " " + program_output_lines[counter])
#         else:
#           print(str(counter) + " " + correct_output_line +
#                 (temp_len + 2) * " " + program_output_lines[counter])
#       except:
#         print("error")
#         break
#       counter += 1
#
#     print("error occured in following lines:")
#     counter = 0
#     for program_output_line in program_output_lines:
#       if program_output_line != correct_output_lines[counter]:
#         print(str(counter) + "; " + str(program_output_line))
#
#       counter += 1
#     return False


def test_program_path():
  from os import path
  if not path.exists(constants.PROGRAM_PATH):
    print("Error occured during opening program\nCheck \"PROGRAM_PATH\" constant")
    import sys
    sys.exit()


def test_tests_path():
  from os import path
  if not path.exists(constants.TESTS_PATH + str(constants.TEST_COUNT) + "/test.out"):
    print("Error occured during opening test\nCheck \"TESTS_PATH\" constant")


def get_number_of_tests():
  import os

  list = os.listdir(constants.TESTS_PATH)  # dir is your directory path
  return len(list)
  # print (number_files)

  # return number_files
  # import sys
  # sys.exit()


if __name__ == '__main__':

  test_tests_path()
  test_program_path()

  num_of_tests = get_number_of_tests()


  # TODO vrijeme izvodenja ispisat i ispisat max vrijeme izvodenja
  # TODO mogucnost podesavanja vremena koje je potrebno da se breaka ako ne uspije izvritt test

  for file in os.listdir(constants.TESTS_PATH):
    # print(file)

    program_output_lines = os.popen("py " + constants.PROGRAM_PATH + " < \"" + constants.TESTS_PATH +
                                          file + "/" + constants.INPUT_FILES_PATH +
                                          "\"").read().split("\n")
    correct_output_lines = open(constants.TESTS_PATH + file + "/" + constants.OUTPUT_FILES_PATH,
                                "r").read().split("\n")

    if program_output_lines == correct_output_lines:
      print("test " + str(constants.TEST_COUNT).rjust(len(str(num_of_tests))) + " = correct")
      constants.PASSED_TESTS += 1
    else:
      print("test " + str(constants.TEST_COUNT).rjust(len(str(num_of_tests))) + " = false")



      print("   program's output " + str(program_output_lines))
      print("   correct output   " + str(correct_output_lines))


      # max width of lines in correct_output_line
      max_length = 0
      for correct_output_line in correct_output_lines:
        if len(correct_output_line) > max_length:
          max_length = len(correct_output_line)

      # num of lines in correct output file
      num_of_lines = 0

      # def file_len(fname):
      with open(constants.TESTS_PATH + file + "/" + constants.INPUT_FILES_PATH) as f:
        for i, l in enumerate(f):
            pass
      num_of_lines = i + 1



    #   else:
    #     try:
    #       print(open(TESTS_PATH + str(TEST_COUNT - 1) + "/test.in", 'r').read())
    #     except:
    #       print(open(TESTS_PATH + str("00") + "/test.in", 'r').read())
    #
      print("left is correct")
      counter = 0
      for correct_output_line in correct_output_lines:

        temp_len = max_length - len(correct_output_line)
        try:
          # if counter < 10:
          print(str(counter).rjust(2) + "  " + correct_output_line +
                (temp_len + 2) * " " + "| " + program_output_lines[counter])

        except:
          print("error")
          break
        counter += 1



    #
    #     print("error occured in following lines:")
    #     counter = 0
    #     for program_output_line in program_output_lines:
    #       if program_output_line != correct_output_lines[counter]:
    #         print(str(counter) + "; " + str(program_output_line))
    #
    #       counter += 1



    constants.TEST_COUNT += 1

  # import sys
  # sys.exit()

  # while True:
  #
  #   try:
  #     print("try: " + str(TEST_COUNT).rjust(len(str(num_of_tests))))
  #     if test():
  #       pass
  #     else:
  #       print("incorrect")
  #       print()
  #
  #   except:
  #     print("error: main")
  #     print(str(PASSED_TESTS) + " / " + str(TEST_COUNT))
  #     break
