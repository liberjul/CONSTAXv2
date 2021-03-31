Downloading the UNITE database
=================================

This tutorial is about how to obtain a reference database for classification of fungi or
eukaryotes in general. These will be downloaded from `UNITE <https://unite.ut.ee/repository.php>`_.

For classification of fungi, we have had tested with the `RepS 35077 General Release FASTA <https://plutof.ut.ee/#/doi/10.15156/BIO/786368>`_.

.. code-block:: language

   curl https://files.plutof.ut.ee/public/orig/E7/28/E728E2CAB797C90A01CD271118F574B8B7D0DAEAB7E81193EB89A2AC769A0896.gz > sh_general_release_04.02.2020.tar.gz
   tar -xzvf sh_general_release_04.02.2020.tar.gz

Use the FASTA called ``sh_general_release_fungi_35077_RepS_04.02.2020.fasta`` within the expanded directory for
your fungal reference database, specified with ``-d`` or ``--db`` in your ``constax`` command.

For the ``--high_level_db`` option, the eukaryotes database found here `https://plutof.ut.ee/#/doi/10.15156/BIO/786370 <https://plutof.ut.ee/#/doi/10.15156/BIO/786370>`_.
can be used. This will help to remove non-fungal OTUs from your dataset, or can be used as the main database (``-d, --db``)
for projects amplifying other eukaryotes.
