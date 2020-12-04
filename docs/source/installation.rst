Installation
============

Simple installation with conda for Linux/OSX/WSL
-------------------------------

  .. code-block:: default

      conda install constax -c bioconda

Custom installation
--------------------

* USEARCH/VSEARCH

  - USEARCH installation from `drive5 <https://www.drive5.com/usearch/download.html>`_

  .. tabs::

      .. tab:: Windows

        .. code-block:: default

            curl -O https://www.drive5.com/downloads/usearch11.0.667_i86linux32.gz
            gunzip usearch<version>.gz

      .. tab:: Linux

        .. code-block:: default

            curl -O https://www.drive5.com/downloads/usearch11.0.667_i86linux32.gz
            gunzip usearch11.0.667_i86linux32.gz

      .. tab:: OSX

        .. code-block:: default

            curl -O https://www.drive5.com/downloads/usearch11.0.667_i86osx32.gz
            gunzip usearch11.0.667_i86osx32.gz

  - `VSEARCH <https://github.com/torognes/vsearch>`_ can be installed by `conda <https://anaconda.org/bioconda/vsearch>`_, `pip <https://pypi.org/project/vsearch/>`_, or downloading from `source <https://github.com/torognes/vsearch#download-and-install>`_.
