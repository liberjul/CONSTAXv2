# Written by Natalie Vande Pol
# November 15, 2017
#
# Command line: python MasterScript1.py
# Script will locate, import, and validate the database file specified
# Requires subscript_lineage2taxonomyTrain.py and subscript_fasta_addFullLineage.py
# be in the same directory
# Creates the following files in the input file location:
#  - a combined taxonomy and fasta database file compatible with the UTAX and
#    SINTAX classifiers
#  - fasta and taxonomy database files compatible with the RDP classifer
#  - training files for the RDP classifier
# Output files are named and located based on the input file



# -*- coding: utf-8 -*-
import sys, os, unicodedata, argparse, glob, time

def convert_utax_line(utax_taxa):
	r_lets = "dkpcofgs"
	new_taxa = []
	for i in range(min(len(utax_taxa), len(r_lets)) - 1):
		new_taxa.append(F"{r_lets[i]}:{utax_taxa[i]}")
	if utax_taxa[-1].count("_") > 1:
		new_taxa.append(F"{r_lets[-1]}:{utax_taxa[-1]}")
	else:
		new_taxa.append(F"{r_lets[min(len(utax_taxa), len(r_lets)) - 1]}:{utax_taxa[-1]}")
	return ",".join(new_taxa)
# sys.path.append("/opt/software/CONSTAX/2/")


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--db", type=str, help="database file")
parser.add_argument("-t", "--tf", type=str, help="training files path")
parser.add_argument("-f", "--format", type=str, help="database formatting")
parser.add_argument("-p", "--path", type=str, help="path to subscript imports")
args = parser.parse_args()

sys.path.append(args.path + "/")

print(F"Importing subscripts from {args.path}")

import subscript_lineage2taxonomyTrain, subscript_fasta_addFullLineage

# silva = "null"
filename = args.db
filename_base = args.tf + "/" + ".".join(os.path.basename(filename).split(".")[:-1])


print("\n____________________________________________________________________\nReformatting database\n")
start = time.process_time()

#RDP output files
fasta = open(filename_base+"__RDP.fasta","w")
taxon_fn = filename_base+"__RDP_taxonomy.txt"
taxon = open(taxon_fn,"w")
print(F"{args.format} format detected\n")
if args.format == "UNITE":
	#UTAX output file
	fastatax = open(filename_base+"__UTAX.fasta","w")

	taxon.write("Seq_ID\tKingdom\tPhylum\tClass\tOrder\tFamily\tGenus\tSpecies\n")

	num = 0
	with open(filename) as database:
		for line in database:
			if line[0] == ">":
				#correct umlauts or special letters
				ascii_line = unicodedata.normalize('NFKD', line).encode('ASCII', 'ignore')
				temp = ascii_line.decode()[1:].split("|")
				# unico_line = unicode(line, '1252')
				# ascii_line = unicodedata.normalize('NFKD', line).encode('ASCII', 'ignore')
				# temp = ascii_line[1:].split("|")

				#UTAX file
				utax_name = temp[1]+"|"+temp[2]
				utax_taxa = temp[4][1:].strip().replace("__",":").replace(";",",")
				temp_utax = utax_taxa.strip().split(",")
				# if temp_utax[0].endswith("Fungi"):
				temp_utax2 = [x for x in temp_utax if "unidentified" not in x]
				temp_utax3 = [y for y in temp_utax2 if "Incertae_sedis" not in y]
				temp_utax4 = [z for z in temp_utax3 if "unknown" not in z]
				if len(temp_utax4) == 0:
					continue
				new_utax_taxa = ",".join(temp_utax4)
				fastatax.write(">"+utax_name+";tax=d"+new_utax_taxa+";\n")

				#RDP files
				name = str(temp[1])
				temp2 = temp[4].strip().split("__")
				to_genus = [ item[:-2] for item in temp2[1:-1] ]

				if "Incertae_sedis" in to_genus:
					indices = [i for i,x in enumerate(to_genus) if x == "Incertae_sedis"]
					for j in indices:
						if "Incertae_sedis" not in to_genus[j-1]:
							to_genus[j] = str(to_genus[j-1])+"_Incertae_sedis"
						else:
							to_genus[j] = str(to_genus[j-1])
				if "unidentified" in to_genus:
					indices = [i for i,x in enumerate(to_genus) if x == "unidentified"]
					for j in indices:
						to_genus[j] = "-"

				if to_genus[0] != "-":
					species = str(temp2[-1])
					if "Incertae" in species:
						species = "unidentified_sp"
					elif to_genus[-1] not in species:
						temp=species.split("_")
						species = temp[0]+"_unidentified_"+temp[1]
					if species.endswith("sp"):
						species+= "_"+str(num)
						num += 1

				taxonomy = name+"\t"+"\t".join(to_genus)+"\t"+species+"\n"
				fasta.write(">"+name+"\n")
				taxon.write(taxonomy)
				seq = next(database)
				fastatax.write(seq)
				fasta.write(seq)
	fasta.close()
	taxon.close()

else:
	max_rank = 1
	with open(filename, "r") as database:
		line = database.readline()
		while line != "":
			t_list = line.strip().split(";")
			if len(t_list) > max_rank:
				max_rank = len(t_list)
			line = database.readline()
	taxon.write("Seq_ID\t" + "\t".join([F"Rank_{x}" for x in range(1, max_rank+1)]) + "\n")
	with open(filename, "r") as database:
		line = database.readline()
		while line != "":
			line = line.replace(" Bacteria;", "?Bacteria;").replace(" Eukaryota;", "?Eukaryota;").replace(" Archaea;", "?Archaea;").replace(" ", "_")
			ascii_line = unicodedata.normalize('NFKD', line).encode('ASCII', 'ignore')
			# temp = ascii_line.decode().replace("*", "_").replace("'", "").replace(",", "").replace("Oral_Taxon", "oral_taxon")[1:].split("?")
			temp = ascii_line.decode().translate(str.maketrans("*,<>", "_   ")).replace("Oral_Taxon", "oral_taxon").replace("'","")[1:].split("?")

			name = str(temp[0]).split(".")[0]
			t_list = temp[1].strip().split(";")

			# temp_utax1 = [x for x in t_list if "unidentified" not in x]
			# temp_utax2 = [y for y in temp_utax1 if "Incertae_sedis" not in y]
			# temp_utax3 = [z for z in temp_utax2 if "unknown" not in z]
			# new_utax_taxa = convert_utax_line(temp_utax3)
			# fastatax.write(">"+name+";tax="+new_utax_taxa+";\n")

			if "unidentified" in t_list:
				indices = [i for i,x in enumerate(t_list) if x == "unidentified"]
				non_unid = [i for i,x in enumerate(t_list) if x != "unidentified"]
				for j in indices:
					t_list[j] = "-"
				if t_list[-1] == "-": # if lowest rank in unidentified, add the lowest identified rank to the lowest taxa
				    t_list[-1] = t_list[non_unid[-1]] + "_unidentified"

			if len(t_list) < max_rank:
				t_list = t_list[:-1] + ["-"]*(max_rank - len(t_list)) + [t_list[-1]] # fill in missing ranks


			taxonomy = name+"\t"+"\t".join(t_list)+"\n"
			fasta.write(">"+name+"\n")
			taxon.write(taxonomy)
			line = database.readline()
			seq = ""
			while line != "" and line[0] != ">":
				seq += line.strip()
				line = database.readline()
			seq = seq.replace("U", "T")
			# fastatax.write(seq + "\n")
			fasta.write(seq + "\n")

	fasta.close()
	taxon.close()
	# fastatax.close()

print(F"Reference database FASTAs formatted in {time.process_time() - start} seconds...\n")

# with open("temp_db_file.txt", "w") as temp_file:
# 	with open(taxon_fn, "r") as ifile:
# 		line = ifile.readline()
# 		temp_file.write("Seq_ID\t" + "\t".join([F"Rank_{x}" for x in range(1, max_rank+1)]) + "\n")
# 		while line != "":
# 			temp_file.write(line)
# 			line = ifile.readline()
#
# os.system(F"cat temp_db_file.txt > {taxon_fn}")
os.system(F"rm {filename_base}__RDP_taxonomy_trained.txt 2> /dev/null")
os.system(F"rm {filename_base}__RDP_taxonomy_headers.txt 2> /dev/null")

subscript_lineage2taxonomyTrain.lin2tax(filename_base, args.format)
subscript_fasta_addFullLineage.addFullLineage(filename_base, args.format)

print("Database formatting complete\n____________________________________________________________________\n\n")
