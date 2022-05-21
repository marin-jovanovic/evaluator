"""
features
header
    first row
    +-------+--------------+--------------+-------------------+
    |  x    | feature      | feature      |    class label    |
    +-------+--------------+--------------+-------------------+
other rows
    +-------+--------------+--------------+-------------------+
    | row 1 | value        | value        | class label value |
    | row 2 | value        | value        | class label value |
    +-------+--------------+--------------+-------------------+
class label
    target variable
"""
import bisect
import sys
from collections import defaultdict
from math import log2


# fixme lowercase


class ID3():
    """main alg class"""

    def ID3(self):
        """constructor"""

    @staticmethod
    def construct_input_data(input_path):
        """
        matrix = [
            [[val1, val2], no]
        ]
        """

        matrix = []

        all_class_label_values = []

        with open(r"{}".format(input_path), encoding="utf-8") as f:
            features = f.readline().strip().split(",")
            class_label = features.pop()

            for line in f:
                feature_values = line.strip().split(",")
                class_label_value = feature_values.pop()

                matrix.append([feature_values, class_label_value])

                if class_label_value not in all_class_label_values:
                    bisect.insort(all_class_label_values, class_label_value)

        return features, matrix, all_class_label_values, class_label

    @staticmethod
    def load_input_data(matrix, keys):
        results = defaultdict(int)
        master_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

        for line, endpoint in matrix:

            results[endpoint] += 1

            for i, result_for_i in enumerate(line):
                master_dict[keys[i]][result_for_i][endpoint] += 1

        return master_dict, results

    @staticmethod
    def get_entropy(vals):
        """
        return -sum(vals[i]/ sum(vals) * log2(vals[i] / sum(vals)))
        :param vals: []
        :return: float
        """

        denominator = sum(vals)

        r = 0
        for i in vals:
            if i == 0:
                continue

            i = i / denominator

            r -= i * log2(i)

        return r

    @staticmethod
    def calculate_information_gain(master_dict, len_matrix, result_log):
        """
        return max(IG)
        IG = [
            entropy(D) - sum(len(Dx=v) / len(D) * entropy(Dx=v))
        ]
        :param master_dict: {
            weather : {
                sunny: {
                    no: 3,
                    yes: 2,
                },
            },
        }
        :param len_matrix: sum of all code{yes} and code{no}
        :param result_log: {yes: 5, no: 9}
        """

        entropy = ID3.get_entropy(result_log.values())

        # name -> val
        ig_log = {}

        for feature, value in master_dict.items():

            total_r = entropy

            for k_1, val_1 in value.items():
                v_extr = val_1.values()
                total_r -= sum(v_extr) / len_matrix * ID3.get_entropy(v_extr)

            ig_log[feature] = total_r

        name, _ = ID3.get_max_freq(ig_log)
        return name

    @staticmethod
    def dec_driver_false(curr_ast):
        """
        1:Vrijeme=suncano 2:Temp=srednja 3:Vjetar=slab ('ne', {'ne': 100,})
        1:Vrijeme=suncano 2:Temp=visoka ('da', {'da': 2,})
        1:Vrijeme=suncano 2:Temp=visoka ('da', {'ne': 2, 'da':2,})
        za slucaj kad je Temp=vlazno idemo u "ne"
        """

        ret = defaultdict(int)

        for feature, val in curr_ast.items():

            if isinstance(val, dict):
                new_vals = ID3.dec_driver_false(val)

                for k, v in new_vals.items():
                    ret[k] += v

            else:
                for k, v in val[1].items():
                    ret[k] += v

        return ret

    @staticmethod
    def decision_driver(curr_ast, our_input_to_test):
        for feature, val in curr_ast.items():

            if feature in our_input_to_test:

                new_ast = val

                if isinstance(new_ast, dict):
                    our_input_to_test.remove(feature)
                    return ID3.decision_driver(new_ast, our_input_to_test)

                else:
                    return val[0]

        # not in curr_ast
        # calc occurrence of targets by (occurrence, alphabet)

        r = ID3.dec_driver_false(curr_ast)

        name, _ = ID3.get_max_freq(r)
        return name

    @staticmethod
    def predict(tests_path, decision_tree):
        lines = []
        with open(r"{}".format(tests_path), encoding="utf-8") as f:
            for l in f:
                lines.append(l.strip())

        keys = lines[0].split(",")[:-1]

        # buffer for printing
        p_line = ""

        num_of_test = 0
        num_of_passing_tests = 0

        # class label values to print in c matrix
        all_out = []

        # add all expected class label values
        for l in lines[1:]:
            out_exp = l.split(",")[-1]
            if out_exp not in all_out:
                bisect.insort(all_out, out_exp)

        # not for printing, just for logging
        confusion_matrix = defaultdict(lambda: defaultdict(int))

        # map expected to obtained output
        # calculate num of tests
        # calculate num of passing tests
        # complete {all_out}
        for line in lines[1:]:
            line = line.strip().split(",")

            expected_out = line.pop()

            obtained_out = ID3.decision_driver(decision_tree,
                                           set(a + "=" + b for a, b in zip(keys, line)))

            if obtained_out not in all_out:
                bisect.insort(all_out, obtained_out)

            confusion_matrix[expected_out][obtained_out] += 1

            num_of_test += 1
            if expected_out == obtained_out:
                num_of_passing_tests += 1

            p_line += " " + obtained_out

        print("[PREDICTIONS]:" + p_line)

        print("[ACCURACY]: {:0.5f}".format(num_of_passing_tests / num_of_test))

        print("[CONFUSION_MATRIX]:")

        new_m = defaultdict(lambda: defaultdict(int))

        # setup dimensions
        for i in all_out:
            for j in all_out:
                new_m[i][j] = 0

        # add entries
        for k, v in confusion_matrix.items():
            if k in new_m:
                for k_2, v_2 in v.items():
                    if k_2 in new_m[k]:
                        new_m[k][k_2] = v_2

        # print
        for k, v in new_m.items():
            t = ""

            for k_2, v_2 in v.items():
                t += str(v_2) + " "

            print(t[:-1])

    @staticmethod
    def argmax_ig(oznaceni_primjeri, kljucevi):
        """ideja ovog je da vrati element po kojem je najbolje podijelit skup"""

        data, result_log = ID3.load_input_data(oznaceni_primjeri, kljucevi)

        where_to_go = ID3.calculate_information_gain(data, len(oznaceni_primjeri), result_log)

        return where_to_go

    @staticmethod
    def get_max_freq(d_map):
        # print(d_map)
        return sorted(d_map.items(), key=lambda x: (-x[1], x[0]))[0]

        # rjeseno
        # nadi max vrijednost, abeceda
        max_var_name = None
        max_occurance_num = 0

        for k, v in d_map.items():
            if not max_var_name:
                max_var_name = k
                max_occurance_num = v

            elif max_occurance_num < v:
                max_var_name = k
                max_occurance_num = v

            elif max_occurance_num == v:
                max_var_name = min(max_var_name, k)

        return max_var_name, max_occurance_num

    @staticmethod
    def kolko_je_najcescih(oznaceni_primjeri):
        d_map = defaultdict(int)

        for primjer in oznaceni_primjeri:
            d_map[primjer[1]] += 1

        _, count = ID3.get_max_freq(d_map)
        return count

    @staticmethod
    def big_v(small_x, keys, matrix):
        where_to_go = small_x

        index_to_del = keys.index(where_to_go)

        new_keys = keys[:]
        new_keys.pop(index_to_del)

        separated_matrices = defaultdict(list)
        new_total_rows = defaultdict(int)

        for i in matrix:
            line = i[0][:]
            del_val = line.pop(index_to_del)

            separated_matrices[del_val].append([line, i[1]])

            new_total_rows[del_val] += 1

        return new_keys, separated_matrices

    @staticmethod
    def argmax_v(oznaceni_primjeri):
        # ime ciljne var -> kolicina
        d_map = defaultdict(int)

        for primjer in oznaceni_primjeri:
            d_map[primjer[1]] += 1

        name, count = ID3.get_max_freq(d_map)
        # return name, {name: count,}
        return name, d_map

    @staticmethod
    def fit(curr_train_set, parent_train_set, big_x, starting_map, depth, is_depth_present):
        ast = {}
        """
        :param small_d: skup oznacenih primjera
        :param d_parent:
        :param big_x: skup svih keyeva
        :return:
        """

        # pogledaj sta je najcesce u skupu oznacenih primjera d_parent

        # ako je prazan trenutni skup oznacenih primjera
        if not curr_train_set:
            # najcesca oznaka u nadcvoru
            return ID3.argmax_v(parent_train_set)

        # recursion limit
        if is_depth_present and depth <= 0:
            return ID3.argmax_v(curr_train_set)

        # pogledaj sta je najcesce u skupu oznacenih primjera d
        if not big_x:
            print("aa")

            pass

        # pogledaj jel big_x sadrzi bilokoji x
        # ili jel ima smisla radit jos podskupova (vidi jel ovo odlicna klasifikacija)
        if not big_x or len(curr_train_set) == ID3.kolko_je_najcescih(curr_train_set):
            return ID3.argmax_v(curr_train_set)

        small_x = ID3.argmax_ig(curr_train_set, big_x)

        big_x, carr = ID3.big_v(small_x, big_x, curr_train_set)

        for v in starting_map[small_x]:
            small_t = ID3.fit(
                [] if v not in carr else carr[v],
                curr_train_set,
                big_x,
                starting_map,
                depth - 1,
                is_depth_present
            )

            ast[small_x + "=" + v] = small_t

        return ast

    @staticmethod
    def get_dict_paths(vals, path="", index=1, paths=[]):
        """
        construct tree for printing
        """

        for k, v in vals.items():
            temp = path + str(index) + ":" + k + " "

            if isinstance(v, dict):
                ID3.get_dict_paths(v, temp, index + 1, paths)

            else:
                paths.append(temp + v[0])

        return paths


def main():
    train_path = sys.argv[1]
    test_path = sys.argv[2]

    depth = 9999
    is_depth_present = False
    if len(sys.argv) >= 4:
        is_depth_present = True
        depth = int(sys.argv[3])


    header, matrix, results, class_label = ID3.construct_input_data(train_path)

    # feature_name -> {value_1, value_2, value3, ...}
    feature_val = defaultdict(set)

    for i, h in enumerate(header):
        for m in matrix:
            feature_val[h].add(m[0][i])

    # accept processed data
    train_dataset = None
    test_dataset = None

    model = ID3()
    # construct model instance

    a = ID3.fit(matrix, matrix, header, feature_val, depth, is_depth_present)
    # model.fit(train_dataset)
    # learn the model
    print("[BRANCHES]:")
    [print(i) for i in ID3.get_dict_paths(a)]

    ID3.predict(test_path, a)
    # predictions = model.predict(test_dataset)
    # generate predictions on unseen data


if __name__ == '__main__':
    main()
