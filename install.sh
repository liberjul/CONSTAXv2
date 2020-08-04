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

if grep -Fq "openjdk-8" env_list.txt
then
  echo "openjdk 8 installed ..."
else
  echo "Installing openjdk 8 ..."
  conda install -c anaconda openjdk
fi

if grep -Fq "ant-1." env_list.txt
then
  echo "Apache ant installed ..."
else
  echo "Installing apache ant ..."
  conda install -c bioconda ant
fi
blastn -version > blastcheck.txt

if $(grep -Fq 'ant-1.' env_list.txt) || $(grep -Fq 'blastn: 2.' blastcheck.txt)
then
  echo "Blast installed ..."
else
  echo "Installing blast ..."
  conda install -c bioconda blast
fi

if grep -Fq "vsearch" env_list.txt
then
  echo "Vsearch installed ..."
else
  echo "Installing vsearch ..."
fi
echo "export SINTAXPATH=vsearch" > pathfile.txt

echo "Installing RDP ..."
git clone https://github.com/rdpstaff/RDPTools.git
cd RDPTools
git submodule init AlignmentTools ReadSeq classifier TaxonomyTree
git submodule update
sed -i 's/1.5/1.6/' AlignmentTools/nbproject/project.properties ReadSeq/nbproject/project.properties classifier/nbproject/project.properties
sed -i 's/basedir="."/basedir="." xmlns:unless="ant:unless"/' classifier/build.xml
sed -i 's/name="download-traindata" unless="offline"/name="download-traindata" unless="skip_td_download"/' classifier/build.xml
sed -i 's+move file="${dist.dir}/data.tgz"+move unless:set="skip_td_download" file="${dist.dir}/data.tgz"+' classifier/build.xml
cd classifier
ant jar -Dskip_td_download=true
cp dist/classifier.jar ../
echo "export RDPPATH=""$(pwd)"/classifier.jar >> ../../pathfile.txt
cd ../..
echo "RDP installed ..."

echo "export CONSTAXPATH=""$(pwd)" >> pathfile.txt

chmod +x constax.sh
