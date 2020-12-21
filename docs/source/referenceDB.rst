Suggested Reference Databases
=============================

Dependent on where your sequences originate (e.g. ITS, 16S, LSU), you will need to have an appropriate 
database with which to classify them.

For Fungi or all Eukaryotes, the `UNITE <https://unite.ut.ee/>`_ database is preferred. The format of the reference database to use with 
CONSTAX is one of those under the `General <https://unite.ut.ee/repository.php>`_ fasta format.

For Bacteria and Archaea, we recommend the `SILVA <https://www.arb-silva.de/no_cache/download/archive/current/Exports/>`_ reference database. 
The ``SILVA_XXX_SSURef_tax_silva.fasta.gz`` file can be gunzip-ped and used.

.. Note::
   SILVA taxonomy is not assigned by Linnean ranks (Kingdom, Phylum, etc.), so instead placeholder ranks 1-n are used. 
   Also, the size of the SILVA database means that a server/cluster is required to train the classifier becasue 
   128GB RAM for the RDP training are required. If you have a computer with 32GB of RAM, you may be able to train using 
   the UNITE database. If you cannot train locally for UNITE, the RDP files can be downloaded from `here <https://github.com/liberjul/CONSTAXv2_data/tree/master/sh_general_release_fungi_35077_RepS_04.02.2020>`_.
   The `genus_wordConditionalProbList.txt.gz` file should be gunzip-ped after downloading.
