import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, help="database file input")
parser.add_argument("-o", "--output", type=str, help="filtered fasta output")
parser.add_argument("-k", "--keyword", type=str, help="filter records to include keyword")
args = parser.parse_args()

rec_dict = {}
with open(args.input, "r") as ifile:
    line = ifile.readline()
    while line != "":
        header = line
        line = ifile.readline()
        seq = ""
        while line != "" and line[0] != ">":
            seq += line.strip()
            line = ifile.readline()
        rec_dict[header] = seq
with open(args.output, "w") as ofile:
    for rec in rec_dict.keys():
        if args.keyword in rec:
            ofile.write(F"{rec}{rec_dict[rec]}\n")
