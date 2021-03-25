Installation
=============

Simple installation with conda for Linux/OSX/WSL
-------------------------------------------------

CONSTAX comes in a conda package that contains all the dependencies needed to run the software and can be easily installed as showed below.

  .. code-block:: default

      conda install constax -c bioconda

If conda is not installed, `follow their instructions <https://conda.io/projects/conda/en/latest/user-guide/install/index.html>`_ to install it. Briefly:

#. Download the correct installation for your system, and run it.

.. tabs::

    .. tab:: Linux / WSL

      .. code-block:: default

          wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.9.2-Linux-x86_64.sh
          bash Miniconda3-py39_4.9.2-Linux-x86_64.sh

    .. tab:: OSX

      .. code-block:: default

          curl -O https://repo.anaconda.com/miniconda/Miniconda3-py39_4.9.2-MacOSX-x86_64.sh
          bash Miniconda3-py39_4.9.2-MacOSX-x86_64.sh

#. Follow the prompts.

#. Close and reopen terminal.

#. Try the command ``conda list``.

#. Proceed to installing CONSTAX as above.

Custom installation of USEARCH
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to use USEARCH which is a proprietary, instead of VSEARCH, you will have to install it yourself and generate a pathfile.txt to specify the binary location. Please see the tutorial sections.

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
