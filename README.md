# CONSTAXv2

CONSTAX (CONSensus TAXonomy) is a tool, written in Python 3, for improved taxonomic resolution of environmental fungal ITS sequences. Briefly, CONSTAX compares the taxonomic classifications obtained from RDP Classifier, UTAX or BLAST, and SINTAX and merges them into an improved consensus taxonomy using a 2 out of 3 rule (e.g. If an OTU is classified as taxon A by RDP and UTAX/BLAST and taxon B by SINTAX, taxon A will be used in the consensus taxonomy) and the classification p-value to break the ties (e.g. when 3 different classification are obtained for the same OTU). This tool also produces summary classification outputs that are useful for downstream analyses. In summary, our results demonstrate that independent taxonomy assignment tools classify unique members of the fungal community, and greater classification power (proportion of assigned operational taxonomic units at a given taxonomic rank) is realized by generating consensus taxonomy of available classifiers with CONSTAX.

CONSTAX v.2 improves upon v.1 with the following features:
- Updated software requirements, including Python 3 and Java 8.
- Compatibility with SILVA-formatted databases
- Streamlined command-line implementation
- BLAST classification option, due to legacy status of UTAX
- Parallelization of classification tasks
- Isolate matching

### Developed by
- [Julian Liber](https://github.com/liberjul)
- [Gian Maria Niccolò Benucci](https://github.com/Gian77)

### CONSTAX v.1 was authored by:
- [Natalie Vande Pol](https://github.com/natalie-vandepol)
- [Kristi Gdanetz MacCready](https://github.com/gdanetzk)
- [Gian Maria Niccolò Benucci](https://github.com/Gian77)
- [Gregory Bonito](https://www.researchgate.net/profile/Gregory_Bonito)

* [Gdanetz K, Benucci GMN, Vande Pol N, Bonito G (2017) CONSTAX: a tool for improved taxonomic resolution of environmental fungal ITS sequences. BMC Bioinformatics 18:538 doi 10.1186/s12859-017-1952-x](https://bmcbioinformatics.biomedcentral.com/track/pdf/10.1186/s12859-017-1952-x)

### Dependencies

- [USEARCH](https://www.drive5.com/usearch/download.html) (<= 9.X for UTAX, >= 9.X for SINTAX) or [VSEARCH](https://anaconda.org/bioconda/vsearch)
- [RDP](https://github.com/rdpstaff/RDPTools)
- [BLAST](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download) ([FTP site](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/), [Bioconda](https://anaconda.org/bioconda/blast))
- Python 3.6+, from [python.org](https://www.python.org/downloads/) or [Anaconda](https://www.anaconda.com/products/individual)
- Python packages [Pandas](https://pandas.pydata.org/getting_started.html) and [Numpy](https://numpy.org/), included in the Anaconda distribution
- [Java 8 JDK](https://www.oracle.com/java/technologies/javase-downloads.html) or [OpenJDK 8](https://anaconda.org/conda-forge/openjdk)

## Installation

### One step, for Linux, [WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10), or MacOS systems
```
conda install -c bioconda constax
```
This uses conda installations, including vsearch instead of usearch. You can modify `SINTAXPATH` in pathfile.txt if you have a usearch installation.
### Simple installation for Windows
```
git clone https://github.com/liberjul/CONSTAXv2.git
cd CONSTAXv2
bash install.sh
```
### Custom installation

#### USEARCH installation
1. Download the desired version from [here](https://www.drive5.com/usearch/download.html).
2. Run `gunzip usearch<version>.gz` to unzip.
3. Run `chmod +x usearch<version>` to make the file executable.

#### RDP installation
1. Requires [Java 8 JDK](https://www.oracle.com/java/technologies/javase-downloads.html) and apache ant (versions 1.9 and 1.10 worked fine)
- If on Windows Subsystem for Linux or Linux:
```
apt install openjdk-8-jdk-headless
apt install ant
```
- If on MacOS
    - install [Java 8 JDK](https://www.oracle.com/java/technologies/javase-downloads.html) and [apache ant 1.10](https://ant.apache.org/bindownload.cgi)
2. Run the following commands:
```
git clone https://github.com/rdpstaff/RDPTools.git
cd RDPTools
git submodule init AlignmentTools ReadSeq classifier TaxonomyTree
git submodule update
sed -i 's/1.5/1.6/' AlignmentTools/nbproject/project.properties ReadSeq/nbproject/project.properties classifier/nbproject/project.properties
sed -i 's/basedir="."/basedir="." xmlns:unless="ant:unless"/' classifier/build.xml
sed -i 's/name="download-traindata" unless="offline"/name="download-traindata" unless="skip_td_download"/' classifier/build.xml
sed -i 's+move file="${dist.dir}/data.tgz"+move unless:set="skip_td_download" file="${dist.dir}/data.tgz"+' classifier/build.xml
cd classifier
ant jar -Dskip_td_download=true
cp dist/classifier.jar ../
```
#### BLAST installation
##### From Bioconda
`conda install -c bioconda blast`
##### From NCBI
1. Download the BLAST executables from [here](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/). The ncbi-blast-\<version\>+-x64-\<system\>64.tar.gz file works fine.
2. Unzip with `tar -xzvf ncbi-blast-<version>+-x64-<system>64.tar.gz` (replace version and system).
3. Add the `blastn` and `makeblastdb` executables to your path. You can do this by moving them to your `bin` directory.

#### CONSTAX installation
1. Clone the repository: `git clone https://github.com/liberjul/CONSTAXv2.git`
2. Make `constax.sh` executable.
```
cd CONSTAXv2
chmod +x constax.sh
ln -s constax.sh constax
```

### Datasets
Dependent on where your sequences originate, you will need to have an appropriate database with which to classify them.

For [Fungi](https://plutof.ut.ee/#/doi/10.15156/BIO/786368) or all [Eukaryotes](https://plutof.ut.ee/#/doi/10.15156/BIO/786370), the UNITE database is preferred.

For Bacteria and Archaea, we recommend the [SILVA database](https://www.arb-silva.de/no_cache/download/archive/current/Exports/). The SILVA_XXX_SSURef_tax_silva.fasta.gz file can be `gunzip`-ped and used.

Note: SILVA taxonomy is not assigned by Linnean ranks (Kingdom, Phylum, etc.), so instead placeholder ranks 1-n are used. Also, the size of the SILVA database means that a server/cluster is required to train the classifier (128GB RAM for RDP). If you have a computer with 32GB of RAM, you may be able to train using the UNITE database. If you cannot train locally for UNITE, the RDP files can be downloaded from [here](https://github.com/liberjul/CONSTAXv2_data/tree/master/sh_general_release_fungi_35077_RepS_04.02.2020). The `genus_wordConditionalProbList.txt.gz` file should be `gunzip`-ped after downloading.

We have included a script for filtering the databases, which can create a Bacteria-only database, for example. The -k or --keyword argument is a substring of the record header.

```
python fasta_select_by_keyword.py -i SILVA_138_SSURef_tax_silva.fasta \
-o SILVA_138_SSURef_tax_silva_bact.fasta -k " Bacteria;"
```
### Running CONSTAX
```
constax --help
```
```
Welcome to CONSTAX version 2.0.4 build 2 - The CONSensus TAXonomy classifier
This software is distributed under MIT License
© Copyright 2020, Julian A. Liber, Gian M. N. Benucci & Gregory M. Bonito
github.com/liberjul/CONSTAXv2
constax.readthedocs.io/

Usage: constax [OPTION] ...
Classify input OTU sequences by CONSTAX consensus taxonomy algorithm
Example constax -t --db sh_general_release_fungi_35077_RepS_04.02.2020.fasta

-c, --conf=0.8                                      Classification confidence threshold
-n, --num_threads=1                                 Number of threads to use
-m, --max_hits=10                                   Maximum number of BLAST hits to use, for use with -b option
-e, --evalue=1                                      Maximum expect value of BLAST hits to use, for use with -b option
-p, --p_iden=0.8                                    Minimum proportion identity of BLAST hits to use, for use with -b option
-d, --db                                            Database to train classifiers
-f, --trainfile=./training_files                    Path to which training files will be written
-i, --input=otus.fasta                              Input file in FASTA format containing sequence records to classify
-o, --output=./outputs                              Output directory for classifications
-x, --tax=./taxonomy_assignments                    Directory for taxonomy assignments
-t, --train                                         Complete training if specified
-b, --blast                                         Use BLAST instead of UTAX if specified
--msu_hpcc                                          If specified, use executable paths on Michigan State University HPCC. Overrides other path arguments
--conservative                                      If specified, use conservative consensus rule (2 null = null winner)
--make_plot                                         If specified, run R script to make plot of classified taxa
--check                                             If specified, runs checks but stops before training or classifying
--mem                                               Memory available to use for RDP, in MB. 32000MB recommended for UNITE, 128000MB for SILVA
--sintax_path                                       Path to USEARCH/VSEARCH executable for SINTAX classification
--utax_path                                         Path to USEARCH executable for UTAX classification
--rdp_path                                          Path to RDP classifier.jar file
--constax_path                                      Path to CONSTAX scripts
--pathfile                                          File with paths to SINTAX, UTAX, RDP, and CONSTAX executables
--isolates                                          FASTA formatted file of isolates to use BLAST against
--isolates_query_coverage=75                        Threshold of sequence query coverage to report isolate matches
--isolates_percent_identity=0                       Threshold of aligned sequence percent identity to report isolate matches
--high_level_db                                     FASTA database file of representative sequences for assignment of high level taxonomy
--high_level_query_coverage=75                      Threshold of sequence query coverage to report high-level taxonomy matches
--high_level_percent_identity=0                     Threshold of aligned sequence percent identity to report high-level taxonomy matches
-h, --help                                          Display this help and exit
-v, --version                                       Display version and exit
```
If using a database for the first time, you will need to use the `-t` or `--train` flag to train the classifiers on the dataset.

In the directory with your OTU/zOTU/ASV/ESV FASTA file:

```
/path/to/CONSTAXv2/constax -i <input file> \
-o <output_directory> \
-f <training_files_directory> \
-x <taxonomy_assignments_directory> \
-d <database_file> \
--sintax_path <path/to/usearch> \
--rdp_path <path/to/RDPTools/classifier.jar> \
--constax_path <path/to/CONSTAXv2> \
-c 1.0 -b -t
```

The classification results are in the output directory. The file `consensus_taxonomy.txt` can be read in to R for microbiome analysis.

```
-c, --conf=0.8
```
Classification confidence threshold, used by each classifier (0,1]. Increase for improved specificity, reduced sensitivity.
```
-n, --num_threads=1
```
Number of threads to use for parallelization. Maximum classification speed at about 32 threads. Training only uses 1 thread.
```
-m, --max_hits=10                                   
```
Maximum number of BLAST hits to use, for use with -b option. When classifying with BLAST, this many hits are kept. Confidence for a given taxa is based on the proportion of these hits agree with that taxa. 5 works well for UNITE, 20 with SILVA (standard, not NR).
```
-e, --evalue=1
```
Maximum expect value of BLAST hits to use, for use with -b option. When classifying with BLAST, only hits under this expect value threshold are used. Decreasing will increase specificity, but decrease sensitivity at high taxonomic ranks.
```
-p, --p_iden=0.8
```
Minimum proportion identity of BLAST hits to use, for use with -b option. Minimum proportion of conserve bases to keep hit.
```
-d, --db
```
Database to train classifiers. UNITE and SILVA formats are supported. See [Datasets](https://github.com/liberjul/CONSTAXv2#datasets).
```
-f, --trainfile=./training_files
```                    
Path to which training files will be written.
```
-i, --input=otus.fasta
```
Input file in FASTA format containing sequence records to classify.
```
-o, --output=./outputs
```
Output directory for classifications.
```
-x, --tax=./taxonomy_assignments
```
Directory for taxonomy assignments.
```
-t, --train
```
Complete training if specified. Cannot run classification without training files present.
```
-b, --blast
```
Use BLAST instead of UTAX if specified. If installed with conda, this in the option that will work by default. UTAX is available from [USEARCH](https://www.drive5.com/usearch/download.html). BLAST classification generally performs better with faster training, similar classification speed, and greater accuracy.
```
--msu_hpcc
```
If specified, use executable paths on Michigan State University HPCC. Overrides other path arguments.
```
--conservative
```
If specified, use conservative consensus rule (2 null = null winner). Works better for SILVA to use this option.
```
--make_plot
```
If specified, run R script to make plot of classified taxa.
```
--check
```
If specified, runs checks but stops before training or classifying.
```
--mem
```
Memory available to use for RDP, in MB. 32000MB recommended for UNITE, 128000MB for SILVA.
```
--sintax_path
```
Path to USEARCH/VSEARCH executable for SINTAX classification. Can also be `vsearch` if already on path.
```
--utax_path
```
Path to USEARCH executable for UTAX classification.
```
--rdp_path
```
Path to RDP `classifier.jar` file, or `classifier` if on path from RDPTools conda install.
```
--constax_path
```
Path to CONSTAX scripts.
```
--pathfile
```
File with paths to SINTAX, UTAX, RDP, and CONSTAX executables.
```
--isolates
```
FASTA formatted file of isolates to use BLAST against.
```
--high_level_db
```
FASTA database file of representative sequences for assignment of high level taxonomy. The [SILVA NR99 database](https://www.arb-silva.de/no_cache/download/archive/release_138/Exports/) for SSU/16S/18S sequences and the [UNITE Eukayotes database](https://plutof.ut.ee/#/doi/10.15156/BIO/786370).
