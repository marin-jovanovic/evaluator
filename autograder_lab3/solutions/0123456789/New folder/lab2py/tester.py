lines = open("../../../../correct_solution.log").read().split("\n\n")

print(lines)

for chunk in lines:
    # print(chunk)

    for l in chunk.split("\n"):
        # print(l)

        if l.startswith("- Passed test:"):
            # print("input", l)

            l = l.replace("- Passed test: ", "")
            print("input", l)



    # print("++++++++++++++++++++++++++++++++++++++++++++++")

# for l in lines:
#     print(l)

# print(lines)

# for l in lines:
#     l = l[:-1]
#     print(l)