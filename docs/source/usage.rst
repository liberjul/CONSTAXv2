Run CONSTAX
===========

To run CONSTAX you need only need two objects 
* an input fasta file with the sequences you want to taxonomically classify; 
* a reference database in the general format.   

A classic run would look like this:

    .. code-clokc:: default

       conda activate <python environment with constax>

       /path/to/CONSTAXv2/constax \
       -i <input fasta to classify> \
       -d <reference database fasta \
       -t \
       -f <training_files_directory> \
       -x <taxonomy_assignments_directory> \
       -o <output_directory> \
       --sintax_path <path/to/usearch> \
       --rdp_path <path/to/RDPTools/classifier.jar> \
       --constax_path <path/to/CONSTAXv2> \
       -c 0.8 \
       -b

       conda deactivate


    .. note::

       Remember. If using a reference database for the first time, you will need to use the -t or --train flag to train
       the classifiers on the dataset. The training step is necessary only at first use, you can just point to
       the --trainfile PATH for the subsequent classifications with the same reference database.

