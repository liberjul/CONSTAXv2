CONSTAX Options
===============

To visualize CONSTAX options:

    .. code-block:: default

       constax --help

This is what CONSTAX will display on the terminal

    .. code-block:: text

       Usage: constax [OPTION] ...
       Classify input OTU sequences by CONSTAX consensus taxonomy algorithm
       Example constax -t --db sh_general_release_fungi_35077_RepS_04.02.2020.fasta

       -c, --conf=0.8                         Classification confidence threshold
       -n, --num_threads=1                    Number of threads to use
       -m, --max_hits=10                      Maximum number of BLAST hits to use, for use with -b option
       -e, --evalue=1                         Maximum expect value of BLAST hits to use, for use with -b option
       -p, --p_iden=0.8                       Minimum proportion identity of BLAST hits to use, for use with -b option
       -d, --db                               Database to train classifiers
       -f, --trainfile=./training_files       Path to which training files will be written
       -i, --input=otus.fasta                 Input file in FASTA format containing sequence records to classify
       -o, --output=./outputs                 Output directory for classifications
       -x, --tax=./taxonomy_assignments       Directory for taxonomy assignments
       -t, --train                            Complete training if specified
       -b, --blast                            Use BLAST instead of UTAX if specified
       --msu_hpcc                             If specified, use executable paths on Michigan State University HPCC. Overrides other path arguments
       --conservative                         If specified, use conservative consensus rule (2 null = null winner)
       --make_plot                            If specified, run R script to make plot of classified taxa
       --check                                If specified, runs checks but stops before training or classifying
       --mem                                  Memory available to use for RDP, in MB. 32000MB recommended for UNITE, 128000MB for SILVA
       --sintax_path                          Path to USEARCH/VSEARCH executable for SINTAX classification
       --utax_path                            Path to USEARCH executable for UTAX classification
       --rdp_path                             Path to RDP classifier.jar file
       --constax_path                         Path to CONSTAX scripts
       --pathfile                             File with paths to SINTAX, UTAX, RDP, and CONSTAX executables
       --isolates                             FASTA formatted file of isolates to use BLAST against
       --high_level_db                        FASTA database file of representative sequences for assignment of high level taxonomy
       -h, --help                             Display this help and exit
       -v, --version                          Display version and exit
