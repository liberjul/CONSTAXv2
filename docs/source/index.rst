Welcome to CONSTAX's documentation!
=====================================

**CONSTAX** (*CONSensus TAXonomy*) is a tool,
written in Python 3, for improved taxonomic resolution
of environmental DNA sequences. Briefly, CONSTAX
compares the taxonomic classifications obtained from RDP
Classifier, UTAX or BLAST, and SINTAX and merges them
into an improved consensus taxonomy using a 2 out of 3 rule
(e.g. If an OTU is classified as taxon A by RDP and UTAX/BLAST and taxon B by SINTAX, taxon A will be used in the consensus taxonomy) and the classification p-value to break the ties (e.g. when 3 different classification are obtained for the same OTU). This tool also produces summary classification outputs that are useful for downstream analyses. In summary, our results demonstrate that independent taxonomy assignment tools classify unique members of the fungal community, and greater classification power (proportion of assigned operational
taxonomic units at a given taxonomic rank) is realized
by generating consensus taxonomy of available classifiers
with CONSTAX.

CONSTAX 2.0.14 improves upon 1.0.0 with the following features:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* **Updated software requirements, including Python 3 and Java 8**

* **Simple installation with conda**

* **Compatibility with SILVA-formatted databases (for Bacteria, Archaea, protists, etc.)**

* **Streamlined command-line implementation**

* **BLAST classification option, due to legacy status of UTAX**

* **Parallelization of classification tasks**

* **Isolate matching**

Developed by
^^^^^^^^^^^^

* `Julian A. Liber <https://github.com/liberjul>`_

* `Gian M. N. Benucci <https://github.com/Gian77>`_

Funded by
^^^^^^^^^

* `Gregory Bonito <https://www.researchgate.net/profile/Gregory_Bonito>`_

CONSTAX 1.0.0 was authored by
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* `Kristi Gdanetz MacCready <https://github.com/gdanetzk>`_

* `Gian M. N. Benucci <https://github.com/Gian77>`_

* `Natalie Vande Pol <https://github.com/natalie-vandepol>`_

* `Gregory Bonito <https://www.researchgate.net/profile/Gregory_Bonito>`_


Reference
^^^^^^^^^

`Liber JA, Bonito G, Benucci GMN (2021) CONSTAX2: improved taxonomic classification of environmental DNA markers. Bioinformatics doi: 10.1093/bioinformatics/btab347 <https://doi.org/10.1093/bioinformatics/btab347>`_

`Gdanetz K, Benucci GMN, Vande Pol N, Bonito G (2017) CONSTAX: a tool for improved taxonomic resolution of environmental fungal ITS sequences. BMC Bioinformatics 18:538 doi 10.1186/s12859-017-1952-x <https://bmcbioinformatics.biomedcentral.com/track/pdf/10.1186/s12859-017-1952-x>`_

See the menu on the left for how to install CONSTAX and how to use it.

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   license
   installation
   referenceDB
   options
   tutorial1
   tutorial2
   tutorial3
   tutorial5
   tutorial4
   help

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
