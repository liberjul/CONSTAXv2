#!/usr/bin/env python

'''
Splits the formatted input/query FASTA into 100 sequence file to
work around BLAST getting stuck on 0 hit queries, where the
0 hit query is proceeded by >100 seqs.
'''
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, help="input query file")
args = parser.parse_args()

buffer = ""
total_rec_count = 0
file_rec_count = 0
file_count = 0
prefix = args.input.split(".fasta")[0]
print("Input FASTA: ", args.input)
with open(args.input, "r") as ifile:
    line = ifile.readline()
    while line != "":
        header = line
        line = ifile.readline()
        seq = ""
        while line != "" and line[0] != ">":
            seq += line.strip()
            line = ifile.readline()
        buffer += F"{header}{seq}\n"
        total_rec_count += 1
        file_rec_count += 1
        if file_rec_count > 99:
            file_rec_count = 0
            with open(F"{prefix}_{file_count:04d}.fasta", "w") as ofile:
                ofile.write(buffer)
            file_count += 1
            buffer = ""
    if buffer != "":
        with open(F"{prefix}_{file_count:04d}.fasta", "w") as ofile:
            ofile.write(buffer)
