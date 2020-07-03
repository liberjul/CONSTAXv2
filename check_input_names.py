import argparse, unicodedata
import numpy as np

def convert_lines(line):
    if line[0] == ">":
        return unicodedata.normalize('NFKD', line).encode('ASCII', 'ignore').decode()
    else:
        return line

convert_lines_vec = np.vectorize(convert_lines)

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, help="database file")
args = parser.parse_args()

buffer = ""
with open(args.input, "r") as ifile:
    lines = np.array(ifile.readlines())
    lines_normalized = convert_lines_vec(lines)
    buffer = "".join(lines_normalized)

with open("formatted_inputs.fasta", "w") as ofile:
    ofile.write(buffer)
