# Check for installed packages
conda list --explicit > env_list.txt

# Check if conda is installed
if grep -Fq "# This file may be used to create an environment using:" env_list.txt
then
  echo "Conda installed ..."
else
  echo "Conda not installed. Please see https://docs.anaconda.com/anaconda/install/"
  exit 1
fi

if grep -Fq "rdptools" env_list.txt
then
  echo "RDPTools installed ..."
else
  echo "Installing RDPTools ..."
  conda install -c bioconda rdptools
fi

if grep -Fq "vsearch" env_list.txt
then
  echo "VSEARCH installed ..."
else
  echo "Installing VSEARCH ..."
  conda install -c bioconda vsearch
fi

blastn -version > blastcheck.txt

if grep -Fq 'blastn: 2.' blastcheck.txt
then
  echo "BLAST installed ..."
else
  echo "Installing BLAST ..."
  conda install -c bioconda blast
fi

echo "export SINTAXPATH=vsearch" > pathfile.txt
echo "export RDPPATH=classifier" >> pathfile.txt
echo "export CONSTAXPATH=""$(pwd)" >> pathfile.txt

chmod +x constax.sh
ln -s constax.sh constax
