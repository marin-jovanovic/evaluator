import os

pokreni_prvi = "./lab1clion"    #moje rjesenje, javite ak je krivo haha
pokreni_drugi = "./lab1clion"   #naredba za pokretanje rjesenja koje se testira

tests_start = 1
tests_end = 2000

def check_whole_files():
    if open('sol1.txt').read() != open('sol2.txt').read():
        print('Wrong Answer')
        exit(0)

def check_only_cost():
    file1 = open('sol1.txt').read()
    file2 = open('sol2.txt').read()

    file1_sol = -1.0
    for line in file1:
        if line.startswith("[TOTAL_COST]:"):
            file1_sol = float(line[len("[TOTAL_COST]:"):])

    for line in file2:
        if line.startswith("[TOTAL_COST]:"):
            file2_sol = float(line[len("[TOTAL_COST]:"):])

    if(file1 != file2):
        print("Wrong Answer")
        exit(0)

for test_index in range(tests_start, tests_end + 1):

    os.system(f"{pokreni_prvi} --alg bfs --ss lab1_maps/{test_index}.txt > sol1.txt")

    os.system(f"{pokreni_drugi} --alg bfs --ss lab1_maps/{test_index}.txt > sol2.txt")

    check_whole_files()

    os.system(f"{pokreni_prvi} --alg ucs --ss lab1_maps/{test_index}.txt > sol1.txt")

    os.system(f"{pokreni_drugi} --alg ucs --ss lab1_maps/{test_index}.txt > sol2.txt")

    check_only_cost()



    for sufix in ["exact", "random", "constant-minus", "constant-plus", "lower", "upper"]:

        os.system(f"{pokreni_prvi} --alg astar --ss lab1_maps/{test_index}.txt --h lab1_maps/{test_index}-{sufix}.txt > sol1.txt")

        os.system(f"{pokreni_drugi} --alg astar --ss lab1_maps/{test_index}.txt --h lab1_maps/{test_index}-{sufix}.txt > sol2.txt")

        check_only_cost()

        # os.system(f"{pokreni_prvi} --ss lab1_maps/{test_index}.txt --h lab1_maps/{test_index}-{sufix}.txt --check-optimistic > sol1.txt")
        #
        # os.system(f"{pokreni_drugi} --ss lab1_maps/{test_index}.txt --h lab1_maps/{test_index}-{sufix}.txt --check-optimistic > sol2.txt")
        #
        # check_whole_files()

        # os.system(f"{pokreni_prvi} --ss lab1_maps/{test_index}.txt --h lab1_maps/{test_index}-{sufix}.txt --check-consistent > sol1.txt")
        #
        # os.system(f"{pokreni_drugi} --ss lab1_maps/{test_index}.txt --h lab1_maps/{test_index}-{sufix}.txt --check-consistent > sol2.txt")
        #
        # check_whole_files()

        continue

    print(f"[{test_index}/{tests_end}] OK!")