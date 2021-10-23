#!/usr/bin/env python
import os, subprocess, argparse, sys, time

def false_to_null(arg):
    if arg == "False":
        return "null"
    else:
        return arg

env = os.environ.copy()

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-c", "--conf", type=str, default="0.8", help="Classification confidence threshold")
parser.add_argument("-n", "--num_threads", type=str, default="1", help="directory to for output files")
parser.add_argument("-m", "--mhits", type=str, default="10", help="Maximum number of BLAST hits to use, for use with -b option")
parser.add_argument("-e", "--evalue", type=str, default="1.0", help="Maximum expect value of BLAST hits to use, for use with -b option")
parser.add_argument("-p", "--p_iden", type=str, default="0.0", help="Minimum proportion identity of BLAST hits to use, for use with -b option")
parser.add_argument("-d", "--db", type=str, default="", help="Database to train classifiers, in FASTA format")
parser.add_argument("-f", "--trainfile", type=str, default="./training_files", help="Path to which training files will be written")
parser.add_argument("-i", "--input", type=str, default="otus.fasta", help="Input file in FASTA format containing sequence records to classify")
parser.add_argument("-o", "--output", type=str, default="./outputs", help="Output directory for classifications")
parser.add_argument("-x", "--tax", type=str, default="./taxonomy_assignments", help="Directory for taxonomy assignments")
parser.add_argument("-t", "--train", action="store_true", help="Complete training if specified")
parser.add_argument("-b", "--blast", action="store_true", help="Use BLAST instead of UTAX if specified")
parser.add_argument("--select_by_keyword", type=str, default="False", help="Takes a keyword argument and --input FASTA file to produce a filtered database with headers containing the keyword with name --output")
parser.add_argument("--msu_hpcc", action="store_true", help="If specified, use executable paths on Michigan State University HPCC. Overrides other path arguments")
parser.add_argument("-s", "--conservative", action="store_true", help="If specified, use conservative consensus rule (2 False = False winner)")
parser.add_argument("--consistent", action="store_true", help="If specified, show if the consensus taxonomy is consistent with the real hierarchical taxonomy")
parser.add_argument("--make_plot", action="store_true", help="If specified, run R script to make plot of classified taxa")
parser.add_argument("--check", action="store_true", help="If specified, runs checks but stops before training or classifying")
parser.add_argument("--mem", type=str, default="32000", help="Memory available to use for RDP, in MB. 32000MB recommended for UNITE, 128000MB for SILVA")
parser.add_argument("--sintax_path", type=str, default="False", help="Path to USEARCH/VSEARCH executable for SINTAX classification")
parser.add_argument("--utax_path", type=str, default="False", help="Path to USEARCH executable for UTAX classification")
parser.add_argument("--rdp_path", type=str, default="False", help="Path to RDP classifier.jar file")
parser.add_argument("--constax_path", type=str, default="False", help="Path to CONSTAX scripts")
parser.add_argument("--pathfile", type=str, default="pathfile.txt", help="File with paths to SINTAX, UTAX, RDP, and CONSTAX executables")
parser.add_argument("--isolates", type=str, default="False", help="FASTA formatted file of isolates to use BLAST against")
parser.add_argument("--isolates_query_coverage", type=str, default="75", help="Threshold of sequence query coverage to report isolate matches")
parser.add_argument("--isolates_percent_identity", type=str, default="1",help="Threshold of aligned sequence percent identity to report isolate matches")
parser.add_argument("--high_level_db", type=str, default="False", help="FASTA database file of representative sequences for assignment of high level taxonomy")
parser.add_argument("--high_level_query_coverage", type=str, default="75", help="Threshold of sequence query coverage to report high-level taxonomy matches")
parser.add_argument("--high_level_percent_identity", type=str, default="1", help="Threshold of aligned sequence percent identity to report high-level taxonomy matches")
parser.add_argument("--combine_only", action="store_true", help="Only combine taxonomy without rerunning classifiers")
parser.add_argument("-v", "--version", action="store_true", help="Display version and exit")
args = parser.parse_args()

env["TRAIN"]=str(args.train).lower()
env["BLAST"]=str(args.blast).lower()
env["SHOW_VERSION"]=str(args.version).lower()
env["KEYWORD"]=false_to_null(args.select_by_keyword)
env["MSU_HPCC"]=str(args.msu_hpcc).lower()
env["CONSERVATIVE"]=str(args.conservative).lower()
env["CONSISTENT"]=str(args.consistent).lower()
env["CONF"]=args.conf
env["NTHREADS"]=args.num_threads
env["MAX_HITS"]=args.mhits
env["EVALUE"]=args.evalue
env["P_IDEN"]=args.p_iden
env["DB"]=args.db
env["TFILES"]=args.trainfile
env["INPUT"]=args.input
env["OUTPUT"]=args.output
env["TAX"]=args.tax
env["MAKE_PLOT"]=str(args.make_plot).lower()
env["CHECK"]=str(args.check).lower()
env["COMBINE_ONLY"]=str(args.combine_only).lower()
env["PATHFILE"]=args.pathfile
env["MEM"]=args.mem
env["ISOLATES"]=false_to_null(args.isolates)
env["ISO_QC"]=args.isolates_query_coverage
env["ISO_ID"]=args.isolates_percent_identity
env["HL_DB"]=false_to_null(args.high_level_db)
env["HL_FMT"]="null"
env["HL_QC"]=args.high_level_query_coverage
env["HL_ID"]=args.high_level_percent_identity
env["USE_ISOS"]="False"
env["SINTAXPATH_USER"]=args.sintax_path.lower() if args.sintax_path == "False" else args.sintax_path
env["UTAXPATH_USER"]=args.utax_path.lower() if args.utax_path == "False" else args.utax_path
env["RDPPATH_USER"]=args.rdp_path.lower() if args.rdp_path == "False" else args.rdp_path
env["CONSTAXPATH_USER"]=args.constax_path.lower() if args.constax_path == "False" else args.constax_path

version="2.0.15"; build="0"; prefix="placehold"

if os.path.isfile(args.pathfile):
    with open(args.pathfile, "r") as pathfile:
        if "\ " in pathfile.read():
            raise NameError("Remove any backslashes (\) from CONSTAXPATH in the pathfile located at: ", args.pathfile)

if args.constax_path != "False":
    constax_path = args.constax_path
elif args.msu_hpcc:
    constax_path = "/mnt/ufs18/rs-022/bonito_lab/CONSTAX_May2020"
elif os.path.isfile(args.pathfile):
    with open(args.pathfile, "r") as pathfile:
        line = pathfile.readline()
        while line != "" and "CONSTAXPATH=" not in line:
            line = pathfile.readline()
        constax_path = line.strip().split("CONSTAXPATH=")[1]
else:
    if "CONDA_PREFIX" not in env:
        raise NameError("CONDA_PREFIX environment variable not found.")
    elif "envs" in env["CONDA_PREFIX"]:
        pathfiles = [F"{env['CONDA_PREFIX']}/opt/constax-{version}-{build}/pathfile.txt"]
    else:
        pathfiles = [F"{prefix}/opt/constax-{version}/pathfile.txt", F"{prefix}/opt/constax-{version}-{build}/pathfile.txt"]
    path_found = False
    for pathfile in pathfiles:
        if os.path.isfile(pathfile):
            path_found = True
            with open(pathfile, "r") as pfile:
                line = pfile.readline()
                while line != "" and "CONSTAXPATH=" not in line:
                    line = pfile.readline()
                constax_path = line.strip().split("CONSTAXPATH=")[1]
            break
    if not path_found:
        raise FileNotFoundError("Cannot find pathfile.txt at ", pathfiles)
if constax_path[-1] != "/":
    constax_path = constax_path.strip('"') + "/"
if os.path.isfile(F"{constax_path}constax_no_inputs.sh"): # First check the path in pathfile
    script_loc = F"{constax_path}constax_no_inputs.sh"
elif os.path.isfile("./constax_no_inputs.sh"): # Check local and global locations
    script_loc = "./constax_no_inputs.sh"
else: # If those don't work, change the pathfile to fix it for future runs
    if "CONDA_PREFIX" not in env:
        raise NameError("CONDA_PREFIX environment variable not found.")
    elif "envs" in env["CONDA_PREFIX"]:
        constax_paths = [F"{env['CONDA_PREFIX']}/opt/constax-{version}-{build}"]
    else:
        constax_paths = [F"{prefix}/opt/constax-{version}-{build}"]
    path_found = False
    for pos_constax_path in constax_paths:
        if os.path.isfile(F"{pos_constax_path}/constax_no_inputs.sh"):
            path_found = True
            new_constax_path = pos_constax_path
            script_loc = F"{pos_constax_path}/constax_no_inputs.sh"
            break
    if not path_found:
        raise FileNotFoundError("Cannot find constax_no_inputs.sh in ", constax_paths)
    subprocess.run(F"sed -i'' -e 's|CONSTAXPATH=.*|CONSTAXPATH={new_constax_path}|' {new_constax_path}/pathfile.txt", shell=True)

### Attempt to run CONSTAX main script
if "CONDA_PREFIX" not in env: # Must have CONDA installed and on PATH
    raise NameError("CONDA_PREFIX environment variable not found.")
else:
    script_loc = script_loc.replace(" ", "\ ") # Add escape characters to paths in case spaces are present
    log_file = F"log_constax2_{time.strftime('%Y-%m-%d_%H-%M-%S')}.txt" # Set up unique logfile name

    if not os.path.isdir(env["CONSTAXPATH_USER"]): # If there is not a user-specified CONSTAXPATH, assign the one detected
        if env["CONSTAXPATH_USER"] != "false":
            raise FileNotFoundError(F"The constax_path you specified at {args.constax_path} does not exist.")
        env["CONSTAXPATH_USER"] = script_loc.strip("/constax_no_inputs.sh")

    if not os.path.isfile(args.pathfile): # If there is not a user-specified pathfile, assign the one detected
        if args.pathfile != "pathfile.txt": # If one was specified but doesn't exist
            raise FileNotFoundError(F"The pathfile you specified at {args.pathfile} does not exist.")
        new_pathfile = script_loc.strip("constax_no_inputs.sh") + "pathfile.txt"
        if os.path.isfile(new_pathfile): # Verify that the paths look right
            with open(new_pathfile, "r") as pathfile:
                if "\ " in pathfile.read():
                    raise NameError("Remove any backslashes (\) from CONSTAXPATH in the pathfile located at: ", new_pathfile)
                else:
                    env["PATHFILE"] = new_pathfile
        else:
            raise FileNotFoundError("No pathfile found in the CONSTAX directory")

    if "envs" in env["CONDA_PREFIX"]: # If run in a conda environment
        active_env = env["CONDA_PREFIX"].split("/envs/")[-1]
        try:
            with open(log_file, "w") as f:
                subprocess.run(F"bash -c 'conda activate {active_env}; {script_loc}'", env=env, check=True, shell=True, stderr=f)
        except subprocess.CalledProcessError as e:
            print(str(e))
            if "exit status 2" in str(e):
                subprocess.run(F"sed -i'' -e 's|python |python3 |' {script_loc}", shell=True) # fix python version
                subprocess.run(script_loc, env=env, shell=True)
            elif "exit status 1" not in str(e):
                print(str(e))
                with open(log_file, "r") as ifile:
                    if "conda activate" in ifile.read():
                        try:
                            subprocess.run(F"bash -c 'source activate {active_env}; {script_loc}'", env=env, check=True, shell=True)
                        except subprocess.CalledProcessError as e:
                            if "exit status 2" in str(e):
                                subprocess.run(F"sed -i'' -e 's|python |python3 |' {script_loc}", shell=True) # fix python version
                                subprocess.run(F"bash -c 'source activate {active_env}; {script_loc}'", env=env, shell=True)
                            elif "exit status 1" not in str(e):
                                print(str(e))
                    else:
                        for line in ifile:
                            print(line)
    else:
        try:
            subprocess.run(F"{script_loc}", env=env, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            if "exit status 2" in str(e):
                subprocess.run(F"sed -i'' -e 's|python |python3 |' {script_loc}", shell=True) # fix python version
                subprocess.run(script_loc, env=env, shell=True)
            elif "exit status 1" not in str(e):
                print(str(e))
