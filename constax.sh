#!/bin/bash -login

echo "################################################################"
echo "###############*** This is CONSTAX v.2 ***######################"
echo "#                                                              #"
echo "#                     MIT License                              #"
echo "#                 Copyright (C) 2020                           #"
echo "#  Julian Liber, Gian Maria Niccolo' Benucci, Gregory Bonito   #"
echo "#                                                              #"
echo "#         https://github.com/liberjul/CONSTAXv2                #"
echo "################################################################"


### Parse variable inputs
TEMP=`getopt -o c:n:m:e:p:d:i:o:x:tbhvf: --long conf:,num_threads:,max_hits:,evalue:,p_iden:,db:,input:,output:,tax:,train,blast,msu_hpcc,help,version,conservative,make_plot,trainfile:,mem:,sintax_path:,utax_path:,rdp_path:,constax_path:,pathfile:,isolates: \
             -n 'constax' -- "$@"`

if [ $? != 0 ]
then
  echo "Terminating..." >&2
  echo ""
  echo "Usage: ./constax.sh [OPTION] ..."
  echo "Classify input OTU sequences by CONSTAX consensus taxonomy algorithm"
  echo "Example ./constax.sh -t --db /mnt/research/common-data/Bio/UserDownloads/CONSTAX/DB/sh_general_release_fungi_35077_RepS_04.02.2020.fasta"
  echo ""
  echo "-c, --conf=0.8                                      Classification confidence threshold"
  echo "-n, --num_threads=1                                 Number of threads to use"
  echo "-m, --max_hits=10                                   Maximum number of BLAST hits to use, for use with -b option"
  echo "-e, --evalue=1                                      Maximum expect value of BLAST hits to use, for use with -b option"
  echo "-p, --p_iden=0.8                                    Minimum proportion identity of BLAST hits to use, for use with -b option"
  echo "-d, --db                                            Database to train classifiers, default uses UNITE General Release Feb 04 2020"
  echo "-f, --trainfile=./training_files                    Path to which training files will be written"
  echo "-i, --input=otus.fasta                              Input file in FASTA format containing sequence records to classify"
  echo "-o, --output=./outputs                              Output directory for classifications"
  echo "-x, --tax=./taxonomy_assignments                    Directory for taxonomy assignments"
  echo "-t, --train                                         Complete training if specified"
  echo "-b, --blast                                         Use BLAST instead of UTAX if specified"
  echo "--msu_hpcc                                          If specified, use executable paths on Michigan State University HPCC. Overrides other path arguments"
  echo "--conservative                                      If specified, use conservative consensus rule (2 null = null winner)"
  echo "--make_plot                                         If specified, run R script to make plot of classified taxa"
  echo "--mem                                               Memory available to use for RDP, in MB. 32000MB recommended for UNITE, 128000MB for SILVA."
  echo "--sintax_path                                       Path to USEARCH executable for SINTAX classification"
  echo "--utax_path                                         Path to USEARCH executable for UTAX classification"
  echo "--rdp_path                                          Path to RDP classifier.jar file"
  echo "--constax_path                                      Path to CONSTAX scripts"
  echo "--pathfile                                          File with paths to SINTAX, UTAX, RDP, and CONSTAX executables"
  echo "--isolates                                          FASTA formatted file of isolates to use BLAST against"
  echo "-h, --help                                          Display this help and exit"
  echo "-v, --version                                       Display version and exit"
  exit 1
fi

eval set -- "$TEMP"

VERSION=2.0.0; BUILD=0
TRAIN=false
BLAST=false
HELP=false
SHOW_VERSION=false
MSU_HPCC=false
CONSERVATIVE=False
CONF=0.8
NTHREADS=1
MAX_HITS=10
EVALUE=1
P_IDEN=0.8
DB=/mnt/research/common-data/Bio/UserDownloads/CONSTAX/DB/sh_general_release_fungi_35077_RepS_04.02.2020.fasta
INPUT=otus.fasta
OUTPUT=./outputs
TAX=./taxonomy_assignments
SINTAXPATH_USER=false
UTAXPATH_USER=false
RDPPATH_USER=false
CONSTAXPATH_USER=false
MAKE_PLOT=false
PATHFILE=pathfile.txt
MEM=32000
ISOLATES=null
USE_ISOS=False # Used as python bool

while true; do
  case "$1" in
    -c | --conf ) CONF="$2"; shift 2 ;;
    -p | --p_iden) P_IDEN="$2"; shift 2 ;;
    -n | --num_threads ) NTHREADS="$2"; shift 2 ;;
    -m | --max_hits ) MAX_HITS="$2"; shift 2 ;;
    -e | --evalue ) EVALUE="$2"; shift 2 ;;
    -d | --db ) DB="$2"; shift 2 ;;
    -i | --input ) INPUT="$2"; shift 2 ;;
    -o | --output ) OUTPUT="${2%/}"; shift 2 ;;
		-x | --tax ) TAX="${2%/}"; shift 2 ;;
    -f | --trainfile ) TFILES="${2%/}"; shift 2 ;;
    --mem ) MEM="$2"; shift 2 ;;
    --rdp_path ) RDPPATH_USER="$2"; shift 2 ;;
    --sintax_path ) SINTAXPATH_USER="$2"; shift 2 ;;
    --utax_path ) UTAXPATH_USER="$2"; shift 2 ;;
    --constax_path ) CONSTAXPATH_USER="${2%/}"; shift 2 ;;
    --pathfile ) PATHFILE="$2"; shift 2 ;;
    --isolates ) ISOLATES="$2"; shift 2 ;;
    -t | --train ) TRAIN=true; shift ;;
    -b | --blast ) BLAST=true; shift ;;
		-h | --help ) HELP=true; shift ;;
    -v | --version) SHOW_VERSION=true; shift ;;
    --msu_hpcc ) MSU_HPCC=true; shift ;;
    --conservative ) CONSERVATIVE=True; shift ;;
    --make_plot ) MAKE_PLOT=true; shift ;;
    -- ) shift; break ;;
    * ) break ;;
  esac
done

if $HELP
	then
    echo "Usage: ./constax.sh [OPTION] ..."
    echo "Classify input OTU sequences by CONSTAX consensus taxonomy algorithm"
    echo "Example ./constax.sh -t --db /mnt/research/common-data/Bio/UserDownloads/CONSTAX/DB/sh_general_release_fungi_35077_RepS_04.02.2020.fasta"
    echo ""
    echo "-c, --conf=0.8                                      Classification confidence threshold"
    echo "-n, --num_threads=1                                 Number of threads to use"
    echo "-m, --max_hits=10                                   Maximum number of BLAST hits to use, for use with -b option"
    echo "-e, --evalue=1                                      Maximum expect value of BLAST hits to use, for use with -b option"
    echo "-p, --p_iden=0.8                                    Minimum proportion identity of BLAST hits to use, for use with -b option"
    echo "-d, --db                                            Database to train classifiers, default uses UNITE General Release Feb 04 2020"
    echo "-f, --trainfile=./training_files                    Path to which training files will be written"
    echo "-i, --input=otus.fasta                              Input file in FASTA format containing sequence records to classify"
    echo "-o, --output=./outputs                              Output directory for classifications"
    echo "-x, --tax=./taxonomy_assignments                    Directory for taxonomy assignments"
    echo "-t, --train                                         Complete training if specified"
    echo "-b, --blast                                         Use BLAST instead of UTAX if specified"
    echo "--msu_hpcc                                          If specified, use executable paths on Michigan State University HPCC. Overrides other path arguments"
    echo "--conservative                                      If specified, use conservative consensus rule (2 null = null winner)"
    echo "--make_plot                                         If specified, run R script to make plot of classified taxa"
    echo "--mem                                               Memory available to use for RDP, in MB. 32000MB recommended for UNITE, 128000MB for SILVA."
    echo "--sintax_path                                       Path to USEARCH executable for SINTAX classification"
    echo "--utax_path                                         Path to USEARCH executable for UTAX classification"
    echo "--rdp_path                                          Path to RDP classifier.jar file"
    echo "--constax_path                                      Path to CONSTAX scripts"
    echo "--pathfile                                          File with paths to SINTAX, UTAX, RDP, and CONSTAX executables"
    echo "--isolates                                          FASTA formatted file of isolates to use BLAST against"
    echo "-h, --help                                          Display this help and exit"
    echo "-v, --version                                       Display version and exit"
		exit 1
fi
if $SHOW_VERSION
then
  echo "CONSTAX version $VERSION"
  exit 1
fi
if [ $MAX_HITS -eq 0 ]
then
  echo "Set -m/--max_hits to an integer greater than zero."
  exit 1
elif [[ $CONF =~ '^[+-]?[0-9]+([.][0-9]+)?$' ]] || (( $(echo "$CONF > 1.0" | bc -l) )) || (( $(echo "$CONF < 0.0" | bc -l) ))
then
  echo "Set -c/--conf to a float between 0 and 1"
  exit 1
elif [ $NTHREADS -lt 1 2> /dev/null ] || [ $? == 2 ]
then
  echo "Set -n/--nthreads to an integer greater than 0"
  exit 1
elif [[ $P_IDEN =~ '^[+-]?[0-9]+([.][0-9]+)?$' ]] || (( $(echo "$P_IDEN > 1.0" | bc -l) )) || (( $(echo "$P_IDEN < 0.0" | bc -l) ))
then
  echo "Set -p/--p_iden to a float between 0 and 1"
  exit 1
fi

if ! [ -f "$INPUT" ]
then
	echo "Input file $INPUT does not exist, exiting..."
	exit 1
elif ! [ -s "$INPUT" ]
then
	echo "Input file $INPUT is empty, exiting..."
	exit 1
elif [[ "$INPUT" != *.fasta ]]
then
  echo "Input file $INPUT must end with .fasta, exiting..."
  exit 1
fi

if ! [ -s "$DB" ]
then
	echo "Database file $DB is non-existent or empty, exiting..."
  exit 1
elif [[ "$DB" != *.fasta ]]
then
  echo "Database file $DB must end with .fasta, exiting..."
  exit 1
fi
if [ -d "$OUTPUT" ]  && ! [ -z "$(ls -A $OUTPUT)" ]
then
	echo "Overwritting previous classification..."
fi
if [ -d "$TAX" ]  && ! [ -z "$(ls -A $TAX)" ]
then
	echo "Overwritting previous taxonomy assignments..."
fi
if ! [ -d "$OUTPUT" ] # Output directory doesn't exist
then
	mkdir "$OUTPUT"
fi
if ! [ -d "$TAX" ] # Taxonomic assignments directory does not exist
then
	mkdir "$TAX"
fi

if $TRAIN && [ -z "$TFILES" ] # if training true and path not specified
then
	TFILES="training_files"
fi

if $TRAIN && ! [ -d "$TFILES" ] # if training is true and path does not exist
then
	mkdir "$TFILES"
fi

if $TRAIN
then
  if [ -z "$(ls -A $TFILES)" ] # training true and training file path empty
  then
  	echo "Training, with output to $TFILES..."
  else # training true and trainfile path is not empty
    echo "Performing training and overwritting training files..."
  fi
else # Training not true
  if  [ -z "$TFILES" ] #  No trainfile path provided
  then
    TFILES="training_files"
  fi
  if grep -Fxq "Classifier training complete using BLAST: $BLAST" "${TFILES}"/training_check.txt # If trainfile path doesn't exist or is empty
  then
    echo "Classifying without training..."
  else
    echo "Cannot classify without existing training files, please specify -t"
		exit 1
	fi
fi
if [ -f "$PATHFILE" ] # First try in local directory
then
  echo "Using local pathfile $PATHFILE"
  source "$PATHFILE"
else # Then try in package directory.
  echo "Pathfile input not found in local directory ..."
  DIR=$(conda list | head -n 1 | rev | cut -d" " -f1 | rev | cut -d: -f1)
  PATHFILE=$DIR"/pkgs/constax-$VERSION-$BUILD/opt/constax-$VERSION/pathfile.txt"
  if [ -f "$PATHFILE" ]
  then
    sed -i "s|=.*/opt/constax|=$DIR/pkgs/constax-$VERSION-$BUILD/opt/constax|g" "$PATHFILE"
    source "$PATHFILE"
  else
    echo "Pathfile input not found at $PATHFILE ..."
  fi
fi
# Check for user input paths
if [ $(command -v "$SINTAXPATH_USER") ] && [[ "$SINTAXPATH_USER" != false ]]
then
  SINTAXPATH="$SINTAXPATH_USER"
fi
if [ $(command -v "$UTAXPATH_USER") ] && [[ "$UTAXPATH_USER" != false ]]
then
  UTAXPATH="$UTAXPATH_USER"
fi
if [ -f "$RDPPATH_USER" ] [ [ $(command -v "$RPDPATH_USER") ] && [[ "$RDPPATH_USER" != false ]] ]
then
  RDPPATH="$RDPPATH_USER"
fi
if [ -d "$CONSTAXPATH_USER" ]
then
  CONSTAXPATH="$CONSTAXPATH_USER"
fi

if $MSU_HPCC
then
  SINTAXPATH=/mnt/research/rdp/public/thirdParty/usearch10.0.240_i86linux64
  UTAXPATH=/mnt/research/rdp/public/thirdParty/usearch8.1.1831_i86linux64
  RDPPATH=/mnt/research/rdp/public/RDPTools/classifier.jar
  CONSTAXPATH=/mnt/ufs18/rs-022/bonito_lab/CONSTAX_May2020
elif $BLAST && [ $(command -v blastn) ] && [ $(command -v "$SINTAXPATH") ] && [ [ $(command java -jar "$RDPPATH" > /dev/null 2>&1) ] || [ $(command -v "$RDPPATH") ] ] && [ -d "$CONSTAXPATH" ]
then
  echo "All needed executables exist."
  echo "SINTAX: $SINTAXPATH"
  echo "RDP: $RDPPATH"
  echo "CONSTAX: $CONSTAXPATH"
elif ! $BLAST && [ $(command -v "$SINTAXPATH") ] && [ [ $(command java -jar "$RDPPATH" > /dev/null 2>&1) ] || [ $(command -v "$RDPPATH") ] ] && [ -d "$CONSTAXPATH" ] && [ $(command -v "$UTAXPATH") ]
then
  echo "All needed executables exist."
  echo "SINTAX: $SINTAXPATH"
  echo "RDP: $RDPPATH"
  echo "UTAX: $UTAXPATH"
  echo "CONSTAX: $CONSTAXPATH"
else
  echo "Please specify --msu_hpcc if using it, otherwise specify paths for --sintax_path,"
  echo "--rdp_path, --utax_path (if not using BLAST), and --constax_path"
  echo "SINTAX: $SINTAXPATH"
  if ! [ $(command -v "$SINTAXPATH") ] ; then echo "SINTAX not executable" ; fi
  echo "RDP: $RDPPATH"
  if ! [ $(command -v java -jar "$RDPPATH") ] && ! [ $(command -v "$RDPPATH") ] ; then echo "RDP not executable alone or by java -jar" ; fi
  echo "UTAX: $UTAXPATH"
  if ! $BLAST &&  ! [ $(command -v "$UTAXPATH") ] ; then echo "UTAX not executable" ; fi
  if $BLAST &&  ! [ $(command -v blastn) ] ; then echo "BLAST not executable" ; fi
  echo "CONSTAX: $CONSTAXPATH"
  if [ -d "$CONSTAXPATH" ] ; then echo "CONSTAX directory not found" ; fi
  exit 1
fi
if ! $BLAST  && [ $(echo "$UTAXPATH" | grep -oP "(?<=usearch).*?(?=\.)") -gt 9 ]
then
  echo "USEARCH executable must be version 9.X or lower to use UTAX"
  exit 1
fi

base=$(basename -- ${DB%.fasta})

FORMAT=$(python "$CONSTAXPATH"/detect_format.py -d "$DB" -t "$TFILES" 2>&1)

echo "Memory size: "$MEM"mb"

if [[ "$FORMAT" == "null" ]]
then
  exit 1
fi

if $TRAIN
then
	python "$CONSTAXPATH"/FormatRefDB.py -d "$DB" -t "$TFILES" -f $FORMAT -p "$CONSTAXPATH"

  echo "__________________________________________________________________________"
	echo "Training SINTAX Classifier"
  if [ $(echo "$SINTAXPATH" | grep -oP "(?<=usearch).*?(?=\.)") -lt 11 2> /dev/null ]
  then
  	"$SINTAXPATH" -makeudb_sintax "${TFILES}/${base}"__UTAX.fasta -output ${TFILES}/sintax.db
  else
    "$SINTAXPATH" -makeudb_usearch "${TFILES}/${base}"__UTAX.fasta -output ${TFILES}/sintax.db
  fi
  if $BLAST
  then
    echo "__________________________________________________________________________"
  	echo "Training BLAST Classifier"
    if $MSU_HPCC
    then
      module load BLAST
    fi

    makeblastdb -in "${TFILES}/${base}"__RDP_trained.fasta -dbtype nucl -out "${TFILES}/${base}"__BLAST
  else
    echo "__________________________________________________________________________"
    echo "Training UTAX Classifier"

    "$UTAXPATH" -utax_train "${TFILES}/${base}"__UTAX.fasta -report ${TFILES}/utax_db_report.txt -taxconfsout ${TFILES}/utax.tc \
    -utax_splitlevels NVpcofgs -utax_trainlevels kpcofgs -log ${TFILES}/utax_train.log -report ${TFILES}/utax_report.txt

    "$UTAXPATH" -makeudb_utax "${TFILES}/${base}"__UTAX.fasta -taxconfsin ${TFILES}/utax.tc -output ${TFILES}/utax.db \
     -log ${TFILES}/make_udb.log -report ${TFILES}/utax_report.txt

  fi
	echo "__________________________________________________________________________"
  echo "Training RDP Classifier"

  if [ $(command -v "$RDPPATH" > /dev/null 2>&1) ]
  then
    "$RDPPATH" train -o "${TFILES}/." -s "${TFILES}/${base}"__RDP_trained.fasta -t "${TFILES}/${base}"__RDP_taxonomy_trained.txt
  else
    java -Xmx"$MEM"m -jar "$RDPPATH" train -o "${TFILES}/." -s "${TFILES}/${base}"__RDP_trained.fasta -t "${TFILES}/${base}"__RDP_taxonomy_trained.txt
  fi

  # The rRNAClassifier.properties file should be in one of these two places
  if [ -f "$CONSTAXPATH"/rRNAClassifier.properties ]
  then
    cp "$CONSTAXPATH"/rRNAClassifier.properties "${TFILES}"/
  elif [ -f "${RDPPATH%dist/classifier.jar}"/samplefiles/rRNAClassifier.properties ]
  then
    cp "${RDPPATH%dist/classifier.jar}"/samplefiles/rRNAClassifier.properties "${TFILES}"/
  elif [ -f "${RDPPATH%.jar}"/samplefiles/rRNAClassifier.properties ]
  then
    cp "${RDPPATH%.jar}"/samplefiles/rRNAClassifier.properties "${TFILES}"/
  else
    echo "Cannot locate rRNAClassifier.properties file, please place in $CONSTAXPATH or RDPTools/classifier/samplefiles"
  fi
  echo "Classifier training complete using BLAST: $BLAST" > "${TFILES}"/training_check.txt

	# -Xmx set to memory GB you want to use

fi

echo "__________________________________________________________________________"
echo "Assigning taxonomy to OTU's representative sequences"

FRM_INPUT=$(python "$CONSTAXPATH"/check_input_names.py -i "$INPUT" 2>&1)

"$SINTAXPATH" -sintax "$FRM_INPUT" -db "${TFILES}"/sintax.db -tabbedout "$TAX"/otu_taxonomy.sintax -strand both -sintax_cutoff $CONF -threads $NTHREADS
if [[ "$SINTAXPATH" == vsearch ]]
then
  sed -i 's|([0-1][.][0-9]\{2\}|&00|g' "$TAX"/otu_taxonomy.sintax
fi
if $BLAST
then

  if $MSU_HPCC && ! $TRAIN
  then
    module load BLAST
  fi

  blastn -query "$FRM_INPUT" -db "${TFILES}/${base}"__BLAST -num_threads $NTHREADS -outfmt "7 qacc sacc evalue bitscore pident qcovs" -max_target_seqs $MAX_HITS > "$TAX"/blast.out
  python "$CONSTAXPATH"/blast_to_df.py -i "$TAX"/blast.out -o "$TAX"/otu_taxonomy.blast -d "$DB" -t "$TFILES" -f $FORMAT
else
  "$UTAXPATH" -utax "$FRM_INPUT" -db "${TFILES}"/utax.db -strand both -utaxout "$TAX"/otu_taxonomy.utax -utax_cutoff $CONF -threads $NTHREADS

fi

if [ $(command -v "$RDPPATH" > /dev/null 2>&1) ]
then
  "$RDPPATH" classify --conf $CONF --format allrank --train_propfile "${TFILES}"/rRNAClassifier.properties -o "$TAX"/otu_taxonomy.rdp "$FRM_INPUT"
else
  java -Xmx"$MEM"m -jar "$RDPPATH" classify --conf $CONF --format allrank --train_propfile "${TFILES}"/rRNAClassifier.properties -o "$TAX"/otu_taxonomy.rdp "$FRM_INPUT"
fi

echo "__________________________________________________________________________"
echo "Combining Taxonomies"

if [ -f "$ISOLATES" ] && [ -s "$ISOLATES" ]
then
  echo "Comparing to Isolates"
  USE_ISOS=True

  if $MSU_HPCC && ! $BLAST
  then
    module load BLAST
  fi

  makeblastdb -in "$ISOLATES" -dbtype nucl -out "${TFILES}/${ISOLATES%.fasta}"__BLAST

  blastn -query "$FRM_INPUT" -db "${TFILES}/${ISOLATES%.fasta}"__BLAST -num_threads $NTHREADS -outfmt "7 qacc sacc evalue bitscore pident qcovs" -max_target_seqs 1 -evalue 0.00001 > "$TAX"/isolates_blast.out
fi
rm "$FRM_INPUT"

if $BLAST
then
  python "$CONSTAXPATH"/CombineTaxonomy.py -c $CONF -o "$OUTPUT/" -x "$TAX/" -b -e $EVALUE -m $MAX_HITS -p $P_IDEN -f $FORMAT -d "$DB" -t "$TFILES" -i $USE_ISOS -s $CONSERVATIVE
else
  python "$CONSTAXPATH"/CombineTaxonomy.py -c $CONF -o "$OUTPUT/" -x "$TAX/" -f $FORMAT -d "$DB" -t "$TFILES" -i $USE_ISOS -s $CONSERVATIVE
fi
if $MSU_HPCC
then
  module load GCC/8.3.0  OpenMPI/3.1.4
  module load R
fi

# plot R
# Rscript /mnt/research/common-data/Bio/UserDownloads/CONSTAX/R/ComparisonBars.R -o "$OUTPUT/"

if $MAKE_PLOT && $BLAST
then
  # Rscript /mnt/ufs18/rs-022/bonito_lab/CONSTAX_May2020/ComparisonBars_w_blast.R "$OUTPUT/" FALSE
  Rscript "$CONSTAXPATH"/ComparisonBars.R "$OUTPUT/" TRUE $FORMAT
elif $MAKE_PLOT
then
  # Rscript /mnt/ufs18/rs-022/bonito_lab/CONSTAX_May2020/ComparisonBars_w_blast.R "$OUTPUT/" TRUE
  Rscript "$CONSTAXPATH"/ComparisonBars.R "$OUTPUT/" FALSE $FORMAT
fi
