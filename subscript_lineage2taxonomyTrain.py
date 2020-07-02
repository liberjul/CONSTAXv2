#!/usr/bin/env python
#used to convert a taxonomy in tab-delimited file containing the taxonomic hierarchical structure to RDP Classifier taxonomy training file
#Approach:each taxon is uniquely identified by the combination of its tax id and depth from the root rank, its attributes comprise: name, parent taxid, and level of depth from the root rank.
import os

def lin2tax(file_base, format):
	print("\n\tTraining Taxonomy")
	with open(file_base+"__RDP_taxonomy.txt", 'r') as f:
		line = f.readline()

	# f = open(file_base+"__RDP_taxonomy.txt", 'r').readlines()
	# header = f[0]
		# cols = header.strip().split('\t')[1:]
		cols = line.strip().split('\t')[1:]
		hash = {}#taxon name-id map
		ranks = {}#column number-rank map
		# lineages = []#list of unique lineages
		# lineages = {} # dict of unique lineages
		hash = {"Root":0}#initiate root rank taxon id map
		for i in range(len(cols)):
			name = cols[i]
			ranks[i] = name
		root = ['0', 'Root', '-1', '0', 'rootrank']#root rank info
		with open(file_base+"__RDP_taxonomy_trained.txt", 'w') as output_file:
			output_file.write("*".join(root)+"\n")
		# output_file = open(file_base+"__RDP_taxonomy_trained.txt", 'w')
		ID = 0 #taxon id
		line = f.readline()
		if format == "UNITE":
			name_to_end = {}
			# end_name_dict = {}
			while line != "":
				rec_count = 0
				th_buf = ""
				output_buf = ""
				while line != "" and rec_count < 10000:
				# for line in f[1:]:
					rec_count += 1
					acc = line.split('\t')[0]
					cols = line.strip().split('\t')[1:]
				#	if not cols in lineages:#unique lineage
				#		lineages.append(cols)
					header = F">{acc}\tRoot"
					for i in range(len(cols)):#iterate each column
						#name = string.join(cols[:i + 1], ';')
						name = []
						for node in cols[:i + 1]:
							if not node == '-':
								name.append(node)
						pName = ";".join(name[:-1])
						# if name not in lineages:
						# 	lineages[name] = None
						# 	# lineages.append(name)
						depth = len(name)
						name = ";".join(name)
						if name in hash:
							if name != prev_name:
								prev_name = name
								# end_name = name.split(';')[-1]
								# if end_name not in end_name_dict:
								# 	end_name_dict[end_name] = 1
								# 	end_name = F"{end_name}_1"
								# else:
								# 	end_name_dict[end_name] += 1
								# 	end_name = F"{end_name}_{end_name_dict[end_name]}"
								header += F";{name_to_end[name]}"
							continue
						prev_name = name
						rank = ranks[i]
						#level = len(name.split(';'))
						#pName = string.join(cols[:i], ';')#parent name
						if i == 0:
							pName = 'Root'
						pID = hash[pName]#parent taxid
						ID += 1
						hash[name] = ID #add name-id to the map
						#out = ['%s'%ID, name, '%s'%pID, '%s'%depth, rank]
						end_name = name.split(';')[-1]
						# if end_name not in end_name_dict:
						# 	end_name_dict[end_name] = 1
						# 	end_name = F"{end_name}_1"
						# else:
						# 	end_name_dict[end_name] += 1
						# 	end_name = F"{end_name}_{end_name_dict[end_name]}"
						header += F";{end_name}"
						name_to_end[name] = end_name
						# out = ['%s'%ID, end_name, '%s'%pID, '%s'%depth, rank]
						# output_buf += ("*".join(out)+"\n")
						output_buf = F"{output_buf}{ID}*{end_name}*{pID}*{depth}*{rank}\n"
					th_buf += (header + "\n")
					line = f.readline()
				with open(file_base+"__RDP_taxonomy_headers.txt", "a+") as taxon_headers:
					taxon_headers.write(th_buf)
					print("Headers exported")
				with open(file_base+"__RDP_taxonomy_trained.txt", "a+") as output_file:
					output_file.write(output_buf)
					print("Trained taxonomy exported")
			# while line != "":
			# 	rec_count = 0
			# 	output_buf = ""
			# 	while line != "" and rec_count < 10000:
			# 	# for line in f[1:]:
			# 		rec_count += 1
			# # for line in f[1:]:
			# 		cols = line.strip().split('\t')[1:]
			# 	#	if not cols in lineages:#unique lineage
			# 	#		lineages.append(cols)
			# 		for i in range(len(cols)):#iterate each column
			# 			#name = string.join(cols[:i + 1], ';')
			# 			name = []
			# 			for node in cols[:i + 1]:
			# 				if not node == '-':
			# 					name.append(node)
			# 			pName = ";".join(name[:-1])
			# 			# if not name in lineages:
			# 			# 	lineages.append(name)
			# 			depth = len(name)
			# 			name = ";".join(name)
			# 			if name in hash.keys():
			# 				continue
			# 			rank = ranks[i]
			# 			#level = len(name.split(';'))
			# 			#pName = string.join(cols[:i], ';')#parent name
			# 			if i == 0:
			# 				pName = 'Root'
			# 			pID = hash[pName]#parent taxid
			# 			ID += 1
			# 			hash[name] = ID #add name-id to the map
			# 			#out = ['%s'%ID, name, '%s'%pID, '%s'%depth, rank]
			# 			out = ['%s'%ID, name.split(';')[-1], '%s'%pID, '%s'%depth, rank]
			# 			output_buf += ("*".join(out)+"\n")
			# 		line = f.readline()
			# 	with open(file_base+"__RDP_taxonomy_trained.txt", "a+") as output_file:
			# 		output_file.write(output_buf)
		else:
			name_to_end = {}
			end_name_dict = {}
			while line != "":
				rec_count = 0
				th_buf = ""
				output_buf = ""
				while line != "" and rec_count < 10000:
				# for line in f[1:]:
					rec_count += 1
					acc = line.split('\t')[0]
					cols = line.strip().split('\t')[1:]
				#	if not cols in lineages:#unique lineage
				#		lineages.append(cols)
					header = F">{acc}\tRoot"
					for i in range(len(cols)):#iterate each column
						#name = string.join(cols[:i + 1], ';')
						name = []
						for node in cols[:i + 1]:
							if not node == '-':
								name.append(node)
						pName = ";".join(name[:-1])
						# if name not in lineages:
						# 	lineages[name] = None
						# 	# lineages.append(name)
						depth = len(name)
						name = ";".join(name)
						if name in hash:
							if name != prev_name:
								prev_name = name
								# end_name = name.split(';')[-1]
								# if end_name not in end_name_dict:
								# 	end_name_dict[end_name] = 1
								# 	end_name = F"{end_name}_1"
								# else:
								# 	end_name_dict[end_name] += 1
								# 	end_name = F"{end_name}_{end_name_dict[end_name]}"
								header += F";{name_to_end[name]}"
							continue
						prev_name = name
						rank = ranks[i]
						#level = len(name.split(';'))
						#pName = string.join(cols[:i], ';')#parent name
						if i == 0:
							pName = 'Root'
						pID = hash[pName]#parent taxid
						ID += 1
						hash[name] = ID #add name-id to the map
						#out = ['%s'%ID, name, '%s'%pID, '%s'%depth, rank]
						end_name = name.split(';')[-1]
						if end_name not in end_name_dict:
							end_name_dict[end_name] = 1
							end_name = F"{end_name}_1"
						else:
							end_name_dict[end_name] += 1
							end_name = F"{end_name}_{end_name_dict[end_name]}"
						header += F";{end_name}"
						name_to_end[name] = end_name
						# out = ['%s'%ID, end_name, '%s'%pID, '%s'%depth, rank]
						# output_buf += ("*".join(out)+"\n")
						output_buf = F"{output_buf}{ID}*{end_name}*{pID}*{depth}*{rank}\n"
					th_buf += (header + "\n")
					line = f.readline()
				with open(file_base+"__RDP_taxonomy_headers.txt", "a+") as taxon_headers:
					taxon_headers.write(th_buf)
					print("Headers exported")
				with open(file_base+"__RDP_taxonomy_trained.txt", "a+") as output_file:
					output_file.write(output_buf)
					print("Trained taxonomy exported")
				# taxon_headers.close()
	# output_file.close()
