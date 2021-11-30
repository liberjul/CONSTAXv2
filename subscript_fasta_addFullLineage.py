#!/usr/bin/python
import sys, os

def RDP_head_to_UTAX(lineage, format):
	taxa = lineage.split(";")[1:]
	out = ""
	for r in range(len(taxa)):
		if format == "UNITE":
			out = F"{out}{'dkpcofg'[r]}:{taxa[r]},"
		else:
			out = F"{out}{'dkpcofgs'[r]}:{taxa[r]},"

	return out[:-1]
def addFullLineage(filebase, format):
	print("\n\tAdding Full Lineage\n\n")

	with open(filebase+"__RDP_taxonomy_headers.txt", 'r') as f:
		f1 = f.readlines()
	hash = {} #lineage map

	output_RDP = open(filebase+"__RDP_trained.fasta", 'w')
	output_UTAX = open(filebase+"__UTAX.fasta", 'w')

	for line in f1:
		ID, lineage = line.strip().split("\t")
		ID = ID.strip(">")
		hash[ID] = lineage

	with open(filebase+"__RDP.fasta", 'r') as f:
		f2 = f.readlines()
	for line in f2:
		if line[0] == '>':
			ID = line.strip().replace('>', '')
			try:
				lineage = hash[ID]
			except KeyError:
				print(ID, 'not in taxonomy file')
				sys.exit()
			output_RDP.write(F"{line.strip()}\t{lineage}\n")
			output_UTAX.write(F"{line.strip()};tax={RDP_head_to_UTAX(lineage, format)};\n")
		else:
			output_RDP.write(line.strip()+"\n")
			output_UTAX.write(line.strip()+"\n")
	output_RDP.close()
	output_UTAX.close()
