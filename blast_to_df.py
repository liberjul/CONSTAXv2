'''
For this type of blast command:
blastn -query <query> -db Unite_04_02_2020 -num_threads 16 -outfmt "7 qacc sacc evalue bitscore pident qcovs" -max_target_seqs 20 > <output>
'''

import sys, argparse, os

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--in_file", type=str, help="blastn output file")
parser.add_argument("-o", "--out_file", type=str, help="Output file for classifications")
parser.add_argument("-d", "--db", type=str, help="database file")
parser.add_argument("-t", "--tf", type=str, help="training files path")
parser.add_argument("-f", "--format", type=str, help="database format")
args = parser.parse_args()

filename = args.db
filename_base = args.tf + "/" + ".".join(os.path.basename(filename).split(".")[:-1])

taxa_dict = {}
with open(filename_base + "__RDP_taxonomy_headers.txt", "r") as f_heads:
    line = f_heads.readline()
    while line != "":
        acc, taxa = line[1:].strip().split("\t")
        taxa = taxa.split(";")[1:]
        taxa = ",".join(taxa)
        taxa_dict[acc] = taxa
        line = f_heads.readline()


with open(args.in_file, "r") as ifile:
    header_line = open(filename_base + "__RDP_taxonomy.txt", "r").readline()
    ranks = header_line.strip().split("\t")[1:]
    ranks[0] = ranks[0].replace("Kingdom", "Domain")
    with open(args.out_file, "w") as ofile:
        ofile.write(F"query,subject,bitscore,e_value,percent_identity,query_coverage,{','.join(ranks)}\n")
    line = ifile.readline()
    rec_count = 0
    while line != "":
        buffer = ""
        while line != "" and rec_count < 10000:
            if "# Query: " in line: # Checking if hits were found
                quer = line.strip().split("Query: ")[1]
                line = ifile.readline()
                line = ifile.readline()
                if line == "# 0 hits found\n": # If no hits found
                    buffer = F"{buffer}{quer},{'__'},{1},{0},{0.0},{0},{','.join(['unidentified']*len(ranks))}\n" # Add dummy row to be cut out later
            elif line[0] != "#" and line != "\n": # BLAST hit lines
                spl = line.strip().split("\t")
                sub = spl[1]
                eval, bitscore, id, qcov = spl[2:]
                buffer = F"{buffer}{spl[0]},{sub},{bitscore},{eval},{id},{qcov},"
                buffer = F"{buffer}{taxa_dict[sub]}\n"
            line = ifile.readline()
            rec_count += 1
        rec_count = 0
        with open(args.out_file, "a+") as ofile:
            ofile.write(buffer)
