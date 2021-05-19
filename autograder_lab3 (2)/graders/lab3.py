from itertools import permutations

def grade_solution(student_output, solution):
  grades = {}

  for field in solution:
    # initially set all matches to false
    grades[field] = {'match': False, 'expected': '', 'obtained': ''}
    
    if solution[field]['match'] == 'exact':
      if field in student_output:
        grades[field]['match'] = student_output[field]['value'] == solution[field]['value']
      
      if not grades[field]['match']:  # add expected output if not matched
        grades[field]['expected'] = solution[field]['value']
        grades[field]['obtained'] = student_output[field]['value'] if field in student_output else ''
    
    elif solution[field]['match'] == 'ordered':
      expected_lines = solution[field]['value']
      obtained_lines = student_output[field]['value'] if field in student_output else []
      grades[field]['match'] = expected_lines == obtained_lines

      if not grades[field]['match']:
        grades[field]['expected'] = '\n'.join(expected_lines)
        grades[field]['obtained'] = '\n'.join(obtained_lines)

    elif solution[field]['match'] == 'contained':
      expected_lines = set(solution[field]['value'])
      alt_expected_lines = set(solution[field]['alternative'])
      obtained_lines = set(student_output[field]['value'] if field in student_output else [])
      grades[field]['match'] = expected_lines == obtained_lines or alt_expected_lines == obtained_lines

      if not grades[field]['match']:
        grades[field]['expected'] = '\n'.join(list(alt_expected_lines.difference(obtained_lines)))
        grades[field]['obtained'] = '\n'.join(list(obtained_lines.difference(alt_expected_lines)))
  
  return grades

def generate_expected_output(subtask_info):
  return subtask_info['expected_output_full']

def parse_output(output, task=None, correct_output=False):
  output_lines = output.split('\n')
  task_output = {}

  field_match = {
    'BRANCHES': 'contained',
    'PREDICTIONS': 'exact',
    'ACCURACY': 'exact',
    'CONFUSION_MATRIX': 'ordered'
  }

  values = []
  curr_field = None
  for line in output_lines:
    if line.strip() == '':
      continue

    if line.strip() == "[BRANCHES]:" or line.strip() == "[CONFUSION_MATRIX]:":  # multi-line fields
      curr_field = line.strip()[1:-2]
      continue
    elif line.startswith("[ACCURACY]:") or line.startswith("[PREDICTIONS]:"):
      # (1) store parse of multi-line fields
      if curr_field is not None:
        task_output[curr_field] = {'value': values}
        if correct_output:
          task_output[curr_field]['match'] = field_match[curr_field]
        curr_field = None
        values = []

      field, *value = line.strip().split()
      field = field[1:-2]
      value = value[0] if field == 'ACCURACY' else ' '.join(value)
      task_output[field] = {'value': value}
      if correct_output:
        task_output[field]['match'] = field_match[field]
    elif curr_field is not None:
      values.append(line.strip())

  # store last parsed field (confusion matrix)
  if curr_field is not None:
    task_output[curr_field] = {'value': values}
    if correct_output:
      task_output[curr_field]['match'] = field_match[curr_field]

  return task_output

def log_results(log_file, report, verbose=False):
  log_file.write(f"{report['id']}\n")
  log_file.write("================\n\n")

  # errors with archive and folder structure
  log_file.write("=== UNARCHIVE AND STRUCTURE ===\n")
  if not report['unarchive']:
    log_file.write(f"Failed! Error: {report['error']}\n\n")
    return
  else:
    log_file.write("OK!\n\n")

  # errors with compiling
  log_file.write("=== COMPILE ===\n")
  if not report['compile']:
    log_file.write(f"Failed! Error: {report['error']}\n\n")
    return
  elif report['lang'] == 'python':
    log_file.write("Skipping (python)\n\n")
  else:
    log_file.write("OK!\n\n")
  
  # evaluation results
  log_file.write('=== EVALUATION ===\n')
  total_tests, total_passed = 0, 0
  for subtask in sorted(report['evaluation_results'], reverse=True):  # Only one task currently: ID3
    log_file.write(f"\n== {subtask.upper()} ==\n")
    
    test_instances = report['evaluation_results'][subtask]
    subtask_tests = len(test_instances)
    passed_tests = sum(i['test_passed'] for i in test_instances)
    log_file.write(f"  Passed {passed_tests} / {subtask_tests} tests.\n")
    print(f"  Passed {passed_tests} / {subtask_tests} tests.\n")
    total_tests += subtask_tests
    total_passed += passed_tests

    if verbose:  # logged in a separate file for each student with detailed info about failed tests
      for i in test_instances:
        if not i['test_passed']:
          log_file.write(f"\n- Failed test: {i['command']}\n")
          print(f"\n- Failed test: {i['command']}\n")

          if not i['execute']:
            log_file.write(f"Execution failed with error (process returned non-zero exit code):\n{i['output']}\n")
          elif not i['timeout']:
            log_file.write("Execution timed out.\n")
          else:
            mismatched_fields = [field for field in i['field_results'] if not i['field_results'][field]['match']]
            for mis_field in mismatched_fields:
              log_file.write(f"- Mismatch with field: {mis_field}\n")
              log_text = 'Branches created but not expected' if mis_field == 'BRANCHES' else 'Obtained output'
              log_file.write(f"-> {log_text}:\n")
              log_file.write(i['field_results'][mis_field]['obtained'])
              log_text = 'Missing branches' if mis_field == 'BRANCHES' else 'Expected output'
              log_file.write(f"\n-> {log_text}:\n")
              log_file.write(i['field_results'][mis_field]['expected'])
              log_file.write('\n')
            log_file.write("--> Complete obtained output:\n")
            log_file.write(i['output'] + '\n')
            log_file.write('--> Complete expected output:\n')
            log_file.write(i['expected_output'] + '\n')
  log_file.write("\n=== TOTAL RESULTS ===\n")
  log_file.write(f"{total_passed} / {total_tests} tests passed. ({total_passed * 100. / total_tests}%)\n\n")
