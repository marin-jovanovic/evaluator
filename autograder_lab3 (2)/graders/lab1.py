def grade_solution(student_output, solution):
    grades = {}

    for field in solution:
        if solution[field]['match'] == 'ignored':
            continue
        grades[field] = {'match': False, 'expected': '', 'obtained': ''}
        
        if solution[field]['match'] == 'exact':
            if field in student_output:
                grades[field]['match'] = solution[field]['value'] == student_output[field]['value']       
            else:
                grades[field]['match'] = False
            if not grades[field]['match']:  # add expected output if not matched
                if field in student_output: 
                    grades[field]['expected'] = solution[field]['value']
                    grades[field]['obtained'] = student_output[field]['value'] if field in student_output else ''
                else:
                    grades[field]['expected'] = solution[field]['value']
        elif solution[field]['match'] == 'contained':
            correct_lines = set(solution[field]['value'])
            if field in student_output:
                output_lines = set(student_output[field]['value'])
                grades[field]['match'] = output_lines == correct_lines
            else:
                grades[field]['match'] = False
            if not grades[field]['match']:  # add expected output if not matched
                if field in student_output:
                    grades[field]['expected'] = correct_lines.difference(output_lines)
                    grades[field]['obtained'] = output_lines.difference(correct_lines)
                else:
                    grades[field]['expected'] = correct_lines
                    grades[field]['obtained'] = set()
        else:
            pass
    
    return grades


def generate_expected_output(subtask_info):
    expected_lines = [f"# {subtask_info['name']}"]
    fields = subtask_info['expected_output_fields']
    if subtask_info['name'].startswith('HEURISTIC'):
        expected_lines += [f"[CONDITION]: {i}" for i in fields['CONDITIONS']['value']]
        expected_lines.append(f"[CONCLUSION]: {fields['CONCLUSION']['value']}")
    else:
        for element in ['FOUND_SOLUTION', 'STATES_VISITED', 'PATH_LENGTH', 'TOTAL_COST', 'PATH']:
            expected_lines.append(f"[{element}]: {fields[element]['value']}")
    return '\n'.join(expected_lines)


def parse_output(output, correct_output=False, task=None):
    output_lines = output.split('\n')
    subtask_output = {}

    for line in output_lines:
        if line.startswith('# '):
            subtask = line.strip().split()[1].upper()
        elif line.startswith('['):
            if line.startswith('[CONDITION]:'):
                if 'CONDITIONS' not in subtask_output:
                    subtask_output['CONDITIONS'] = {'value': []}
                    if correct_output:
                        subtask_output['CONDITIONS']['match'] = 'contained'
                subtask_output['CONDITIONS']['value'].append(' '.join(line.strip().split()[1:]))
            else:
                field = line.strip().split()[0][1:-2]
                subtask_output[field] = {'value': []}
                if correct_output:
                    if field in ['PATH', 'PATH_LENGTH', 'STATES_VISITED'] and subtask in ['UCS', 'A-STAR']:
                        subtask_output[field]['match'] = 'ignored'
                    else:
                        subtask_output[field]['match'] = 'exact'
                subtask_output[field]['value'] = ' '.join(line.strip().split()[1:])
        else:
            break

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
    log_file.write(f"\n== {subtask} ==\n")
    test_instances = report['evaluation_results'][subtask]
    passed_tests = sum(i['test_passed'] for i in test_instances)
    log_file.write(f"  Passed {passed_tests} / {len(test_instances)} tests.\n")
    total_tests += len(test_instances)
    total_passed += passed_tests

    if verbose:  # logged in a separate file for each student with detailed info about failed tests
      for i in test_instances:
        if not i['test_passed']:
          log_file.write(f"\n- Failed test: {i['test_name']}\n")
          log_file.write(f"- Command run: {i['command']}\n")

          if not i['execute']:
            log_file.write(f"Execution failed with error:\n{i['output']}\n")
          elif not i['timeout']:
            log_file.write("Execution timed out.\n")
          else:
            mismatched_fields = [field for field in i['field_results'] if not i['field_results'][field]['match']]
            for mis_field in mismatched_fields:
              log_file.write(f"Mismatch with field: {mis_field}\n")
              log_file.write("-> Obtained output:\n")
              if isinstance(i['field_results'][mis_field]['obtained'], set):
                log_file.write('\n'.join(i['field_results'][mis_field]['obtained']))
              else:
                log_file.write(i['field_results'][mis_field]['obtained'])
              log_file.write(f"\n-> Expected output:\n")
              if isinstance(i['field_results'][mis_field]['expected'], set):
                log_file.write('\n'.join(i['field_results'][mis_field]['expected']))
              else:
                log_file.write(i['field_results'][mis_field]['expected'])
              log_file.write('\n')
            log_file.write("-> Complete obtained output:\n")
            if len(i['output'].split('\n')) <= 20:
              log_file.write(i['output'] + '\n')
            else:
              first_part = '\n'.join(i['output'].split('\n')[:10])
              last_part = '\n'.join(i['output'].split('\n')[-10:])
              log_file.write(f"{first_part}\n...\n{last_part}\n")
            log_file.write('-> Complete expected output:\n')
            if len(i['expected_output'].split('\n')) <= 20:
              log_file.write(i['expected_output'] + '\n')
            else:
              first_part = '\n'.join(i['expected_output'].split('\n')[:10])
              last_part = '\n'.join(i['expected_output'].split('\n')[-10:])
              log_file.write(f"{first_part}\n...\n{last_part}\n")
  log_file.write("\n=== TOTAL RESULTS ===\n")
  log_file.write(f"{total_passed} / {total_tests} tests passed. ({total_passed * 100. / total_tests:.2f}%)\n\n")