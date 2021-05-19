from itertools import permutations

def grade_solution(student_output, solution):
  grades = {}

  for field in solution:
    if solution[field]['match'] == 'ignored':
      continue
    grades[field] = {'match': False, 'expected': '', 'obtained': ''}
    
    if solution[field]['match'] == 'exact':
      if field in student_output:
        variants = generate_variants(solution[field]['value'])
        grades[field]['match'] = student_output[field]['value'].lower() in variants
      
      if not grades[field]['match']:  # add expected output if not matched
        grades[field]['expected'] = solution[field]['value']
        grades[field]['obtained'] = student_output[field]['value'].lower() if field in student_output else ''
    
    elif solution[field]['match'] == 'ordered':
      expected_lines = solution[field]['value']
      obtained_lines = student_output[field]['value'] if field in student_output else []

      if obtained_lines:
        match = True
        for exp, obt in zip(expected_lines, obtained_lines):
          exp_variants = generate_variants(exp)
          if obt.lower() not in exp:
            match = False
        grades[field]['match'] = match
      
      grades[field]['expected'] = '\n'.join(expected_lines)
      grades[field]['obtained'] = '\n'.join(obtained_lines)
    
    else:
      pass
  
  return grades

# Generate clauses with different order of literals
def generate_variants(conclusion):
  elems = conclusion.split()[:-2]  # everything except "is x" part
  suffix = ' '.join(conclusion.split()[-2:])
  clause_permutations = list(permutations(elems[::2]))
  variants = set()
  for perm in clause_permutations:
    variants.add(' v '.join(perm) + ' ' + suffix)
  return variants

def generate_expected_output(subtask_info):
  return subtask_info['expected_output_full']

def parse_output(output, task='resolution', correct_output=False):
  output_lines = output.split('\n')
  subtask_output = {}

  for line in output_lines:
    if line.startswith("[CONCLUSION]:"):
      if 'CONCLUSION' not in subtask_output:
        subtask_output['CONCLUSION'] = {'value': []}

      if correct_output:
        subtask_output['CONCLUSION']['match'] = 'exact' if task == 'resolution' else 'ordered'
      
      subtask_output['CONCLUSION']['value'].append(' '.join(line.strip().split()[1:]))
      if task == 'resolution':
        subtask_output['CONCLUSION']['value'] = subtask_output['CONCLUSION']['value'][0]
        break  # should be only one conclusion

  return subtask_output

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
  for subtask in report['evaluation_results']:
    test_instances = report['evaluation_results'][subtask]
    total_tests += len(test_instances)
    total_passed += sum(i['test_passed'] for i in test_instances)
  log_file.write("\n=== TOTAL RESULTS ===\n")
  log_file.write(f"{total_passed} / {total_tests} tests passed. ({total_passed * 100. / total_tests:.2f}%)\n")

  for subtask in sorted(report['evaluation_results'], reverse=True):  # print RESOLUTION first
    log_file.write(f"\n== {subtask.upper()} ==\n")
    
    test_instances = report['evaluation_results'][subtask]
    subtask_tests = len(test_instances)
    passed_tests = sum(i['test_passed'] for i in test_instances)
    log_file.write(f"  Passed {passed_tests} / {subtask_tests} tests. Failed {subtask_tests - passed_tests} tests.\n")

  for subtask in sorted(report['evaluation_results'], reverse=True):  # print RESOLUTION first
    log_file.write(f"\n== {subtask.upper()} ==\n")
    test_instances = report['evaluation_results'][subtask]

    if verbose:  # logged in a separate file for each student with detailed info about failed tests
      failed_test_instances, passed_test_instances = [], []
      for i in test_instances:
        if i['test_passed']:
          passed_test_instances.append(i)
        else:
          failed_test_instances.append(i)

      if failed_test_instances:
        log_file.write('\n== FAILED TESTS ==\n')
      for i in failed_test_instances:
        log_file.write(f"\n- Failed test: {i['command']}\n")
        if not i['execute']:
          log_file.write(f"Execution failed with error (process returned non-zero exit code):\n{i['output']}\n")
        elif not i['timeout']:
          log_file.write("Execution timed out.\n")
        else:
          mismatched_fields = [field for field in i['field_results'] if not i['field_results'][field]['match']]
          
          for mis_field in mismatched_fields:
            log_file.write(f"- Mismatch with field: {mis_field}\n")
            log_file.write("-> Obtained output:\n")
            if isinstance(i['field_results'][mis_field]['obtained'], list):
              log_file.write('\n'.join(i['field_results'][mis_field]['obtained']))
            else:
              log_file.write(i['field_results'][mis_field]['obtained'])
            log_file.write(f"\n-> Expected output:\n")
            if isinstance(i['field_results'][mis_field]['expected'], list):
              log_file.write('\n'.join(i['field_results'][mis_field]['expected']))
            else:
              log_file.write(i['field_results'][mis_field]['expected'])
            log_file.write('\n')
          log_file.write("--> Complete obtained output:\n")
          output_len = len(i['output'])
          if output_len > 1000000000:
            log_file.write(i['output'][:10000])
            log_file.write('\n')
          else:
            log_file.write(i['output'] + '\n')
        log_file.write('\n' * 2)
      
      if passed_test_instances:
        log_file.write("== PASSED TESTS ==\n")
      for i in passed_test_instances:
        log_file.write(f"\n- Passed test: {i['test_name']}\n")
        log_file.write("-> Complete obtained output:\n")
        log_file.write(i['output'] + '\n')
          
