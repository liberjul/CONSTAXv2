Examine SH (Species Hypothesis) hits from UNITE database
=================================

This tutorial is about how to examine poorly classified fungal OTUS by
comparing to SHs from the UNITE database, which often don't have species names
associated with them but are consistent taxa which could be of interest to the user.

This will require a `downloaded UNITE database<https://constax.readthedocs.io/en/latest/tutorial5.html>`_.

You can do this two separate ways:

1. Use the same database for both ``-d/--db`` and for ``--isolates``

    .. code-block:: language

       constax \
       -i otus.fasta \
       -b \
       -t \
       -d sh_general_release_fungi_35077_RepS_04.02.2020.fasta \
       --isolates sh_general_release_fungi_35077_RepS_04.02.2020.fasta

    The accessions found in the ``constax_taxonomy.txt`` file in the output directory is searchable at the `UNITE search page<https://unite.ut.ee/search.php#fndtn-panel1>`_.

2. Examine the ``blast.out`` file in the directory specified by ``-x/--tax`` or the default ``./taxonomy_assignments`` directory.

   .. code-block:: language

      # BLASTN 2.10.0+
      # Query: OTU_1
      # Database: /mnt/ufs18/rs-022/bonito_lab/CONSTAX_May2020/UNITE_Fungi_tf/sh_general_release_fungi_35077_RepS_04.02.2020__BLAST
      # Fields: query acc., subject acc., evalue, bit score, % identity, % query coverage per subject
      # 5 hits found
      OTU_1   KC306753        1.04e-96        351     99.482  100
      OTU_1   AF377107        2.25e-93        340     98.446  100
      OTU_1   AF377107        2.25e-93        340     98.446  100
      OTU_1   KC306757        8.16e-88        322     96.891  100
      OTU_1   KC306757        8.16e-88        322     96.891  100

  The second column is an accession number that can be searched at the `UNITE search page<https://unite.ut.ee/search.php#fndtn-panel1>`_.
