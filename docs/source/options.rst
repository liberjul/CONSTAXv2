CONSTAX Options
===============

To visualize CONSTAX options:

.. code-block:: default

   gian@gian-Z390-GY:~/tutorial$ constax --help

This is what CONSTAX will display on the terminal

.. code-block:: default

    # constax --help
    usage: constax [-h] [-c CONF] [-n NUM_THREADS] [-m MHITS] [-e EVALUE] [-p P_IDEN] [-d DB] [-f TRAINFILE] [-i INPUT]
                [-o OUTPUT] [-x TAX] [-t] [-b] [--select_by_keyword SELECT_BY_KEYWORD] [--msu_hpcc] [-s] [--make_plot]
                [--check] [--mem MEM] [--sintax_path SINTAX_PATH] [--utax_path UTAX_PATH] [--rdp_path RDP_PATH]
                [--constax_path CONSTAX_PATH] [--pathfile PATHFILE] [--isolates ISOLATES]
                [--isolates_query_coverage ISOLATES_QUERY_COVERAGE]
                [--isolates_percent_identity ISOLATES_PERCENT_IDENTITY] [--high_level_db HIGH_LEVEL_DB]
                [--high_level_query_coverage HIGH_LEVEL_QUERY_COVERAGE]
                [--high_level_percent_identity HIGH_LEVEL_PERCENT_IDENTITY] [-v]

    optional arguments:
    -h, --help            show this help message and exit
    -c CONF, --conf CONF  Classification confidence threshold (default: 0.8)
    -n NUM_THREADS, --num_threads NUM_THREADS
                         directory to for output files (default: 1)
    -m MHITS, --mhits MHITS
                         Maximum number of BLAST hits to use, for use with -b option (default: 10)
    -e EVALUE, --evalue EVALUE
                         Maximum expect value of BLAST hits to use, for use with -b option (default: 1.0)
    -p P_IDEN, --p_iden P_IDEN
                         Minimum proportion identity of BLAST hits to use, for use with -b option (default: 0.0)
    -d DB, --db DB        Database to train classifiers, in FASTA format (default: )
    -f TRAINFILE, --trainfile TRAINFILE
                         Path to which training files will be written (default: ./training_files)
    -i INPUT, --input INPUT
                         Input file in FASTA format containing sequence records to classify (default: otus.fasta)
    -o OUTPUT, --output OUTPUT
                         Output directory for classifications (default: ./outputs)
    -x TAX, --tax TAX     Directory for taxonomy assignments (default: ./taxonomy_assignments)
    -t, --train           Complete training if specified (default: False)
    -b, --blast           Use BLAST instead of UTAX if specified (default: False)
    --select_by_keyword SELECT_BY_KEYWORD
                         Takes a keyword argument and --input FASTA file to produce a filtered database with headers
                         containing the keyword with name --output (default: False)
    --msu_hpcc            If specified, use executable paths on Michigan State University HPCC. Overrides other path
                         arguments (default: False)
    -s, --conservative    If specified, use conservative consensus rule (2 False = False winner) (default: False)
    --consistent          If specified, show if the consensus taxonomy is consistent with the real hierarchical taxonomy (default: False)
    --make_plot           If specified, run R script to make plot of classified taxa (default: False)
    --check               If specified, runs checks but stops before training or classifying (default: False)
    --mem MEM             Memory available to use for RDP, in MB. 32000MB recommended for UNITE, 128000MB for SILVA
                         (default: 32000)
    --sintax_path SINTAX_PATH
                         Path to USEARCH/VSEARCH executable for SINTAX classification (default: False)
    --utax_path UTAX_PATH
                         Path to USEARCH executable for UTAX classification (default: False)
    --rdp_path RDP_PATH   Path to RDP classifier.jar file (default: False)
    --constax_path CONSTAX_PATH
                         Path to CONSTAX scripts (default: False)
    --pathfile PATHFILE   File with paths to SINTAX, UTAX, RDP, and CONSTAX executables (default: pathfile.txt)
    --isolates ISOLATES   FASTA formatted file of isolates to use BLAST against (default: False)
    --isolates_query_coverage ISOLATES_QUERY_COVERAGE
                         Threshold of sequence query coverage to report isolate matches (default: 75)
    --isolates_percent_identity ISOLATES_PERCENT_IDENTITY
                         Threshold of aligned sequence percent identity to report isolate matches (default: 1)
    --high_level_db HIGH_LEVEL_DB
                         FASTA database file of representative sequences for assignment of high level taxonomy
                         (default: False)
    --high_level_query_coverage HIGH_LEVEL_QUERY_COVERAGE
                         Threshold of sequence query coverage to report high-level taxonomy matches (default: 75)
    --high_level_percent_identity HIGH_LEVEL_PERCENT_IDENTITY
                         Threshold of aligned sequence percent identity to report high-level taxonomy matches (default:
                         1)

Options details
^^^^^^^^^^^^^^^

.. code-block:: default

   -c, --conf=0.8

Classification confidence threshold, used by each classifier (0,1]. Increase for improved specificity, reduced sensitivity.

.. code-block:: default

   -n, --num_threads=1

Number of threads to use for parallelization. Maximum classification speed at about 32 threads. Training only uses 1 thread.

.. code-block:: default

   -m, --max_hits=10

Maximum number of BLAST hits to use, for use with -b option. When classifying with BLAST, this many hits are kept. Confidence for a given taxa is based on the proportion of these hits agree with that taxa. 5 works well for UNITE, 20 with SILVA (standard, not NR).

.. code-block:: default

   -e, --evalue=1

Maximum expect value of BLAST hits to use, for use with -b option. When classifying with BLAST, only hits under this expect value threshold are used. Decreasing will increase specificity, but decrease sensitivity at high taxonomic ranks.

.. code-block:: default

   -p, --p_iden=0.8

Minimum proportion identity of BLAST hits to use, for use with -b option. Minimum proportion of conserve bases to keep hit.

.. code-block:: default

   -d, --db

Database to train classifiers. UNITE and SILVA formats are supported. See `Datasets <https://github.com/liberjul/CONSTAXv2#datasets>`_.

.. code-block:: default

   -f, --trainfile=./training_files

Path to which training files will be written.

.. code-block:: default

   -i, --input=otus.fasta

Input file in FASTA format containing sequence records to classify.

.. code-block:: default

   -o, --output=./outputs

Output directory for classifications.

.. code-block:: default

   -x, --tax=./taxonomy_assignments

Directory for taxonomy assignments.

.. code-block:: default

   -t, --train

Complete training if specified. Cannot run classification without training files present, so this option is necessary at least at the first time you run CONSTAX or you changed the taxonomic referenced sequence database.

.. code-block:: default

   -b, --blast

Use BLAST instead of UTAX if specified. If installed with conda, this in the option that will work by default. UTAX is available from `USEARCH <https://www.drive5.com/usearch/download.html>`_. BLAST classification generally performs better with faster training, similar classification speed, and greater accuracy.

.. code-block:: default

   --msu_hpcc

If specified, use executable paths on Michigan State University HPCC. Overrides other path arguments.

.. code-block:: default

   --conservative

If specified, use conservative consensus rule (2 null = null winner. For example, if BLAST is the only algorithm that classifies OTU_135 to Family Strophariaceae while SINTAX and RDP give no classification, then no classification is reported at the rank of Family for OTU_135 in the CONSTAX taxonomy). According to our tests, works better for SILVA database to use this option.

.. code-block:: default

   --make_plot

If specified, run R script to make plot of classified taxa. The plot compares how many OTUs were classifies at each rank for RDP, SINTAX, BLAST, and CONSTAX.

.. code-block:: default

   --check

If specified, runs checks but stops before training or classifying.

.. code-block:: default

   --mem

Memory available to use for RDP, in MB. 32000MB recommended for UNITE, 128000MB for SILVA. This is necessary for training the referenced databases.

.. code-block:: default

   --sintax_path

Path to USEARCH/VSEARCH executable for SINTAX classification. Can also be ``vsearch`` if already on path.

.. code-block:: default

   --utax_path

Path to USEARCH executable for UTAX classification.

.. code-block:: default

   --rdp_path

Path to RDP ``classifier.jar`` file, or ``classifier`` if on path from RDPTools conda install.

.. code-block:: default

   --constax_path

Path to CONSTAX scripts.

.. code-block:: default

   --pathfile

File with paths to SINTAX, UTAX, RDP, and CONSTAX executables. This useful in your local CONSTAX installation, please the tutorial for how to set a pathifile up in your system.

.. code-block:: default

   --isolates

FASTA formatted file of isolates to use BLAST against.

.. code-block:: default

   --high_level_db

FASTA database file of representative sequences for assignment of high level taxonomy. For this option you can use the `SILVA <https://www.arb-silva.de/no_cache/download/archive/release_138/Exports/>`_ NR99 database for SSU/16S/18S sequences or the the `UNITE <https://plutof.ut.ee/#/doi/10.15156/BIO/786370>`_ database for Eukaryotic ITS/28S sequences. This option is useful to match your OTUs representative sequences to a reference using a lower cutoff so you can identify for example, which sequences are Fungi and which ones are not.
