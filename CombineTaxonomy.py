# Written by Natalie Vande Pol
# November 15, 2017
#
# Command line: python MasterScript2.py
# Script will locate the taxonomy file from each classifier and validate file
# Creates a taxonomy file in standardized format for each input file and
# generates a consensus taxonomy file based on the three input files
# Reformatted taxonomy files are named based on the input file
# All output files are placed in dedicated outputs folder



import sys, os, itertools, argparse
import pandas as pd

################################################################################
def reformat_RDP(rdp_file, output_dir, confidence, ranks):
	input = open(rdp_file)
	all_lines = input.readlines()
	input.close()

	output_file = F"{output_dir}/otu_taxonomy_rdp_final.txt"
	output = open(output_file,"w")

	if ranks[0] == "Kingdom":
		output.write("OTU_ID\tOTU_Score\tKingdom\tK_score\tPhylum\tP_score\tClass\tC_score")
		output.write("\tOrder\tO_score\tFamily\tF_score\tGenus\tG_score\tSpecies\tS_score\n")
	else:
		output.write("OTU_ID\tOTU_Score")
		for r in ranks:
			output.write(F"\t{r}\t{r.replace('ank_', '')}_score")
		output.write("\n")

	for i, line in enumerate(all_lines):
		# capture confidence level at genus before altering line
		temp = line.strip().split("\t")
		confi = temp[7:-2][::3]
		confi.append(temp[-1])
		taxon = temp[5:][::3]

		# remove any taxonomic levels after first "unidentified"
		j=0
		new_taxon = []
		while j<len(taxon):
			if	taxon[j].endswith("Incertae_sedis"):
				taxon[j] = "Incertae_sedis"
			if  "unidentified" in taxon[j] or float(confi[j])<confidence:
				del confi[j:]
				break
			else: new_taxon.append(taxon[j].capitalize())
			j+=1

		# remove "_sp" species classifications
		if ranks[0] == "Kingdom" and len(new_taxon)>0 and " sp" in new_taxon[-1]:
			del new_taxon[-1]
			del confi[-1]
		# remove terminal Incertae_sedis
		while len(new_taxon)>0 and "Incertae_sedis" in new_taxon[-1]:
			del new_taxon[-1]
			del confi[-1]


		if confi == []:
			score = "NA"
		else:
			score = confi[-1]
		tax_confi = ""
		for k in range(len(new_taxon)):
			tax_confi += F"\t{new_taxon[k]}\t{confi[k]}"

		# iters = [iter(new_taxon), iter(confi)]
		# tax_confi = list(str(it.next()) for it in itertools.cycle(iters))

		# output.write(temp[0]+"\t"+score+"\t"+"\t".join(tax_confi)+"\n")
		output.write(F"{temp[0]}\t{score}{tax_confi}\n")

	output.close()
	return output_file

################################################################################
def reformat_UTAX(utax_file, output_dir, confidence, ranks):
	input = open(utax_file)
	all_lines = input.readlines()
	input.close()

	output_file = F"{output_dir}/otu_taxonomy_utax_final.txt"
	output = open(output_file,"w")
	if ranks[0] == "Kingdom":
		output.write("OTU_ID\tOTU_Score\tKingdom\tK_score\tPhylum\tP_score\tClass\tC_score")
		output.write("\tOrder\tO_score\tFamily\tF_score\tGenus\tG_score\tSpecies\tS_score\n")
	else:
		output.write("OTU_ID\tOTU_Score")
		for r in ranks:
			output.write(F"\t{r}\t{r.replace('ank_', '')}_score")
		output.write("\n")

	for i, line in enumerate(all_lines):
		#remove unwanted third column and convert "(" and ")" to "*"
		temp = line.replace("(", "*").replace(")","*").split()
		line = temp[0]+"\t"+temp[1]

		temp0 = line.split("*")
		confid = temp0[1:][::2]
		line2 = "".join(temp0[0:-2][::2])

		temp1 = line2.split(",")
		j=1
		new_line = [temp1[0]]
		while j<len(temp1):
			if  "unidentified" in temp1[j] or float(confid[j-1]) < confidence:
				del confid[j-1:]
				break
			else:
				new_line.append(temp1[j])
			j+=1

		line2 = ",".join(new_line)

		temp2 = line2.split(",")
		# OTU_1328        d:Fungi, p:Ascomycota, c:Archaeorhizomycetes, o:Archaeorhizomycetales, f:Archaeorhizomycetaceae, g:Archaeorhizomyces, s:Archaeorhizomyces_sp
		temp3 = temp2[0].split()
		# OTU_1328, d:Fungi
		temp4 = []
		for item in temp2[1:]:
			temp4.append(item[2:].capitalize())
		# Ascomycota, Archaeorhizomycetes, Archaeorhizomycetales, Archaeorhizomycetaceae, Archaeorhizomyces, Archaeorhizomyces_sp

		# remove "_sp" species classificaitons
		if ranks[0] == "Kingdom" and len(temp4)>0 and temp4[-1].endswith("_sp"):
			del temp4[-1]
			del confid[-1]

		# remove terminal Incertae_sedis
		while len(temp4)>0 and temp4[-1]=="Incertae_sedis":
			del temp4[-1]
			del confid[-1]

		confid = [str(x) for x in confid]
		if len(confid) > 0:
			score = confid[-1]
		else:
			score = 0
		final_line = F"{temp3[0]}\t{score}\t{temp3[1][2:].capitalize()}\tNA"

		tax_confi = ""
		for k in range(len(temp4)):
			tax_confi += F"\t{temp4[k]}\t{confid[k]}"

		output.write(F"{final_line+tax_confi}\n")

	output.close()
	return output_file

################################################################################
def reformat_SINTAX(sintax_file, output_dir, confidence, ranks):
	input = open (sintax_file)
	all_lines = input.readlines()
	input.close()

	output_file = F"{output_dir}otu_taxonomy_sintax_final.txt"
	output = open(output_file, "w")
	if ranks[0] == "Kingdom":
		output.write("OTU_ID\tOTU_Score\tKingdom\tK_score\tPhylum\tP_score\tClass\tC_score")
		output.write("\tOrder\tO_score\tFamily\tF_score\tGenus\tG_score\tSpecies\tS_score\n")
	else:
		output.write("OTU_ID\tOTU_Score")
		for r in ranks:
			output.write(F"\t{r}\t{r.replace('ank_', '')}_score")
		output.write("\n")
	for i, line in enumerate(all_lines):
		# remove unwanted third column and convert "(" and ")" to "*"
		# temp = line.replace("(", "*").replace(")","*").split("\t")
		temp = line.split("\t")
		ID = temp[0].split(" ")[0]
		del temp[2:]
		# temp =>  'OTU_999'	'd:Fungi*1.0000*,p:Ascomycota*1.0000*,c:Leotiomycetes*1.0000*,o:Helotiales*1.0000*,s:Helotiales_sp*1.0000*'
		### NEW STUFF
		temp0 = temp[1].split(",")
		res = []
		for x in temp0:
			t = list(x)
			t[-1] = "*"
			t[-8] = "*"
			res.append("".join(t))
		temp0 = ",".join(res).split("*")[:-1]
		### END NEW STUFF
		# temp0 = temp[1].split("*")
		# temp0 =>  'd:Fungi,' '1.0000' ',p:Ascomycota' '1.0000' ',c:Leotiomycetes' '1.0000' ',o:Helotiales' '1.0000' ',s:Helotiales_sp' '1.0000'
		confid = temp0[1:][::2]
		# confid =>  '1.0000' '1.0000' '1.0000' '1.0000' '1.0000'
		temp_line = "".join(temp0[0:-2][::2])
		# temp_line =>  "d:Fungi,p:Ascomycota,c:Leotiomycetes,o:Helotiales,s:Helotiales_sp"

		# fix missing taxonomic levels
		temp1 = temp_line.split(",")
		# temp1 =>  'd:Fungi' 'p:Ascomycota' 'c:Leotiomycetes' 'o:Helotiales' 's:Helotiales_sp'
		if ranks[0] == "Kingdom":
			levels = ["d:", "p:", "c:", "o:", "f:", "g:", "s:"]
			if len(temp1)<len(levels) and len(temp1) > 1:
				if "g:" in temp1[-2]:
					for k, level in enumerate(temp1):
						if levels[k] not in temp1[k]:
							temp1.insert(k, levels[k]+"Incertae_sedis")
							confid.insert(k, 9)
				else:
					for k, level in enumerate(temp1):
						if levels[k] not in temp1[k]:
							temp1.insert(k, levels[k]+"unidentified")
							confid.insert(k, 0)
		# else:
		# 	levels = [r.replace('ank_', '') for r in ranks]
		# 	if len(temp1)<len(ranks):
		# 		print(levels, temp1, len(temp1))
		# 		for k, level in enumerate(temp1):
		# 			print(temp1[k], levels[k])
		# 			if levels[k] not in temp1[k]:
		# 				temp1.insert(k, levels[k]+"unidentified")
		# 				confid.insert(k, 0)
		# print(confid, temp1)
		j=0
		temp2 = []
		while j<len(temp1):
			if  "unidentified" in temp1[j]:
				del confid[j:]
				break
			elif confid[j]==9 and float(confid[j+1])<confidence:
				del confid[j:]
				break
			elif float(confid[j])<confidence:
				del confid[j:]
				break
			else:
				temp2.append(temp1[j].capitalize())
			j+=1

		# remove "_sp" species classificaitons
		if len(temp2)>0 and temp2[-1].endswith("_sp"):
			del temp2[-1]
			del confid[-1]
		# remove terminal Incertae_sedis
		while len(temp2)>0 and "Incertae_sedis" in temp2[-1]:
			del temp2[-1]
			del confid[-1]

		confid = [str(x) if x!=9 else "NA" for x in confid]

		new_taxonomy = []
		for item in temp2:
			new_taxonomy.append(item[2:].capitalize())

		if confid == []:
			score = "NA"
		else:
			score = confid[-1]

		tax_confi = ""
		for k in range(len(new_taxonomy)):
			tax_confi += F"\t{new_taxonomy[k]}\t{confid[k]}"

		output.write(F"{ID}\t{score}{tax_confi}\n")


	output.close()
	return output_file

################################################################################
def reformat_BLAST(blast_file, output_dir, confidence, max_hits, ethresh, p_iden_thresh, ranks):
	output_file = F"{output_dir}/otu_taxonomy_blast_final.txt" # Filename for output
	if ranks[0] == "Kingdom":
		classification_buf = "OTU_ID\tOTU_Score\tKingdom\tK_score\tPhylum\tP_score\tClass\tC_score"
		classification_buf += "\tOrder\tO_score\tFamily\tF_score\tGenus\tG_score\tSpecies\tS_score\n"
	else:
		classification_buf = "OTU_ID\tOTU_Score"
		for r in ranks:
			classification_buf += F"\t{r}\t{r.replace('ank_', '')}_score"
		classification_buf += "\n"

	blast_res = pd.read_csv(blast_file) # Read the input csv
	blast_res = blast_res.astype({"e_value" : "float64"})
	uniq = pd.unique(blast_res["query"]) # List of all otus
	for q in uniq:
		q_list = [q, "0.0"] # OTU and placeholder confidence
		q_sub = blast_res[(blast_res["query"] == q) & (blast_res["e_value"] <= ethresh) & (blast_res["percent_identity"] >= p_iden_thresh)] # Subset by OTU and e_values
		if len(q_sub) == 0:
			q_list.extend([""]*len(ranks)*2)
		else:
			q_sub = q_sub[:min([len(q_sub), max_hits])] # Take all hits or up to max_hits
			for t in ranks:
				if t not in q_sub.columns and t == "Kingdom":
					t = "Domain"
				vcs = q_sub[t].value_counts(normalize = True)
				if len(vcs) == 0 or "unidentified" in vcs.index[0] or vcs[0] < confidence or (t == ranks[-1] and vcs.index[0].endswith("_sp")): # If unidentified, under conf thresh, or a species with "_sp", break
				    break
				else:
					if vcs.index[0].endswith("Incertae_sedis"):
					    q_list.extend(["Incertae_sedis", str(vcs[0])])
					else:
						q_list.extend([vcs.index[0], str(vcs[0])])
					q_list[1] = str(vcs[0])
		classification_buf += "\t".join(q_list) + "\n"
	with open(output_file, "w") as ofile:
	    ofile.write(classification_buf)
	return output_file

################################################################################
def build_iso_dict(isolate_file):
	iso_dict = {}
	with open(isolate_file, "r") as ifile:
		line = ifile.readline()
		while line != "":
			if "# Query: " in line: # Checking if hits were found
				quer = line.strip().split("Query: ")[1]
				line = ifile.readline()
				line = ifile.readline()
				if line == "# 0 hits found\n": # If no hits found
					iso_dict[quer] = ["", ""]
			elif line[0] != "#": # BLAST hit lines
				spl = line.strip().split("\t")
				iso_dict[spl[0]] = [spl[1], spl[4]]
			line = ifile.readline()
	return iso_dict

################################################################################
def build_dict(filename):
	file = open(filename, "r")
	all_lines = file.readlines()
	file.close()

	dict = {}
	for i, line in enumerate(all_lines[1:]):
		temp = line.replace(" ", "_").strip().split()
		dict[temp[0]] = []
		if len(temp)>2:
			dict[temp[0]]=temp[2:]
		if len(dict[temp[0]])<14:
			while len(dict[temp[0]])<14:
				dict[temp[0]].append("")
		# strip numbers from species identifications
		species = "".join(
						list(
							filter(lambda c: not c.isdigit(), dict[temp[0]][-2])))
		dict[temp[0]][-2] = species.replace("_"," ")
	return dict

################################################################################
def vote(cla1, cla2, cla3, conservative):
	winner = ""
	taxa = [cla1[0].replace("NA", ""), cla2[0].replace("NA", ""), cla3[0].replace("NA", "")]
	scores = [cla1[1], cla2[1], cla3[1]]
	tally = ["0","0","0"]
	duplicates_notempty = [i for i, x in enumerate(taxa) if x!= "" and taxa.count(x) > 1]
	unique_2empty = [i for i, x in enumerate(taxa) if x!="" and taxa.count("") > 1]
	unique = [i for i, x in enumerate(taxa) if x!="" and taxa.count("") == 1]
	for j in range(0,3):
		if taxa[j]!="":
			if j in duplicates_notempty:
				winner = taxa[j]
				break
			elif j in unique_2empty:
				if conservative:
					winner = ""
				else:
					winner = taxa[j]
				break
			elif j in unique:
				scores = [float(x) if x!="NA" and x!="" else 0 for x in scores]
				winner = taxa[scores.index(max([scores[x] for x in unique]))]
		else:
			winner = taxa[j]
	return winner

################################################################################
def count_classifications(filenames, output_dir):
	# rdp, utax, sintax, consensus
	file_num = 0
	unique_dict = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{}}
	for i, file in enumerate(filenames):
		input = open(file, "r")
		all_lines = input.readlines()
		input.close()
		count_y = [0,0,0,0,0,0,0]
		count_n = [0,0,0,0,0,0,0]
		output1 = open(F"{output_dir}otu_taxonomy_CountClassified.txt", "w")
		if i<3:	#first 3 files have scores
			start= 2
			freq = 2
		else: 	#consensus file does not have scores
			start= 1
			freq = 1
		for j, line in enumerate(all_lines[1:]):
			temp = line.strip().split("\t")
			taxonomy = temp[start::freq]
			if len(taxonomy)==7:
				# strip numbers from species identifications
				species = "".join(list(filter(lambda c: not c.isdigit(), taxonomy[-1])))
				taxonomy[-1] = species.replace("_"," ").strip()

			for k in range(0,7):
				if k<len(taxonomy):
					count_y[k]+=1
					if taxonomy[k] not in unique_dict[k]:
						unique_dict[k][taxonomy[k]] = [0,0,0,0]
						unique_dict[k][taxonomy[k]][file_num]+= 1
					else:
						unique_dict[k][taxonomy[k]][file_num]+= 1
				else:
					taxonomy.append("Unidentified")
					count_n[k]+=1
					if taxonomy[k] not in unique_dict[k]:
						unique_dict[k][taxonomy[k]] = [0,0,0,0]
						unique_dict[k][taxonomy[k]][file_num]+= 1
					else:
						unique_dict[k][taxonomy[k]][file_num]+= 1


		for l, level in enumerate(count_y):
			count_y[l] = str(level)
		for m, level in enumerate(count_n):
			count_n[m] = str(level)
		output1.write("\tKingdom\tPhylum\tClass\tOrder\tFamily\tGenus\tSpecies\n")
		output1.write("Classified\t"+"\t".join(count_y)+"\n")
		output1.write("Unclassified\t"+"\t".join(count_n))
		output1.close()
		file_num+=1

	output2 = open(F"{output_dir}Classification_Summary.txt", "w")
	output2.write("Classification\tRDP\tUTAX\tSINTAX\tConsensus\n")
	for l in range(0, 7):
		key_list = list(unique_dict[l].keys())
		key_list.sort()
		for key in key_list:
			output2.write(key+"\t"+"\t".join(str(x) for x in unique_dict[l][key])+"\n")
	output2.close()

###############################################################################
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
###############################################################################
#Example RDP input:
#OTU_2836	_	Root	rootrank	1.0	Fungi	Kingdom	0.98	Zygomycota	Phylum	0.05	Zygomycota_Incertae_sedis	Class	0.05	Mucorales	Order	0.04	Syncephalastraceae	Family	0.01	Fennellomyces	Genus	0.01	Fennellomyces linderi	Species	0.01
#Criteria: temp = line.split("\t"), temp[3]=="rootrank" len(temp)> 21

#Example UTAX input
#OTU_2545	d:Fungi,p:Basidiomycota(0.9941),c:Agaricomycetes(0.8548),o:Agaricales(0.8523),f:Mycenaceae(0.5664),g:Mycena(0.2776),s:Mycena_epipterygia(0.0882)	p:Basidiomycota,c:Agaricomycetes,o:Agaricales	-
#Criteria: "),c:" in line, temp = line.split("\t"), temp[1].startswith("d:")

#Example SINTAX input
#OTU_5443	d:Fungi(1.0000),p:Ascomycota(0.9700),c:Pezizomycetes(0.8000),o:Pezizales(0.7900),f:Sarcosomataceae(0.7700),g:Pseudoplectania(0.3700),s:Pseudoplectania_nigrella(0.3700)	+	d:Fungi,p:Ascomycota,c:Pezizomycetes
#Criteria: "),p:" in line, temp = line.split("\t"), temp[1].startswith("d:")

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output_dir", type=str, help="directory to for output files")
parser.add_argument("-c", "--conf", type=float, help="confidence score for voting")
parser.add_argument("-x", "--tax", type=str, help="taxonomy assignments directory")
parser.add_argument("-b", "--blast", type=bool, nargs='?', const=True, default=False, help="Use BLAST instead of SINTAX")
parser.add_argument("-e", "--evalue", type=float, default=1, help="Maximum evalue for BLAST hits")
parser.add_argument("-m", "--mhits", type=int, default=10, help="Maximum number of hits for BLAST")
parser.add_argument("-p", "--p_iden", type=float, default=0., help="Minimum proportion identity of hits for BLAST")
parser.add_argument("-f", "--format", type=str, help="database formatting")
parser.add_argument("-d", "--db", type=str, default="", help="database file")
parser.add_argument("-t", "--tf", type=str, default="", help="training files path")
parser.add_argument("-i", "--isolates", type=bool, help="Use isolates")
parser.add_argument("-s", "--conservative", type=bool, help="Use conservative rule (prevents overclassification, looses sensitivity)")
args = parser.parse_args()

# confidence = float(args.conf)

if args.blast:
	three_classifiers = ["rdp", "sintax", "blast"]
else:
	three_classifiers = ["rdp", "utax", "sintax"]

if args.format == "UNITE":
	filename = args.db
	filename_base = args.tf + "/" + ".".join(os.path.basename(filename).split(".")[:-1])

	header_line = open(filename_base + "__RDP_taxonomy.txt", "r").readline()
	ranks = header_line.strip().split("\t")[1:]
	for classifier in three_classifiers:
		file_name = F"{args.tax}otu_taxonomy."+classifier
		try:
			open(file_name,"r")
		except IOError:
			print("ERROR: "+classifier.upper()+" file could not be opened.")
			sys.exit()
		input_file = open(file_name,"r")
		line = input_file.readline()
		temp0 = line.split("\t")
		if classifier == "rdp":
			if len(temp0)<10 or temp0[3]!="rootrank":
				print("Input file not in RDP format. Please Reformat As Below:")
				print("OTU_###	_	Root	rootrank	1.0	Fungi	Kingdom	0.98	Zygomycota	Phylum	0.05	Zygomycota_Incertae_sedis	Class	0.05	Mucorales	Order	0.04	Syncephalastraceae	Family	0.01	Fennellomyces	Genus	0.01	Fennellomyces linderi	Species	0.01")
				sys.exit()
		elif classifier == "utax":
			if ",s:" not in temp0[1] or not temp0[1].startswith("d:"):
				print("Input file not in UTAX format. Please Reformat As Below:")
				print("OTU_###	d:Fungi,p:Ascomycota(0.9700),c:Pezizomycetes(0.8000),o:Pezizales(0.7900),f:Sarcosomataceae(0.7700),g:Pseudoplectania(0.3700),s:Pseudoplectania_nigrella(0.3700)	+	d:Fungi,p:Ascomycota,c:Pezizomycetes")
				sys.exit()
		elif classifier == "blast":
			if "query,subject,bitscore,e_value,percent_identity,query_coverage" not in temp0[0]:
				print("Input file not in BLAST format. Please Reformat As Below:")
				print("query,subject,bitscore,e_value,percent_identity,query_coverage,kingdom,phylum,class,order,family,genus,species")
				sys.exit()
		else:
			if "),s:" not in temp0[1] or not temp0[1].startswith("d:"):
				print("Input file not in SINTAX format. Please Reformat As Below:")
				print("OTU_###	d:Fungi(1.0000),p:Ascomycota(0.9700),c:Pezizomycetes(0.8000),o:Pezizales(0.7900),f:Sarcosomataceae(0.7700),g:Pseudoplectania(0.3700),s:Pseudoplectania_nigrella(0.3700)	+	d:Fungi,p:Ascomycota,c:Pezizomycetes")
				sys.exit()

		input_file.close()

		if classifier == "rdp":
			print("\n____________________________________________________________________\nReformatting "+classifier.upper()+" file\n")
			rdp_file = reformat_RDP(file_name, args.output_dir, args.conf, ranks)
			rdp_dict = build_dict(rdp_file)
		elif classifier == "utax":
			print("\nReformatting "+classifier.upper()+" file\n")
			uta_file = reformat_UTAX(file_name, args.output_dir, args.conf, ranks)
			uta_dict = build_dict(uta_file)
		elif classifier == "blast":
			print("\nReformatting "+classifier.upper()+" file\n")
			blast_file = reformat_BLAST(file_name, args.output_dir, args.conf, max_hits=args.mhits, ethresh=args.evalue, p_iden_thresh=args.p_iden, ranks=ranks)
			blast_dict = build_dict(blast_file)
		else:
			print("\nReformatting "+classifier.upper()+" file\n")
			sin_file = reformat_SINTAX(file_name, args.output_dir, args.conf, ranks)
			sin_dict = build_dict(sin_file)
		if args.isolates:
			print("\nReformatting isolate result file\n")
			iso_dict = build_iso_dict(F"{args.tax}/isolates_blast.out")
		print("\tDone\n")

	print("\nGenerating consensus taxonomy & combined taxonomy table\n")
	consensus_file = F"{args.output_dir}consensus_taxonomy.txt"
	consensus = open(consensus_file, "w")
	if args.isolates:
		consensus.write("OTU_ID\tKingdom\tPhylum\tClass\tOrder\tFamily\tGenus\tSpecies\tIsolate\tIsolate_percent_id\n")
	else:
		consensus.write("OTU_ID\tKingdom\tPhylum\tClass\tOrder\tFamily\tGenus\tSpecies\n")

	if args.blast:
			combined = open(F"{args.output_dir}combined_taxonomy.txt", "w")
			combined.write("OTU_ID\tKingdom_RDP\tKingdom_BLAST\tKingdom_SINTAX\tKingdom_Consensus\tPhylum_RDP\tPhylum_BLAST\tPhylum_SINTAX")
			combined.write("\tPhylum_Consensus\tClass_RDP\tClass_BLAST\tClass_SINTAX\tClass_Consensus\tOrder_RDP\tOrder_BLAST\tOrder_SINTAX")
			combined.write("\tOrder_Consensus\tFamily_RDP\tFamily_BLAST\tFamily_SINTAX\tFamily_Consensus\tGenus_RDP\tGenus_BLAST\tGenus_SINTAX")
			combined.write("\tGenus_Consensus\tSpecies_RDP\tSpecies_BLAST\tSpecies_SINTAX\tSpecies_Consensus\n")

			for otu in rdp_dict.keys():
				consensus.write(otu+"\t")
				combined.write(otu)
				levels = []
				for m in range(0,14,2):
					level = vote(rdp_dict[otu][m:m+2], blast_dict[otu][m:m+2], sin_dict[otu][m:m+2], args.conservative)
					combined.write("\t"+rdp_dict[otu][m]+"\t"+blast_dict[otu][m]+"\t"+sin_dict[otu][m]+"\t")
					if level != "":
						levels.append(level)
					combined.write(level)
				if args.isolates:
					lev_string = '\t'.join(levels)
					consensus.write(F"{lev_string}\t{iso_dict[otu][0]}\t{iso_dict[otu][1]}\n")
				else:
					consensus.write("\t".join(levels)+"\n")
				combined.write("\n")
			print("\tDone\n")

			consensus.close()
			combined.close()


			print("\nGenerating classification counts & summary table\n")
			count_classifications([rdp_file, sin_file, blast_file, consensus_file], args.output_dir)
	else:
		combined = open(F"{args.output_dir}combined_taxonomy.txt", "w")
		combined.write("OTU_ID\tKingdom_RDP\tKingdom_SINTAX\tKingdom_UTAX\tKingdom_Consensus\tPhylum_RDP\tPhylum_SINTAX\tPhylum_UTAX")
		combined.write("\tPhylum_Consensus\tClass_RDP\tClass_SINTAX\tClass_UTAX\tClass_Consensus\tOrder_RDP\tOrder_SINTAX\tOrder_UTAX")
		combined.write("\tOrder_Consensus\tFamily_RDP\tFamily_SINTAX\tFamily_UTAX\tFamily_Consensus\tGenus_RDP\tGenus_SINTAX\tGenus_UTAX")
		combined.write("\tGenus_Consensus\tSpecies_RDP\tSpecies_SINTAX\tSpecies_UTAX\tSpecies_Consensus\n")

		for otu in rdp_dict.keys():
			consensus.write(otu+"\t")
			combined.write(otu)
			levels = []
			for m in range(0,14,2):
				level = vote(rdp_dict[otu][m:m+2], sin_dict[otu][m:m+2], uta_dict[otu][m:m+2], arg.conservative)
				combined.write("\t"+rdp_dict[otu][m]+"\t"+sin_dict[otu][m]+"\t"+uta_dict[otu][m]+"\t")
				if level != "":
					levels.append(level)
				combined.write(level)
			if args.isolates:
				lev_string = '\t'.join(levels)
				consensus.write(F"{lev_string}\t{iso_dict[otu][0]}\t{iso_dict[otu][1]}\n")
			else:
				consensus.write("\t".join(levels)+"\n")
			combined.write("\n")
		print("\tDone\n")

		consensus.close()
		combined.close()


		print("\nGenerating classification counts & summary table\n")
		count_classifications([rdp_file, uta_file, sin_file, consensus_file], args.output_dir)
	print("\tDone\n\n")
	print("____________________________________________________________________\n")
else:
	filename = args.db
	filename_base = args.tf + "/" + ".".join(os.path.basename(filename).split(".")[:-1])

	header_line = open(filename_base + "__RDP_taxonomy.txt", "r").readline() # Extract first line of taxonomy file to get ranks
	ranks = header_line.strip().split("\t")[1:]
	for classifier in three_classifiers:
		file_name = F"{args.tax}otu_taxonomy."+classifier
		try:
			open(file_name,"r")
		except IOError:
			print("ERROR: "+classifier.upper()+" file could not be opened.")
			sys.exit()
		input_file = open(file_name,"r")
		line = input_file.readline()
		temp0 = line.split("\t")
		if classifier == "rdp":
			if len(temp0)<10 or temp0[3]!="rootrank":
				print("Input file not in RDP format. Please Reformat As Below:")
				print("OTU_###	_	Root	rootrank	1.0	Fungi	Kingdom	0.98	Zygomycota	Phylum	0.05	Zygomycota_Incertae_sedis	Class	0.05	Mucorales	Order	0.04	Syncephalastraceae	Family	0.01	Fennellomyces	Genus	0.01	Fennellomyces linderi	Species	0.01")
				sys.exit()
		elif classifier == "utax":
			if not temp0[1].startswith("R1:"):
				print("Input file not in UTAX format. Please Reformat As Below:")
				print("OTU_###	d:Fungi,p:Ascomycota(0.9700),c:Pezizomycetes(0.8000),o:Pezizales(0.7900),f:Sarcosomataceae(0.7700),g:Pseudoplectania(0.3700),s:Pseudoplectania_nigrella(0.3700)	+	d:Fungi,p:Ascomycota,c:Pezizomycetes")
				sys.exit()
		elif classifier == "blast":
			if "query,subject,bitscore,e_value,percent_identity,query_coverage" not in temp0[0]:
				print("Input file not in BLAST format. Please Reformat As Below:")
				print("query,subject,bitscore,e_value,percent_identity,query_coverage,kingdom,phylum,class,order,family,genus,species")
				sys.exit()
		else:
			if temp0[1].startswith("R1:"):
				print("Input file not in SINTAX format. Please Reformat As Below:")
				print("OTU_###	d:Fungi(1.0000),p:Ascomycota(0.9700),c:Pezizomycetes(0.8000),o:Pezizales(0.7900),f:Sarcosomataceae(0.7700),g:Pseudoplectania(0.3700),s:Pseudoplectania_nigrella(0.3700)	+	d:Fungi,p:Ascomycota,c:Pezizomycetes")
				sys.exit()

		input_file.close()

		if classifier == "rdp":
			print("\n____________________________________________________________________\nReformatting "+classifier.upper()+" file\n")
			rdp_file = reformat_RDP(file_name, args.output_dir, args.conf, ranks)
			rdp_dict = build_dict(rdp_file)
		elif classifier == "utax":
			print("\nReformatting "+classifier.upper()+" file\n")
			uta_file = reformat_UTAX(file_name, args.output_dir, args.conf, ranks)
			uta_dict = build_dict(uta_file)
		elif classifier == "blast":
			print("\nReformatting "+classifier.upper()+" file\n")
			blast_file = reformat_BLAST(file_name, args.output_dir, args.conf, max_hits=args.mhits, ethresh=args.evalue, p_iden_thresh=args.p_iden, ranks=ranks)
			blast_dict = build_dict(blast_file)
		else:
			print("\nReformatting "+classifier.upper()+" file\n")
			sin_file = reformat_SINTAX(file_name, args.output_dir, args.conf, ranks)
			sin_dict = build_dict(sin_file)
		if args.isolates:
			print("\nReformatting isolate result file\n")
			iso_dict = build_iso_dict(F"{args.tax}/isolates_blast.out")
		print("\tDone\n")

	print("\nGenerating consensus taxonomy & combined taxonomy table\n")
	consensus_file = F"{args.output_dir}consensus_taxonomy.txt"
	consensus = open(consensus_file, "w")

	combined = open(F"{args.output_dir}combined_taxonomy.txt", "w")
	combined.write("OTU_ID")
	consensus.write("OTU_ID")

	if args.blast:
		for r in ranks:
			combined.write(F"\t{r}_RDP\t{r}_BLAST\t{r}_SINTAX\t{r}_Consensus")
			consensus.write(F"\t{r}")
		if args.isolates:
			consensus.write("\tIsolate\tIsolate_percent_id")
		combined.write("\n")
		consensus.write("\n")

		for otu in rdp_dict.keys():
			consensus.write(otu+"\t")
			combined.write(otu)
			levels = []
			for m in range(0,14,2):
				level = vote(rdp_dict[otu][m:m+2], blast_dict[otu][m:m+2], sin_dict[otu][m:m+2], args.conservative)
				combined.write("\t"+rdp_dict[otu][m]+"\t"+blast_dict[otu][m]+"\t"+sin_dict[otu][m]+"\t")
				if level != "":
					levels.append(level)
				combined.write(level)
			if args.isolates:
				lev_string = '\t'.join(levels)
				consensus.write(F"{lev_string}\t{iso_dict[otu][0]}\t{iso_dict[otu][1]}\n")
			else:
				consensus.write("\t".join(levels)+"\n")
			combined.write("\n")
		print("\tDone\n")

		consensus.close()
		combined.close()


		print("\nGenerating classification counts & summary table\n")
		count_classifications([rdp_file, sin_file, blast_file, consensus_file], args.output_dir)
	else:
		combined = open(F"{args.output_dir}combined_taxonomy.txt", "w")
		filename = args.db
		filename_base = args.tf + "/" + ".".join(os.path.basename(filename).split(".")[:-1])

		header_line = open(filename_base + "__RDP_taxonomy.txt", "r").readline()
		ranks = header_line.strip().split("\t")[1:]
		combined.write("OTU_ID")
		consensus.write("OTU_ID")

		for r in ranks:
			combined.write(F"\t{r}_RDP\t{r}_SINTAX\t{r}_UTAX\t{r}_Consensus")
			consensus.write(F"\t{r}")
		if args.isolates:
			consensus.write("\tIsolate\tIsolate_percent_id")
		combined.write("\n")
		consensus.write("\n")

		for otu in rdp_dict.keys():
			consensus.write(otu+"\t")
			combined.write(otu)
			levels = []
			for m in range(0,14,2):
				level = vote(rdp_dict[otu][m:m+2], sin_dict[otu][m:m+2], uta_dict[otu][m:m+2], args.conservative)
				combined.write("\t"+rdp_dict[otu][m]+"\t"+sin_dict[otu][m]+"\t"+uta_dict[otu][m]+"\t")
				if level != "":
					levels.append(level)
				combined.write(level)
			if args.isolates:
				lev_string = '\t'.join(levels)
				consensus.write(F"{lev_string}\t{iso_dict[otu][0]}\t{iso_dict[otu][1]}\n")
			else:
				consensus.write("\t".join(levels)+"\n")
			combined.write("\n")
		print("\tDone\n")

		consensus.close()
		combined.close()


		print("\nGenerating classification counts & summary table\n")
		count_classifications([rdp_file, uta_file, sin_file, consensus_file], args.output_dir)
	print("\tDone\n\n")
	print("____________________________________________________________________\n")
