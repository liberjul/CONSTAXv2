Installation
=============

Simple installation with conda for Linux/OSX/WSL
-------------------------------------------------

CONSTAX is a command line tool. You will need to open and run commands
in a terminal to use it. Windows user can `install WSL <https://docs.microsoft.com/en-us/windows/wsl/install-win10>`_ to use CONSTAX or `custom install <https://github.com/liberjul/CONSTAXv2#custom-installation-and-installation-for-windows>`_ on their machine.

CONSTAX comes in a conda package that contains all the dependencies needed to run the software and can be easily installed as showed below.

  .. code-block:: default

      conda install constax -c bioconda

If conda is not installed (you get an error which might include ``command not found``), `follow their instructions <https://conda.io/projects/conda/en/latest/user-guide/install/index.html>`_ to install it. Briefly:

1. Download the correct installation for your system, and run it.

  * Miniconda installation commands:

    .. tabs::

        .. tab:: Linux / WSL

          .. code-block:: default

              wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.9.2-Linux-x86_64.sh
              bash Miniconda3-py39_4.9.2-Linux-x86_64.sh

        .. tab:: OSX

          .. code-block:: default

              curl -O https://repo.anaconda.com/miniconda/Miniconda3-py39_4.9.2-MacOSX-x86_64.sh
              bash Miniconda3-py39_4.9.2-MacOSX-x86_64.sh

2. Follow the prompts.

3. Close and reopen terminal.

4. Try the command ``conda list``.

5. Proceed to installing CONSTAX as above.

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
