import os

# tests path
PATH = "C:/.../test/"

# program path

PROGRAM_NAME = "C:\\...\\solution.py"
# solution_recursion
TEST_COUNT = 0
FLAG_ADD_ZERO = True
PASSED_TESTS = 0


def test():
    global TEST_COUNT
    # java programs
    program_output_lines = os.popen("java -cp bin ClassName < " +PATH+str(TEST_COUNT)+"\\primjer.in").read().split("\n")

    # python programs
    # program_output_lines = os.popen("py " + PROGRAM_NAME + " < \"" +
    #                                 PATH + str(TEST_COUNT) + "/test.in" + "\"").read().split("\n")
    correct_output_lines = open(PATH + str(TEST_COUNT) + "/test.out", 'r').read().split("\n")



    if str(program_output_lines) != str(correct_output_lines):
        print("prog " + str(program_output_lines))
        print("corr " + str(correct_output_lines))
        c = (open(PATH + str(TEST_COUNT) + "/Test.pj", 'r').read().split("\n"))
        for i in c: print(i)

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
            print(open(PATH + str(TEST_COUNT-1) + "/test.in", 'r').read())
        except:
            print(open(PATH + str("00") + "/test.in", 'r').read())

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

########################
# Main
########################
while True:

    try:
        print("try: " + str(TEST_COUNT))
        if test():
            pass
        else:
            print("incorrect")
        print()
    except:
        print("err")
        print(str(PASSED_TESTS) + " / " + str(TEST_COUNT))
        break
