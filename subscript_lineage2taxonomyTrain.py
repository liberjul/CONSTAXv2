#!/usr/bin/env python
#used to convert a taxonomy in tab-delimited file containing the taxonomic hierarchical structure to RDP Classifier taxonomy training file
#Approach:each taxon is uniquely identified by the combination of its tax id and depth from the root rank, its attributes comprise: name, parent taxid, and level of depth from the root rank.
import os

def lin2tax(file_base, format):
	print("\n\tTraining Taxonomy")
	with open(file_base+"__RDP_taxonomy.txt", 'r') as f:
		line = f.readline()
		cols = line.strip().split('\t')[1:] # Split the first line into columns
		hash = {}#taxon name-id map
		ranks = {}#column number-rank map
		hash = {"Root":0}#initiate root rank taxon id map
		for i in range(len(cols)): # Assign ranks based on column headers
			ranks[i] = cols[i]
		root = ['0', 'Root', '-1', '0', 'rootrank']#root rank info
		with open(file_base+"__RDP_taxonomy_trained.txt", 'w') as output_file:
			output_file.write("*".join(root)+"\n")
		ID = 0 #taxon id
		line = f.readline()
		if format == "UNITE":
			name_to_end = {}
			while line != "":
				rec_count = 0
				th_buf = "" # taxon header buffer
				output_buf = "" # trained taxonomy buffer
				while line != "" and rec_count < 10000: # Rec count to export when buffer is at 10000 records
					rec_count += 1
					acc = line.split('\t')[0]
					cols = line.strip().split('\t')[1:]
					header = F">{acc}\tRoot"
					for i in range(len(cols)):#iterate each column
						name = []
						for node in cols[:i + 1]:
							if not node == '-':
								name.append(node)
						pName = ";".join(name[:-1])
						depth = len(name)
						name = ";".join(name)
						if name in hash: # Avoid repeated taxonomies
							if name != prev_name:
								prev_name = name
								header += F";{name_to_end[name]}"
							continue
						prev_name = name
						rank = ranks[i]
						if i == 0:
							pName = 'Root'
						pID = hash[pName]#parent taxid
						ID += 1
						hash[name] = ID #add name-id to the map
						end_name = name.split(';')[-1]
						header = F"{header};{end_name}"
						name_to_end[name] = end_name
						output_buf = F"{output_buf}{ID}*{end_name}*{pID}*{depth}*{rank}\n"
					th_buf = F"{th_buf}{header}\n"
					line = f.readline()
				with open(file_base+"__RDP_taxonomy_headers.txt", "a+") as taxon_headers:
					taxon_headers.write(th_buf)
				with open(file_base+"__RDP_taxonomy_trained.txt", "a+") as output_file:
					output_file.write(output_buf)
		else:
			name_to_end = {}
			end_name_dict = {}
			while line != "":
				rec_count = 0
				th_buf = ""
				output_buf = ""
				while line != "" and rec_count < 10000:
					rec_count += 1
					acc = line.split('\t')[0]
					cols = line.strip().split('\t')[1:]
					header = F">{acc}\tRoot"
					for i in range(len(cols)):#iterate each column
						name = []
						for node in cols[:i + 1]:
							if not node == '-':
								name.append(node)
						pName = ";".join(name[:-1])
						depth = len(name)
						name = ";".join(name)
						if name in hash:
							if name != prev_name:
								prev_name = name
								header += F";{name_to_end[name]}"
							continue
						prev_name = name
						rank = ranks[i]
						if i == 0:
							pName = 'Root'
						pID = hash[pName]#parent taxid
						ID += 1
						hash[name] = ID #add name-id to the map
						end_name = name.split(';')[-1]
						if end_name not in end_name_dict:
							end_name_dict[end_name] = 1
							end_name = F"{end_name}_1"
						else:
							end_name_dict[end_name] += 1
							end_name = F"{end_name}_{end_name_dict[end_name]}"
						header = F"{header};{end_name}"
						name_to_end[name] = end_name
						output_buf = F"{output_buf}{ID}*{end_name}*{pID}*{depth}*{rank}\n"
					th_buf = F"{th_buf}{header}\n"
					line = f.readline()
				with open(file_base+"__RDP_taxonomy_headers.txt", "a+") as taxon_headers:
					taxon_headers.write(th_buf)
					print("Headers exported")
				with open(file_base+"__RDP_taxonomy_trained.txt", "a+") as output_file:
					output_file.write(output_buf)
					print("Trained taxonomy exported")
