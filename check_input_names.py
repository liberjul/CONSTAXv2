'''
Script to convert invalid input names to compliant ASCII names. Uses a random
hex string for file name.
'''
import argparse, unicodedata, random
import numpy as np

def convert_lines(line):
    if line[0] == ">":
        return unicodedata.normalize('NFKD', line).encode('ASCII', 'ignore').decode().replace(" ", "_")
    else:
        return line

convert_lines_vec = np.vectorize(convert_lines)

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, help="database file")
parser.add_argument("-n", "--name", type=str, default="", help="output name")
parser.add_argument("-f", "--filter", type=bool, nargs='?', const=True, default=False, help="filter unidentified taxa")
args = parser.parse_args()

buffer = ""
with open(args.input, "r") as ifile:
    lines = np.array(ifile.readlines())
    lines_normalized = convert_lines_vec(lines)


if args.name == "":
    name = F"formatted_inputs_{'%06x' % random.randrange(16**6)}.fasta"
    print(name)
else:
    name = args.name
with open(name, "w") as ofile:
    if args.filter:
        head, seq = "",""
        for line in lines_normalized:
            if line[0] == ">":
                if "k__unidentified" not in head:
                     buffer = F"{buffer}{head}{seq}"
                head = line
                seq = ""
            else:
                seq = F"{seq}{line}"
        if "k__unidentified" not in head:
             buffer = F"{buffer}{head}{seq}"
    else:
        buffer = "".join(lines_normalized)
    ofile.write(buffer)
