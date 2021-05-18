"""
sos

    # check if starting clauses are consistent
    #   true for one or more interpretations
    # not needed (Zoran Medic)

    sos
        negated target + new clauses

    sos strategy
        at least one of clauses from sos

deletion strategy

    https://www3.cs.stonybrook.edu/~cse352/L17ResolutionPart3.pdf

"""

import bisect
import sys

# not operator
TILDA = "~"


def load_clauses(auxiliary_raw, support_raw):
    """
    handling:
        1. comments and empty lines
        2. tautology in support

    """

    # if clause is unknown only this will be printed
    print_buffer_for_unknown = []

    # line index
    index = 1

    # for printing
    auxiliary_dict = {}
    auxiliary = []

    for line in auxiliary_raw:
        print_buffer_for_unknown.append(str(index) + ". " + line.lower())

        # create formatted clause, sorted tuples
        line_formatted = []

        # create clause
        # handle A v A ...
        # todo tautology check

        for t_raw in line.lower().split(" v "):
            # is positive
            i_p = True

            # neg atom manager
            if t_raw.startswith(TILDA):
                t_raw = t_raw[1:]
                i_p = False

            bisect.insort(line_formatted, (t_raw, i_p))

        if line_formatted not in auxiliary:
            auxiliary.append(line_formatted)

            auxiliary_dict[str(line_formatted)] = (index, None, None)
            index += 1

    """
    support

    handles
        1. tautology => print true and break
        2. multiple same values A v A ... => A v ...
    """
    support = []

    c_dict = {}

    for t in support_raw.split(" v "):
        # is positive
        i_p = False

        if t.startswith(TILDA):
            t = t[1:]

            # invert
            i_p = True

        print_buffer_for_unknown.append(
            str(index) + ". " + ("" if i_p else TILDA)
            + t.lower())

        if t in c_dict and c_dict.get(t) == i_p:
            # handler: A v A ...
            # same val
            # no need to add
            continue

        c_dict[t] = i_p

        auxiliary_dict[str([(t, i_p)])] = (index, None, None)
        index += 1

        # support
        bisect.insort(support, [(t, i_p)])

    # optimization
    auxiliary = d_same_states_in_c(auxiliary)
    auxiliary = d_tautology(auxiliary)
    auxiliary = d_same_clauses(auxiliary)

    aux_d_unit_resolution(auxiliary)

    support = d_same_states_in_c(support)
    support = d_tautology(support)
    support = d_same_clauses(support)

    init_d_unit_resolution(auxiliary, support)

    return auxiliary, support, auxiliary_dict, index, print_buffer_for_unknown


# todo check wit hempty file


def p_formatted(d, conclusion, last_line, print_buffer_for_unknown,
                print_if_unknown):
    """"
    d - log
    conclusion - True or False
    last_line - for printing
    """

    # check true or unknown
    if conclusion:

        """get nums for auxiliary and support that are used"""

        vals = {v[0]: (v[1], v[2]) for k, v in d.items() if
                v[1] is not None and v[2] is not None}

        to_do = [d.get("[]")]

        sup_print = [to_do[0][0]]
        aux_print = []

        while to_do:
            c = to_do.pop()

            l_p = c[1]
            r_p = c[2]

            for i in (l_p, r_p):

                if i not in vals:
                    if i not in aux_print:
                        bisect.insort(aux_print, i)

                elif i not in sup_print:

                    bisect.insort(sup_print, i)

                    if i in vals:
                        n = vals.get(i)

                        to_do.append([i, n[0], n[1]])

        """assign correct index"""

        correct_i = 1

        correct_dict = {}

        aux_ordered_to_print = {}
        sup_ordered_to_print = {}

        for k, v in d.items():
            row = v[0]

            if row in aux_print:
                correct_dict[row] = correct_i
                correct_i += 1
                aux_ordered_to_print[row] = p_line(k, v)

            elif row in sup_print:
                correct_dict[row] = correct_i
                correct_i += 1
                sup_ordered_to_print[row] = p_line(k, v)

        # todo comments in cooking
        # todo check if aux contains not needed clauses

        for i, data in aux_ordered_to_print.items():
            wrong_i = data[0]
            print("{}. {}".format(correct_dict.get(wrong_i), data[1]))

        print("===============")

        for i, data in sup_ordered_to_print.items():
            wrong_i = data[0]

            l = correct_dict.get(data[2])
            r = correct_dict.get(data[3])

            print("{}. {} ({}, {})".format(correct_dict.get(wrong_i),
                                           data[1], l, r))

        print("===============")
        print("[CONCLUSION]: {} is true".format(last_line))

    else:
        if print_if_unknown:
            [print(i) for i in print_buffer_for_unknown]
            print("===============")

        print("[CONCLUSION]: {} is unknown".format(last_line))


def p_line(k, v):
    c_i = v[0]
    l = v[1]
    r = v[2]

    if l and r:
        if l > r:
            l, r = r, l

    exp = ""

    if k == "[]":
        return [c_i, "NIL", l, r]

    for atom, value in eval(k):
        exp += ("" if value else TILDA) + atom + " v "

    exp = exp[:-3]

    # if no parents -> auxiliary
    if not l and not r:
        return [c_i, exp, None, None]

    else:
        return [c_i, exp, l, r]


def main():
    direction_f = None
    clauses_path = None
    instructions_path = None

    for i, arg in enumerate(sys.argv):

        if arg not in ["resolution", "cooking"]:
            continue

        direction_f = arg
        clauses_path = sys.argv[i + 1]

        if direction_f == "cooking":
            instructions_path = sys.argv[i + 2]

        break

    # direction_f = "cooking"
    # direction_f = "resolution"
    # clauses_path = "C:/git/artificial-intelligence/lab2/empty.txt"
    # clauses_path = "../../../../lab2_files/cooking_chicken_broccoli_alfredo_big.txt"
    # instructions_path = "../../../../lab2_files/cooking_chicken_broccoli_alfredo_big_input.txt"

    input_lines = [i for i in open(r"{}".format(clauses_path), encoding="utf-8")
        .read().lower().strip().split("\n")
                   if not (i.startswith("#") or i.isspace() or not i)]

    # if not input_lines:
    #     print("empty file")
    #     sys.exit()

    if direction_f == "resolution":
        to_test = input_lines.pop()

        auxiliary, support, temp_dict, ind, print_buffer_for_unknown = \
            load_clauses(input_lines, to_test)

        pl_resolve(auxiliary, support, to_test, temp_dict, ind,
                   print_buffer_for_unknown)

    if direction_f == "cooking":
        print("Constructed with knowledge:")
        [print(i) for i in input_lines]
        print()

        for line in open(r"{}".format(instructions_path),
                         encoding="utf-8").read().lower().strip().split("\n"):

            if line.startswith("#") or line.isspace() or not line:
                continue

            print("User’s command:", line.lower())

            data = line[:-2].lower()
            flag = line[-1]

            if flag == "?":

                auxiliary, support, temp_dict, ind, print_buffer_for_unknown = \
                    load_clauses(input_lines, data)

                pl_resolve(auxiliary, support, data, temp_dict, ind,
                           print_buffer_for_unknown, False)
                print()

            elif flag == "+":

                if data not in input_lines:
                    input_lines.append(data)

                print("Added", data)
                print()

            elif flag == "-":

                if data in input_lines:
                    while input_lines.__contains__(data):
                        input_lines.remove(data)

                print("removed", data)
                print()


def pl_resolve(auxiliary, support, testing_exp, new_dict, index,
               print_buffer_for_unknown, print_if_unknown=True):
    while True:

        new_clauses = []

        for i_1, c_1 in enumerate(support):

            for i_2, c_2 in enumerate(auxiliary + support):

                if c_1 == c_2:
                    # two equal clauses

                    if c_2 in auxiliary:
                        auxiliary.remove(c_2)

                    continue

                # check if this two clauses can be matched
                for i in c_1:
                    for j in c_2:

                        # same atoms, diff values
                        if i[0] == j[0] and i[1] != j[1]:

                            # make new clause
                            clause = c_1 + c_2

                            # remove same atoms
                            clause = sorted(set(clause))

                            # control map
                            c_map = {}
                            how_many = 0

                            for t in clause:

                                name = t[0]
                                val = t[1]

                                # check for {A v ~A v ...} and flag every A
                                if name not in c_map:
                                    c_map[name] = val

                                else:
                                    if c_map.get(name) != val:
                                        how_many += 1
                                        elem_to_remove = name

                            if how_many == 1:
                                # not tautology

                                clause.remove((elem_to_remove, True))
                                clause.remove((elem_to_remove, False))

                                if str(sorted(clause)) not in new_dict:
                                    l = new_dict.get(str(sorted(c_1)))[0]
                                    r = new_dict.get(str(sorted(c_2)))[0]

                                    new_dict[str(sorted(clause))] = [index, l,
                                                                     r]
                                    index += 1

                                # check for NIL
                                if not clause:
                                    p_formatted(new_dict, True, testing_exp,
                                                print_buffer_for_unknown,
                                                print_if_unknown)
                                    return

                                if clause not in (support + new_clauses):
                                    new_clauses.append(clause)

        # not adding
        #   tautology
        #   same clauses that are already in support
        global_d_unit_resolution(auxiliary, support, new_clauses)

        for i in new_clauses:
            bisect.insort(support, i)

        if not new_clauses:
            p_formatted(new_dict, False, testing_exp, print_buffer_for_unknown,
                        print_if_unknown)
            return


def is_tautology(clause):
    # control map
    c_map = {}

    for t in clause:
        name = t[0]
        val = t[1]

        if name not in c_map:
            c_map[name] = val

        elif c_map.get(name) != val:
            return True

    return False


def d_tautology(clauses):
    """
     remove all A v ~A v ...
     """

    return [i for _, i in enumerate(clauses) if not is_tautology(i)]


def aux_d_unit_resolution(auxiliary):
    """
    same as d_unit_resolution but only for aux
    """

    for clause in auxiliary:
        for other in auxiliary:
            if set(clause) <= set(other) and clause != other:
                auxiliary.remove(other)


def init_d_unit_resolution(auxiliary, support):
    for clause in support:

        for other in auxiliary:
            if clause == other or set(clause) <= set(other):
                auxiliary.remove(other)

        for other in support:
            if set(clause) <= set(other) and clause != other:
                support.remove(other)


def global_d_unit_resolution(auxiliary, support, new_cl):
    """
    1 a b
    2 a
    3 a b c

    remove 1 because of 2
    remove 3 because of 2
    """

    for clause in new_cl:
        for other in auxiliary:
            if clause == other or set(clause) <= set(other):
                auxiliary.remove(other)

    for clause in new_cl:
        for other in support:
            if set(clause) <= set(other):
                support.remove(other)

            elif set(other) <= set(clause):
                new_cl.remove(clause)
                break


def d_same_clauses(clauses):
    """
    1. A v B
    2. A v B
    removes 2.
    """

    return [i for n, i in enumerate(clauses) if i not in clauses[:n]]


def d_same_states_in_c(clauses):
    """
    A v A v B v B => A v B
    """

    return [list(set(c)) for c in clauses]


if __name__ == '__main__':
    main()
