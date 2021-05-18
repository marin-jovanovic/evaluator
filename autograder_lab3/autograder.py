import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import zipfile
from distutils.dir_util import copy_tree
from functools import partial
from subprocess import CalledProcessError, TimeoutExpired
from tempfile import TemporaryDirectory

ERR_EXECUTE = -1
ERR_TIMEOUT = -2
CODE_OK = 1


def unarchive(archive_path, output_dir='lab_solutions', archive_type='zip'):
    if archive_type == 'zip':
        try:
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(output_dir)
        except zipfile.BadZipfile as e:
            # Failed
            return False, e
    else:
        return False, f"Unknown archive type: {archive_type}"
    return True, None


def compile(path_to_solution, language):
    """Compile a single solution, given the path and the pre-determined language
    """
    # Cache current dir, return after compile or in case of errors
    cwd = os.getcwd()
    # cwd = return_to_dir

    try:
        if language == 'python':
            # No need to compile
            return True, ""

        elif language == 'java':
            # Move to solution
            os.chdir(path_to_solution)
            # Compilation is done via maven
            cmd = 'mvn -q clean compile'.split()
            if os.name != 'nt':
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL).wait()
            else:
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL, shell=True).wait()
            # Restore directory
            os.chdir(cwd)
            return True, ""

        elif language == 'cpp':
            os.chdir(path_to_solution)

            # Makefile should be copied prior
            if not os.path.exists('Makefile'):
                shutil.copy(os.path.join(cwd, 'Makefile'), path_to_solution)

            cmd = ['make' if os.name != 'nt' else 'mingw32-make']
            output = subprocess.Popen(cmd).wait()
            print("After compile: ", os.listdir('.'))
            # Check if the solution executable exists after compilation
            if not os.path.exists('solution') and not os.path.exists(
                'solution.exe'):
                os.chdir(cwd)
                return False, "No entry point"
            os.chdir(cwd)
            return True, ""

    # Should make this a bit prettier
    except Exception as e:
        # Make sure that directory is restored even if compilation errored out
        os.chdir(cwd)
        return False, str(e)


def validate_solution_structure(solution_folder):
    # Flag if empty or invalid (differentiate w error)
    # Enumerate all non-private files in the extracted solution folder
    folder_files = [f for f in os.listdir(solution_folder) if
                    not f.startswith('__')]

    if not folder_files:
        # There are no files in the unarchived solution, empty archive submitted
        return "Empty archive", None, ""

    # Level 1: the only file in the unarchived folder should determine
    # the programming language of the solution (lab[x][cpp/java/py])
    should_be_dir = os.path.join(solution_folder, folder_files[0])
    if not len(folder_files) == 1 or not os.path.isdir(should_be_dir):
        extracted_folder_files = " ".join(folder_files)
        return "Invalid structure", None, extracted_folder_files

    solution_dir = folder_files[0]
    return "OK", solution_dir, ""


# Iterate over student solutions
# 1. A logfile with overview for all students
# 2. A results output file for each student with detailed results

def iterate_student_solutions(solutions_dir=None, evaluation_log_file=None,
                              test_suites_dir=None, test_directory=None,
                              for_jmbag=None,
                              log_results=None, parse_output=None,
                              grade_solution=None,
                              generate_expected_output=None):
    student_reports = {}

    with open(evaluation_log_file, 'wt', encoding="utf-8") as log_file:

        # [Assumption:] the name of the folder for each student is the JMBAG
        # of the student. It can also be a name, ID or any _unique_ identifier
        if for_jmbag is not None:
            solutions = [s for s in os.listdir(solutions_dir) if for_jmbag in s]
        else:
            solutions = os.listdir(solutions_dir)

        # The sorting here is done to ensure execution order is consistent
        for idx, dir_name in enumerate(sorted(solutions)):

            # Default to empty dict in case there's an error
            report = {
                "id": None,
                "evaluation_results": {},
                "unarchive": True,
                "compile": True,
                "lang": '',
                "error": ""
            }

            # [Assumption] The folder of the student solution (downloaded) should contain
            # _only_ one file -- the archive with the solution
            student_dir = os.path.join(solutions_dir, dir_name)
            print(f"Directory: {student_dir}")
            files = list(os.listdir(student_dir))  # should be of length 1
            files = [f for f in files if
                     f != 'autograder.log']  # if autograder.log already exists skip it
            print(f"Files in directory: {files}")

            # inserted start
            #
            # todo make sure this is folder
            for file in os.listdir(student_dir):
                print(file)
                if file.__contains__("."):
                    continue
                else:
                    student_solution_zip = os.path.join(student_dir, file)
                    break
            #
            # inserted end

            # fixme, this was in original version
            # student_solution_zip = os.path.join(student_dir, files[0])

            # [1] Extract the solution into a temporary directory
            with TemporaryDirectory() as tmpdir:
                print(tmpdir)

                # my add
                from distutils.dir_util import copy_tree
                copy_tree(student_solution_zip, tmpdir)

                # fixme
                # # [1.1] Try to unarchive solution
                # success, message = unarchive(student_solution_zip,
                #                              output_dir=tmpdir)
                #
                # if not success:
                #     # Wrong archive type (maybe allow multiple archive types to be extracted)
                #     report["unarchive"] = False
                #     _, archive_name = os.path.split(student_solution_zip)
                #     error_log = f"Wrong archive type {archive_name}"
                #     report["error"] = error_log
                #     student_reports[dir_name] = report
                #     log_results(log_file, report, student_dir)
                #     with open(os.path.join(student_dir, 'autograder.log'), 'wt',
                #               encoding="utf-8") as student_log:
                #         log_results(student_log, report, verbose=True)
                #     continue

                report['id'] = files[0].split('.')[0]

                # [1.2] Check if structure looks like it should
                validation_result, solution_root, error_meta = validate_solution_structure(
                    tmpdir)


                if solution_root is None:
                    # Log error, assign 0 points and continue to next solution
                    error_log = f"{validation_result} {error_meta}"
                    report["unarchive"] = False
                    report["error"] = error_log
                    student_reports[dir_name] = report
                    log_results(log_file, report, student_dir)
                    with open(os.path.join(student_dir, 'autograder.log'), 'wt',
                              encoding="utf-8") as student_log:
                        log_results(student_log, report, verbose=True)
                    continue

                # Determine the language of the solution
                if solution_root.endswith('py'):
                    lang = 'python'
                elif solution_root.endswith('java'):
                    lang = 'java'
                elif solution_root.endswith('cpp'):
                    lang = 'cpp'
                else:
                    # Invalid naming -- log error, assign 0 points
                    report["unarchive"] = False
                    error_log = f"Unknown language {solution_root}"
                    report["error"] = error_log
                    student_reports[dir_name] = report
                    log_results(log_file, report, student_dir)
                    with open(os.path.join(student_dir, 'autograder.log'), 'wt',
                              encoding="utf-8") as student_log:
                        log_results(student_log, report, verbose=True)
                    continue
                report["lang"] = lang

                # [2] Compile the solution
                solution_dir = os.path.join(tmpdir, solution_root)
                compile_result, compile_error = compile(solution_dir, lang)
                if not compile_result:
                    # Log error, assign 0 points and continue to next solution
                    report["compile"] = False
                    report[
                        "error"] = f"Compile error: [{lang}]: {compile_error}"
                    student_reports[dir_name] = report
                    log_results(log_file, report, student_dir)
                    print(os.getcwd())
                    with open(os.path.join(student_dir, 'autograder.log'), 'wt',
                              encoding="utf-8") as student_log:
                        log_results(student_log, report, verbose=True)
                    continue

                # [3] Run the solution
                # Compile and unpack OK, copy files and run evaluation
                # [3.1] Copy required test files and metadata into the temporary directory
                copy_tree(test_directory, solution_dir)

                # [3.2] Actually evaluate solution on test suites
                for filename in os.listdir(test_suites_dir):
                    if filename.endswith('.json'):
                        test_suite = json.load(
                            open(os.path.join(test_suites_dir, filename)))
                        results = run_evaluation(solution_dir, lang,
                                                 test_suite=test_suite,
                                                 parse_output=parse_output,
                                                 grade_solution=grade_solution,
                                                 generate_expected_output=generate_expected_output)
                        for subtask in results:
                            if subtask not in report["evaluation_results"]:
                                report["evaluation_results"][subtask] = []
                            report["evaluation_results"][subtask] += results[
                                subtask]

                student_reports[dir_name] = report

                # fixme
                # input("pre last")

            # Log general student's results into a general file (log_file)
            log_results(log_file, report)

            # Log detailed student's results into student's log file (inside student_dir)
            with open(os.path.join(student_dir, 'autograder.log'), 'wt',
                      encoding="utf-8") as student_log:
                log_results(student_log, report, verbose=True)



    return student_reports


def run_evaluation(path_to_solution, language,
                   test_suite, expected_output=None,
                   verbose=False, parse_output=None, grade_solution=None,
                   generate_expected_output=None):
    results = {}

    for subtask in test_suite:

        if subtask not in results:
            results[subtask] = []

        # test_suite is a dict with subtask as key and a list of test instances as value
        for test_instance in test_suite[subtask]:

            report = {
                'test_name': test_instance['name'],
                'execute': True,
                'timeout': True,
                'output': None,
                'expected_output': '',
                'correct_fields': 0,
                'field_results': None,
                'total_fields': None,
                'test_passed': False
            }

            evaluation_fields = [field for field in
                                 test_instance['expected_output_fields'] if
                                 test_instance['expected_output_fields'][field][
                                     'match'] != 'ignored']
            report['total_fields'] = len(evaluation_fields)
            report['field_results'] = {field: False for field in
                                       evaluation_fields}

            execution_args = test_instance['execution_args']
            result_code, result, command = execute(path_to_solution, language,
                                                   execution_args)
            report['result_code'] = result_code
            report['command'] = command

            # Log various possible errors
            if result_code == ERR_EXECUTE:
                # Execution failed, log the error
                report['execute'] = False
                report['output'] = result

            elif result_code == ERR_TIMEOUT:
                # Solution timed out
                report['timeout'] = False

            elif result_code == CODE_OK:
                # Executed OK, store result
                report['output'] = result

                # [1] Parse student's output
                student_output = parse_output(result, task=subtask)
                # [2] Compare output with correct solution
                field_matches = grade_solution(student_output, test_instance[
                    'expected_output_fields'])
                # [3] Store info about matches between student's and correct output
                correct_fields = sum(
                    field_matches[field]['match'] for field in field_matches)
                report['field_results'] = field_matches
                report['correct_fields'] = correct_fields
                report['test_passed'] = correct_fields == report['total_fields']
                if not report['test_passed']:
                    report['expected_output'] = generate_expected_output(
                        test_instance)

            # Append report for this test instance to subtask's list
            results[subtask].append(report)

    return results


def execute(path_to_solution, language, arguments):
    """Execute a single solution and return the output
    """

    # Max allowed 2 minutes
    max_time = 120  # seconds
    # Cache current directory
    curdir = os.getcwd()
    # Move to solution directory
    os.chdir(path_to_solution)

    # Determine run command based on language
    if language == 'python':
        ex_cmd = 'python solution.py'
        command = ex_cmd + ' ' + arguments

    elif language == 'java':
        ex_cmd = 'java -cp target/classes ui.Solution' if os.name != 'nt' \
            else 'java -cp target/classes -Dfile.encoding=UTF-8 ui.Solution'
        command = ex_cmd + ' ' + arguments

    elif language == 'cpp':
        ex_cmd = './solution'
        command = ex_cmd + ' ' + arguments

    print(f"Running: {command}")

    try:
        result = subprocess.check_output(command.split(),
                                         stderr=subprocess.STDOUT,
                                         timeout=max_time,
                                         env={**os.environ.copy(),
                                              'PYTHONUTF8': '1'})
    except CalledProcessError as e:
        os.chdir(curdir)
        error_message = e.output.decode("utf-8")

        return ERR_EXECUTE, error_message, command
    except TimeoutExpired as e:
        os.chdir(curdir)
        return ERR_TIMEOUT, None, command

    result = result.decode("utf-8").strip()

    os.chdir(curdir)
    return CODE_OK, result, command


def parse_arguments():
    parser = argparse.ArgumentParser(description='AI Labs autograder')
    # parser.add_argument('lab', type=str, default='lab1')
    parser.add_argument('-solutions', type=str, default='solutions',
                        help='Directory with student solutions')
    parser.add_argument('-test_suites', type=str, default='test_suites',
                        help='Name of the directory inside data/lab[x] folder containing test_suites')
    parser.add_argument('-test_files', type=str, default='files',
                        help='Name of the directory inside data/lab[x] folder containing files used for testing')
    parser.add_argument('-evaluation_log', type=str, default='full.log',
                        help='Path to file with evalauation log output')
    parser.add_argument('-for_jmbag', type=str, default=None,
                        help='Run only for student JBMAG (name of directory)')
    parser.add_argument('--root', default=False, action='store_true',
                        help='Flag indicating that solutions folder contains subfolders with submissions.')
    return parser.parse_args()


def main():
    args = parse_arguments()
    start = time.time()

    lab_v = "lab3"

    if lab_v == 'lab1':
        from graders.lab1 import log_results, parse_output, grade_solution, \
            generate_expected_output
    elif lab_v == 'lab2':
        from graders.lab2 import log_results, parse_output, grade_solution, \
            generate_expected_output
    elif lab_v == 'lab3':
        from graders.lab3 import log_results, parse_output, grade_solution, \
            generate_expected_output

    test_suites_path = os.path.join('data', lab_v, args.test_suites)
    test_files_path = os.path.join('data', lab_v, args.test_files)
    solutions_path = args.solutions
    evaluation_log_file = args.evaluation_log

    iterator_partial = partial(
        iterate_student_solutions,
        evaluation_log_file=evaluation_log_file,
        test_suites_dir=test_suites_path,
        test_directory=test_files_path,
        for_jmbag=args.for_jmbag,
        log_results=log_results,
        parse_output=parse_output,
        grade_solution=grade_solution,
        generate_expected_output=generate_expected_output
    )

    if args.root:  # solutions folder contains folder for each lab group
        for folder in sorted(os.listdir(solutions_path)):
            group_dir = os.path.join(solutions_path, folder)
            points = iterator_partial(group_dir)
            print(f"Folder {group_dir} done.")
    else:  # solutions folder contains all submissions in a single folder
        points = iterator_partial(solutions_path)

    end = time.time()
    print(f"Total time (seconds): {end - start}")


if __name__ == '__main__':
    main()
