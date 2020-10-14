'''
Script to convert invalid input names to compliant ASCII names. Uses a random
hex string for file name.
'''
import argparse, unicodedata, random
import numpy as np

def convert_lines(line_arr, filter=False):
    if filter and "k__unidentified" in line_arr[0]:
        return ""
    else:
        return F"{unicodedata.normalize('NFKD', line_arr[0]).encode('ASCII', 'ignore').decode().replace(' ', '_')}{line_arr[1]}"

convert_lines_vec = np.vectorize(convert_lines)

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, help="database file")
parser.add_argument("-n", "--name", type=str, default="", help="output name")
parser.add_argument("-f", "--filter", type=bool, nargs='?', const=True, default=False, help="filter unidentified taxa")
args = parser.parse_args()

rec_dict={}
with open(args.input, "r", encoding='utf-8') as ifile:
    line = ifile.readline()
        while line != "":
            header = line
            line = ifile.readline()
            seq = ""
            while line != "" and line[0] != ">":
                seq = F"{seq}{line}"
                line = ifile.readline()
            rec_dict[header] = seq

if args.name == "":
    name = F"formatted_inputs_{'%06x' % random.randrange(16**6)}.fasta"
    print(name)
else:
    name = args.name
rec_array = np.array(list(rec_dict.items()))
rec_hash = {}
for i in range(rec_array.shape[0]):
    rec_hash[i] = convert_lines(rec_array[i], filter=args.filter)

buffer = "".join(hash.values())
with open(name, "w") as ofile:
    ofile.write(buffer)
