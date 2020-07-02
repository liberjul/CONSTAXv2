#!/bin/bash -login

echo "################################################################"
echo "###############*** This is CONSTAX v.2 ***######################"
echo "#                                                              #"
echo "#                     MIT License                              #"
echo "#                 Copyright (C) 2020                           #"
echo "#   Julian Liber, Natalie Vandepol, Kristi Gadnetz,            #"
echo "#     Gian Maria Niccolo' Benucci, Gregory Bonito              #"
echo "#                                                              #"
echo "#      https://github.com/Gian77/CONSTAX                       #"
echo "################################################################"


### Parse variable inputs
TEMP=`getopt -o c:n:m:e:p:d:i:o:x:tbhf: --long conf:,num_threads:,max_hits:,evalue:,p_iden:,db:,input:,output:,tax:,train,blast,msu_hpcc,help,trainfile:,mem:,sintax_path:,utax_path:,rdp_path:,constax_path: \
             -n 'constax' -- "$@"`

if [ $? != 0 ]
then
  echo "Terminating..." >&2
  echo ""
  echo "Usage: ./constax.sh [OPTION] ..."
  echo "Classify input OTU sequences by CONSTAX consesus taxonomy algorithm"
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
  echo "--msu_hpcc                                          If specified, use executable paths on Michigan State University HPCC"
  echo "--mem                                               Memory available to use for RDP, in MB. 32000MB recommended for UNITE, 128000MB for SILVA."
  echo "--sintax_path                                       Path to USEARCH executable for SINTAX classification"
  echo "--utax_path                                         Path to USEARCH executable for UTAX classification"
  echo "--rdp_path                                          Path to RDP classifier.jar file"
  echo "--constax_path                                      Path to CONSTAX scripts"
  echo "-h, --help                                          Display this help and exit"
  exit 1
fi

# Note the quotes around `$TEMP': they are essential!
eval set -- "$TEMP"


TRAIN=false
BLAST=false
HELP=false
MSU_HPCC=false
CONF=0.8
NTHREADS=1
MAX_HITS=10
EVALUE=1
P_IDEN=0.8
DB=/mnt/research/common-data/Bio/UserDownloads/CONSTAX/DB/sh_general_release_fungi_35077_RepS_04.02.2020.fasta
INPUT=otus.fasta
OUTPUT=./outputs
TAX=./taxonomy_assignments
SINTAXPATH=false
UTAXPATH=false
RDPPATH=false
CONSTAXPATH=false
MEM=32000

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
    --rdp_path ) RDPPATH="$2"; shift 2 ;;
    --sintax_path ) SINTAXPATH="$2"; shift 2 ;;
    --utax_path ) UTAXPATH="$2"; shift 2 ;;
    --constax_path ) CONSTAXPATH="${2%/}"; shift 2 ;;
    -t | --train ) TRAIN=true; shift ;;
    -b | --blast ) BLAST=true; shift ;;
		-h | --help ) HELP=true; shift ;;
    --msu_hpcc ) MSU_HPCC=true; shift ;;
    -- ) shift; break ;;
    * ) break ;;
  esac
done

if $HELP
	then
    echo "Usage: ./constax.sh [OPTION] ..."
    echo "Classify input OTU sequences by CONSTAX consesus taxonomy algorithm"
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
    echo "--msu_hpcc                                          If specified, use executable paths on Michigan State University HPCC"
    echo "--mem                                               Memory available to use for RDP, in MB. 32000MB recommended for UNITE, 128000MB for SILVA."
    echo "--sintax_path                                       Path to USEARCH executable for SINTAX classification"
    echo "--utax_path                                         Path to USEARCH executable for UTAX classification"
    echo "--rdp_path                                          Path to RDP classifier.jar file"
    echo "--constax_path                                      Path to CONSTAX scripts"
    echo "-h, --help                                          Display this help and exit"
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
fi

if $TRAIN && ! [ -s "$DB" ]
then
	echo "Database file $DB is non-existent or empty, exiting..."
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
	mkdir $TFILES
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
if $MSU_HPCC
then
  SINTAXPATH=/mnt/research/rdp/public/thirdParty/usearch10.0.240_i86linux64
  UTAXPATH=/mnt/research/rdp/public/thirdParty/usearch8.1.1831_i86linux64
  RDPPATH=/mnt/research/rdp/public/RDPTools/classifier.jar
  CONSTAXPATH=/mnt/ufs18/rs-022/bonito_lab/CONSTAX_May2020
elif $BLAST  && [ -f $SINTAXPATH ] && [ -f $RDPPATH ] && [ -d $CONSTAXPATH ]
then
  echo "All needed executables exist."
elif ! $BLAST  && [ -f $SINTAXPATH ] && [ -f $RDPPATH ] && [ -d $CONSTAXPATH ] && [ -f $UTAXPATH ]
then
  echo "All needed executables exist."
else
  echo "Please specify --msu_hpcc if using it, otherwise specify paths for --sintax_path,"
  echo "--rdp_path, --utax_path (if not using BLAST), and --constax_path"
  exit 1
fi
if ! $BLAST  && [ $(echo $UTAXPATH | grep -oP "(?<=usearch).*?(?=\.)") -gt 9 ]
then
  echo "USEARCH executable must be version 9.X or lower to use UTAX"
  exit 1
fi

# Execute the python script, passing as the first argument the value of the variable ref_database declared in sconfig
base=$(basename -- ${DB%.fasta})

FORMAT=$(python $CONSTAXPATH/detect_format.py -d $DB -t $TFILES 2>&1)

echo "Memory size: "$MEM"mb"

if [[ "$FORMAT" == "null" ]]
then
  exit 1
fi

# UTAX_VER=
if $TRAIN
then
	python $CONSTAXPATH/FormatRefDB.py -d $DB -t $TFILES -f $FORMAT -p $CONSTAXPATH

  echo "__________________________________________________________________________"
	echo "Training SINTAX Classifier"
  if [ $(echo $SINTAXPATH | grep -oP "(?<=usearch).*?(?=\.)") -lt 11 ]
  then
  	$SINTAXPATH -makeudb_sintax "${TFILES}/${base}"__UTAX.fasta -output ${TFILES}/sintax.db
  else
    $SINTAXPATH -makeudb_usearch "${TFILES}/${base}"__UTAX.fasta -output ${TFILES}/sintax.db
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

    $UTAXPATH -utax_train "${TFILES}/${base}"__UTAX.fasta -report ${TFILES}/utax_db_report.txt -taxconfsout ${TFILES}/utax.tc \
    -utax_splitlevels NVpcofgs -utax_trainlevels kpcofgs -log ${TFILES}/utax_train.log -report ${TFILES}/utax_report.txt

    $UTAXPATH -makeudb_utax "${TFILES}/${base}"__UTAX.fasta -taxconfsin ${TFILES}/utax.tc -output ${TFILES}/utax.db \
     -log ${TFILES}/make_udb.log -report ${TFILES}/utax_report.txt

  fi
	echo "__________________________________________________________________________"
  echo "Training RDP Classifier"

  java -Xmx"$MEM"m -jar $RDPPATH train -o "${TFILES}/." -s "${TFILES}/${base}"__RDP_trained.fasta -t "${TFILES}/${base}"__RDP_taxonomy_trained.txt

  cp ${RDPPATH%dist/classifier.jar}/samplefiles/rRNAClassifier.properties "${TFILES}"/

  echo "Classifier training complete using BLAST: $BLAST" > "${TFILES}"/training_check.txt

	# -Xmx set to memory GB you want to use

fi

echo "__________________________________________________________________________"
echo "Assigning taxonomy to OTU's representative sequences"

$SINTAXPATH -sintax "$INPUT" -db "${TFILES}"/sintax.db -tabbedout "$TAX"/otu_taxonomy.sintax -strand both -sintax_cutoff $CONF -threads $NTHREADS
if $BLAST
then

  if $MSU_HPCC && ! $TRAIN
  then
    module load BLAST
  fi

  blastn -query "$INPUT" -db "${TFILES}/${base}"__BLAST -num_threads $NTHREADS -outfmt "7 qacc sacc evalue bitscore pident qcovs" -max_target_seqs $MAX_HITS > "$TAX"/blast.out
  # python /mnt/ufs18/rs-022/bonito_lab/CONSTAX_May2020/blast_to_df.py -i "$TAX"/blast.out -o "$TAX"/otu_taxonomy.blast -d $DB -t $TFILES
  python $CONSTAXPATH/blast_to_df.py -i "$TAX"/blast.out -o "$TAX"/otu_taxonomy.blast -d $DB -t $TFILES -f $FORMAT
else
  $UTAXPATH -utax "$INPUT" -db "${TFILES}"/utax.db -strand both -utaxout "$TAX"/otu_taxonomy.utax -utax_cutoff $CONF -threads $NTHREADS

fi

java -Xmx"$MEM"m -jar $RDPPATH classify --conf $CONF --format allrank --train_propfile "${TFILES}"/rRNAClassifier.properties -o "$TAX"/otu_taxonomy.rdp "$INPUT"


echo "__________________________________________________________________________"
echo "Combining Taxonomies"

    # python /mnt/research/common-data/Bio/UserDownloads/CONSTAX/scripts/CombineTaxonomy.py -c $CONF -o "$OUTPUT/" -x "$TAX/"
if $BLAST
then
  # python /mnt/ufs18/rs-022/bonito_lab/CONSTAX_May2020/CombineTaxonomy_silva.py -c $CONF -o "$OUTPUT/" -x "$TAX/" -b -e $EVALUE -m $MAX_HITS -p $P_IDEN -f $FORMAT -d $DB -t $TFILES
  python $CONSTAXPATH/CombineTaxonomy.py -c $CONF -o "$OUTPUT/" -x "$TAX/" -b -e $EVALUE -m $MAX_HITS -p $P_IDEN -f $FORMAT -d $DB -t $TFILES
else
  # python /mnt/ufs18/rs-022/bonito_lab/CONSTAX_May2020/CombineTaxonomy_silva.py -c $CONF -o "$OUTPUT/" -x "$TAX/" -f $FORMAT -d $DB -t $TFILES
  python $CONSTAXPATH/CombineTaxonomy.py -c $CONF -o "$OUTPUT/" -x "$TAX/" -f $FORMAT -d $DB -t $TFILES
fi
if $MSU_HPCC
then
  module load GCC/8.3.0  OpenMPI/3.1.4
  module load R
fi

# plot R
# Rscript /mnt/research/common-data/Bio/UserDownloads/CONSTAX/R/ComparisonBars.R -o "$OUTPUT/"
if $BLAST
then
  # Rscript /mnt/ufs18/rs-022/bonito_lab/CONSTAX_May2020/ComparisonBars_w_blast.R "$OUTPUT/" FALSE
  Rscript $CONSTAXPATH/ComparisonBars.R "$OUTPUT/" TRUE $FORMAT
else
  # Rscript /mnt/ufs18/rs-022/bonito_lab/CONSTAX_May2020/ComparisonBars_w_blast.R "$OUTPUT/" TRUE
  Rscript $CONSTAXPATH/ComparisonBars.R "$OUTPUT/" FALSE $FORMAT
fi
