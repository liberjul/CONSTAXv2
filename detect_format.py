import sys, os, unicodedata, argparse, glob

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--db", type=str, help="database file")
args = parser.parse_args()

silva = "null"
filename = args.db

## Check if file exists
try:
	open(filename,"r")
except IOError:
	valid = 0
	sys.exit()


with open(filename,"r") as input_file:
	line = input_file.readline()
	line_bar_split = line.split("|")
	if line[0]!=">": # or len(temp0)!= 5:
		format = "INVALID"
	elif len(line_bar_split) > 1: # UNITE, because "|" is used in accession
		if "k__" in line_bar_split[-1]: # kingdom header is defined
			format="UNITE"

	elif line.count(";") >= 1: # Silva has ranks divided by ";"
		format = "SILVA"
	else:
		format = "INVALID"
print(format)
