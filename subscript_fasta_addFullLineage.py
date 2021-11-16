#!/usr/bin/python
import sys, os

def RDP_head_to_UTAX(lineage):
	taxa = lineage.split(";")[1:]
	out = ""
	for r in range(len(taxa)):
		out = F"{out}{'dkpcofgs'[r]}:{taxa[r]},"
	return out[:-1]
def addFullLineage(filebase):
	print("\n\tAdding Full Lineage\n\n")
	f1 = open(filebase+"__RDP_taxonomy_headers.txt", 'r').readlines()
	hash = {} #lineage map

	output_RDP = open(filebase+"__RDP_trained.fasta", 'w')
	output_UTAX = open(filebase+"__UTAX.fasta", 'w')

	for line in f1:
		ID, lineage = line.strip().split("\t")
		ID = ID.strip(">")
		hash[ID] = lineage

	f2 = open(filebase+"__RDP.fasta", 'r').readlines()
	for line in f2:
		if line[0] == '>':
			ID = line.strip().replace('>', '')
			try:
				lineage = hash[ID]
			except KeyError:
				print(ID, 'not in taxonomy file')
				sys.exit()
			output_RDP.write(F"{line.strip()}\t{lineage}\n")
			output_UTAX.write(F"{line.strip()};tax={RDP_head_to_UTAX(lineage)};\n")
		else:
			output_RDP.write(line.strip()+"\n")
			output_UTAX.write(line.strip()+"\n")
	output_RDP.close()
	output_UTAX.close()
