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
args = parser.parse_args()

buffer = ""
with open(args.input, "r") as ifile:
    lines = np.array(ifile.readlines())
    lines_normalized = convert_lines_vec(lines)
    buffer = "".join(lines_normalized)

if args.name == "":
    name = F"formatted_inputs_{'%06x' % random.randrange(16**6)}.fasta"
    print(name)
else:
    name = args.name
with open(name, "w") as ofile:
    ofile.write(buffer)
