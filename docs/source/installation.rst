Installation
=============

Simple installation with conda for Linux/OSX/WSL
-------------------------------------------------

CONSTAX comes in a conda package that contained all the dependancies needed to run the software and can be easily installed this way:

  .. code-block:: default

      conda install constax -c bioconda

Custom installation of USEARCH
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to use USEARCH which is a propetary, instead of VSEARCH, you will have to install it yourself and generate a pathfile.txt to specify the binary location. Please see the tutorial secitons.

* USEARCH/VSEARCH

  - USEARCH installation from `drive5 <https://www.drive5.com/usearch/download.html>`_

  .. tabs::

      .. tab:: Linux

        .. code-block:: default

            wget https://www.drive5.com/downloads/usearch11.0.667_i86linux32.gz
            gunzip usearch11.0.667_i86linux32.gz

      .. tab:: Windows

        .. code-block:: default

            curl -O https://www.drive5.com/downloads/usearch11.0.667_win32.gz
            gunzip usearch11.0.667_win32.gz

      .. tab:: OSX

        .. code-block:: default

            curl -O https://www.drive5.com/downloads/usearch11.0.667_i86osx32.gz
            gunzip usearch11.0.667_i86osx32.gz

  - `VSEARCH <https://github.com/torognes/vsearch>`_ can be installed by `conda <https://anaconda.org/bioconda/vsearch>`_, `pip <https://pypi.org/project/vsearch/>`_, or downloading from `source <https://github.com/torognes/vsearch#download-and-install>`_.
