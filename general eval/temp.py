##########
# Constants
##########
import os

import constants
import multiprocessing


##########
# Subroutines
##########


def print_blue(data):
    print("\33[34m" + data + "\033[0m")


def print_red(data):
    print("\33[31m" + data + "\033[0m")


def get_programs_output(queue, program_path, args):
    program_output_lines = os.popen("py " + program_path + " " + args).read().split("\n")
    queue.put(program_output_lines)


if __name__ == '__main__':

    time_limit = 10

    # read paths
    temp = [line[:-1] for line in open("log.txt").readlines()]
    program_path = temp[0]
    tests_path = temp[1]

    # print paths
    print_blue("paths")
    print("program path:", program_path)
    print("tests path:", tests_path)
    print()

    # print test files
    print_blue("test files")
    for test in os.listdir(tests_path):
        print(test)
    print()

    import datetime

    biggest_execution_time_seconds = 0
    biggest_execution_time_milliseconds = 0

    for file in os.listdir(tests_path):
        print_blue(80 * "-")
        t_path = tests_path + "/" + file

        print("test:", t_path)

        raw_data = [i[:-1] for i in open(t_path).readlines()]
        print(raw_data)
        args = raw_data[0]

        print("args:", args)
        print("expected output:", raw_data[2:])

        start_time = datetime.datetime.now()
        queue = multiprocessing.Queue()
        p = multiprocessing.Process(target=get_programs_output, args=(queue, program_path, args,))
        p.start()

        p.join(time_limit)

        if p.is_alive():
            p.terminate()
            print('function terminated')
            print_red("too much time")
            p.join()

        program_output_lines = queue.get()

        end_time = datetime.datetime.now()
        execution_time = end_time - start_time
        time_raw = str(execution_time).split(".")
        miliseconds = int(time_raw[1])

        seconds = sum(x * int(t) for x, t in zip([3600, 60, 1], time_raw[0].split(":")))

        if seconds > biggest_execution_time_seconds \
            or (seconds == biggest_execution_time_seconds and miliseconds > biggest_execution_time_milliseconds):
            biggest_execution_time_seconds = seconds
            biggest_execution_time_milliseconds = miliseconds

        correct_output_lines = raw_data[2:]

        if program_output_lines == correct_output_lines:
            print_blue("test correct!")

            constants.PASSED_TESTS += 1
        else:
            print_blue("test failed")

            print("   program's output " + str(program_output_lines))
            print("   correct output   " + str(correct_output_lines))

            # max width of lines in correct_output_line
            max_length = 0
            for correct_output_line in correct_output_lines:
                if len(correct_output_line) > max_length:
                    max_length = len(correct_output_line)

            # num of lines in correct output file
            with open(t_path) as f:
                for i, l in enumerate(f):
                    pass
            num_of_lines = i + 1

            print("\n" + str("    ").rjust(2) + "left is correct")
            counter = 0
            for correct_output_line in correct_output_lines:

                temp_len = max_length - len(correct_output_line)
                try:
                    print(str(counter).rjust(2) + "  " + correct_output_line +
                          (temp_len + 2) * " " + "| " + program_output_lines[counter])
                    if correct_output_line != program_output_lines[counter]:
                        print("error occured in previous line \nrest of output is not displayed")
                        break
                except:
                    print("error")
                    break
                counter += 1

            print()
        constants.TEST_COUNT += 1

    print("\nanalysis results")
    print("tests passed: " + str(constants.PASSED_TESTS) + " / " + str(constants.TEST_COUNT - 1))
    print("longest execution time: " + str(biggest_execution_time_seconds) + "."
          + str(biggest_execution_time_milliseconds) + " [s]")
