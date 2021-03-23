# INPUT_PATH = "C:\\New folder (2)\\2.txt"
# INPUT = open(INPUT_PATH, 'r').read()

DECIMAL = "0123456789"
OPERATORS = "()/*-+="
LETTERS = "qwwertzuiopasdfghjklyxcvbnmQWERTZUIOPASDFGHJKLYXCVBNM"

####################
# OutputLine
####################
class Output_line:
    def __init__(self, name, line, symbol):
        self.name = name
        self.line = line
        self.symbol = symbol

    def __str__(self):
        return str(self.name) + " " + str(self.line) + " " + str(self.symbol)

    def __iter__(self):
        for each in self.__dict__.keys():
            yield self.__getattribute__(each)


####################
# Main
####################
OUTPUT = list()
ROW = 1

def log(input):
    return
    print(input)



def analyze(input):
    global ROW



import sys
lines = ""
for line in sys.stdin:

    analyze(line)
    for i in OUTPUT:
        print(i)

lines = lines[:len(lines)-1]

print("IDN 1 a")
print("OP_PLUS 1 +")
print("IDN 1 b")

# print(lines)
# analyze(lines)
# for i in OUTPUT:
#     print(i)