#!/bin/bash -login

VERSION=2.0.18; BUILD=0; PREFIX=placehold

echo "Welcome to CONSTAX version $VERSION build $BUILD - The CONSensus TAXonomy classifier"
echo "This software is distributed under MIT License"
echo "© Copyright 2022, Julian A. Liber, Gian M. N. Benucci & Gregory M. Bonito"
echo "https://github.com/liberjul/CONSTAXv2"
echo "https://constax.readthedocs.io/"
echo ""

echo "Please cite us as:"
echo "CONSTAX2: Improved taxonomic classification of environmental DNA markers"
echo "Julian Aaron Liber, Gregory Bonito, Gian Maria Niccolò Benucci"
echo "Bioinformatics, Volume 37, Issue 21, 1 November 2021, Pages 3941–3943; doi: https://doi.org/10.1093/bioinformatics/btab347"

if $SHOW_VERSION
then
  echo "CONSTAX version $VERSION build $BUILD"
  exit 1
fi
#Check Python version
python -V > ver_python.txt 2>&1
if grep -Fq "Python 2" ver_python.txt; then exit 2; fi

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
elif [ $ISO_QC -lt 1 2> /dev/null ] || [ $ISO_QC -gt 100 2> /dev/null ] || [ $? == 2 ]
then
  echo "Set --isolates_query_coverage to an integer greater than 0 and less than or equal to  100"
  exit 1
elif [ $ISO_ID -lt 1 2> /dev/null ] || [ $ISO_ID -gt 100 2> /dev/null ] || [ $? == 2 ]
then
  echo "Set --isolates_percent_identity to an integer greater than 0 and less than or equal to 100"
  exit 1
elif [ $HL_QC -lt 1 2> /dev/null ] || [ $HL_QC -gt 100 2> /dev/null ] || [ $? == 2 ]
then
  echo "Set --high_level_query_coverage to an integer greater than 0 and less than 100"
  exit 1
elif [ $HL_ID -lt 1 2> /dev/null ] || [ $HL_ID -gt 100 2> /dev/null ] || [ $? == 2 ]
then
  echo "Set --high_level_percent_identity to an integer greater than 0 and less than 100"
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
elif [[ "$INPUT" != *.fasta ]] && [[ "$INPUT" != *.fa ]] && [[ "$INPUT" != *.fna ]]
then
  echo "Input file $INPUT must end with .fasta, .fa, or .fna; exiting..."
  exit 1
fi
if [[ "$KEYWORD" == "null" ]]
then
  if ! [ -s "$DB" ]
  then
  	echo "Database file $DB is non-existent or empty, exiting..."
    exit 1
  elif [[ "$DB" != *.fasta ]] && [[ "$DB" != *.fa ]] && [[ "$DB" != *.fna ]]
  then
    echo "Database file $DB must end with .fasta, .fa, or .fna; exiting..."
    exit 1
  fi
  if [ -d "$OUTPUT" ]  && ! [ -z "$(ls -A $OUTPUT)" ]
  then
  	echo "Overwriting previous classification..."
  fi
  if [ -d "$TAX" ]  && ! [ -z "$(ls -A $TAX)" ]
  then
  	echo "Overwriting previous taxonomy assignments..."
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
      echo "Performing training and overwriting training files..."
    fi
  else # Training not true
    if  [ -z "$TFILES" ] #  No trainfile path provided
    then
      TFILES="training_files"
    fi
    if grep -Fxq "Classifier training complete using BLAST: $BLAST" "${TFILES}"/training_check.txt # If trainfile path doesn't exist or is empty
    then
      echo "Classifying without training..."
      if [[ "$(blastn -version | grep -o "blastn: 2[.].*" | head -n1 | cut -d' ' -f2)" != "$(grep -o 'BLAST version 2[.].*' ${TFILES}/training_check.txt | tail -n1 | cut -d' ' -f3)" ]]
      then
        echo "BLAST executable version does not match the version used to generate the training files, "
        echo "if BLAST Database error occurs, change your executable or use -t flag."
      elif ! grep -Fxq "SINTAX executable ${SINTAXPATH##*/}" "${TFILES}"/training_check.txt
      then
        echo "SINTAX executable does not match the executable used to generate the training files, "
        echo "if SINTAX error occurs, change your executable or use -t flag."
      fi
    else
      echo "Cannot classify without existing training files, please specify -t"
  		exit 1
  	fi
  fi
fi
if [ -f "$PATHFILE" ] # First try user-suppplied pathfile
then
  echo "Using the user-supplied pathfile at $PATHFILE"
  source "$PATHFILE"
elif [ -f "pathfile.txt" ] # Next try in local directory
then
  echo "Using local pathfile.txt"
  source pathfile.txt
else # Then try in package directory.
  echo "Pathfile input not found in local directory ..."
  DIR=$(conda list | head -n 1 | rev | cut -d' ' -f1 | rev | cut -d: -f1)
  PATHFILE=$DIR"/pkgs/constax-$VERSION-$BUILD/opt/constax-$VERSION/pathfile.txt"
  if [ -f "$PATHFILE" ]; then source $PATHFILE; echo "Pathfile input found at $PATHFILE ..."; else echo "Pathfile input not found at $PATHFILE ..."; fi
  PATHFILE=$DIR"/pkgs/constax-$VERSION-$BUILD_STRING/opt/constax-$VERSION/pathfile.txt"
  if [ -f "$PATHFILE" ]; then source $PATHFILE; echo "Pathfile input found at $PATHFILE ..."; else echo "Pathfile input not found at $PATHFILE ..."; fi
  PATHFILE=$DIR"/opt/constax-$VERSION/pathfile.txt"
  if [ -f "$PATHFILE" ]; then source $PATHFILE; echo "Pathfile input found at $PATHFILE ..."; else echo "Pathfile input not found at $PATHFILE ..."; fi
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
if [[ "$RDPPATH_USER" != false ]]
then
  RDPPATH="$RDPPATH_USER"
fi
if [ -d "$CONSTAXPATH_USER" ]
then
  CONSTAXPATH="$CONSTAXPATH_USER"
fi

if $MSU_HPCC
then
  echo "Using paths for the MSU HPCC ..."
  SINTAXPATH=/mnt/research/rdp/public/thirdParty/usearch10.0.240_i86linux64
  UTAXPATH=/mnt/research/rdp/public/thirdParty/usearch8.1.1831_i86linux64
  RDPPATH=/mnt/research/rdp/public/RDPTools/classifier.jar
  CONSTAXPATH=/mnt/ufs18/rs-022/bonito_lab/CONSTAX_May2020
elif ! [ -d "$CONSTAXPATH" ]
then
  echo "CONSTAX directory not found"
  exit 1
elif [[ "$KEYWORD" != "null" ]]
then
  python "$CONSTAXPATH"/fasta_select_by_keyword.py -i "$INPUT" -o "$OUTPUT" -k $KEYWORD
  echo "Filtered file output to $OUTPUT"
  exit 1
elif $BLAST && [ $(command -v blastn) ] && [ $(command -v "$SINTAXPATH") ] && [ [ $(command java -jar "$RDPPATH" > /dev/null 2>&1) ] || [ $(command -v "$RDPPATH") ] ]
then
  echo "All needed executables exist."
  echo "SINTAX: $SINTAXPATH"
  echo "RDP: $RDPPATH"
  echo "CONSTAX: $CONSTAXPATH"
elif ! $BLAST && [ $(command -v "$SINTAXPATH") ] && [ [ $(command java -jar "$RDPPATH" > /dev/null 2>&1) ] || [ $(command -v "$RDPPATH") ] ] && [ $(command -v "$UTAXPATH") ]
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
  if ! $BLAST &&  ! [ $(command -v "$UTAXPATH") ] ; then echo "UTAX not executable. Did you mean to use -b/--blast flag?" ; fi
  if $BLAST &&  ! [ $(command -v blastn) ] ; then echo "BLAST not executable" ; fi
  echo "CONSTAX: $CONSTAXPATH"
fi
if ! $BLAST  && [ $(echo "$UTAXPATH" | sed -e 's/.*usearch\([0-9]*\).*/\1/') -gt 9 ]
then
  echo "USEARCH executable must be version 9.X or lower to use UTAX"
  exit 1
fi

base=$(basename -- ${DB%.*})
echo "python $CONSTAXPATH/detect_format.py -d $DB 2>&1"
FORMAT=$(python "$CONSTAXPATH"/detect_format.py -d "$DB" 2>&1)
if [[ $FORMAT == "INVALID" ]]
then
  echo "Database file $DB must be in UNITE or SILVA format, exiting..."
  exit 1
fi
echo "Memory size: "$MEM"mb"

if [[ "$FORMAT" == "null" ]]
then
  exit 1
fi

if $CHECK
then
  echo "All checks passed, rerun without --check flag."
  exit 0
fi
if ! $COMBINE_ONLY
then
  if $TRAIN
  then
    echo "python $CONSTAXPATH/FormatRefDB.py -d $DB -t $TFILES -f $FORMAT -p $CONSTAXPATH"
  	python "$CONSTAXPATH"/FormatRefDB.py -d "$DB" -t "$TFILES" -f $FORMAT -p "$CONSTAXPATH"

    echo "__________________________________________________________________________"
  	echo "Training SINTAX Classifier"
    if [ $(echo "$SINTAXPATH" | sed -e 's/.*usearch\([0-9]*\).*/\1/') -lt 11 2> /dev/null ]
    then
      echo "$SINTAXPATH -makeudb_sintax ${TFILES}/${base}__UTAX.fasta -output ${TFILES}/sintax.db"
    	"$SINTAXPATH" -makeudb_sintax "${TFILES}/${base}"__UTAX.fasta -output ${TFILES}/sintax.db
    else
      echo "$SINTAXPATH -makeudb_usearch ${TFILES}/${base}__UTAX.fasta -output ${TFILES}/sintax.db"
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
      echo "makeblastdb -in ${TFILES}/${base}__RDP_trained.fasta -dbtype nucl -out ${TFILES}/${base}__BLAST"
      makeblastdb -in "${TFILES}/${base}"__RDP_trained.fasta -dbtype nucl -out "${TFILES}/${base}"__BLAST
    else
      echo "__________________________________________________________________________"
      echo "Training UTAX Classifier"
      echo "$UTAXPATH -utax_train ${TFILES}/${base}__UTAX.fasta -report ${TFILES}/utax_db_report.txt -taxconfsout ${TFILES}/utax.tc -utax_splitlevels NVpcofgs -utax_trainlevels kpcofgs -log ${TFILES}/utax_train.log -report ${TFILES}/utax_report.txt"
      "$UTAXPATH" -utax_train "${TFILES}/${base}"__UTAX.fasta -report ${TFILES}/utax_db_report.txt -taxconfsout ${TFILES}/utax.tc \
      -utax_splitlevels NVpcofgs -utax_trainlevels kpcofgs -log ${TFILES}/utax_train.log -report ${TFILES}/utax_report.txt

      echo "$UTAXPATH -makeudb_utax ${TFILES}/${base}__UTAX.fasta -taxconfsin ${TFILES}/utax.tc -output ${TFILES}/utax.db -log ${TFILES}/make_udb.log -report ${TFILES}/utax_report.txt"
      "$UTAXPATH" -makeudb_utax "${TFILES}/${base}"__UTAX.fasta -taxconfsin ${TFILES}/utax.tc -output ${TFILES}/utax.db \
       -log ${TFILES}/make_udb.log -report ${TFILES}/utax_report.txt

    fi
  	echo "__________________________________________________________________________"
    echo "Training RDP Classifier"

    if [ $(command -v "$RDPPATH") ]
    then
      echo "$RDPPATH train -o ${TFILES}/. -s ${TFILES}/${base}__RDP_trained.fasta -t ${TFILES}/${base}__RDP_taxonomy_trained.txt -Xmx$MEMm > rdp_train.out 2>&1"
      "$RDPPATH" train -o "${TFILES}/." -s "${TFILES}/${base}"__RDP_trained.fasta -t "${TFILES}/${base}"__RDP_taxonomy_trained.txt -Xmx"$MEM"m > rdp_train.out 2>&1
    else
      echo "java -Xmx$MEMm -jar $RDPPATH train -o ${TFILES}/. -s ${TFILES}/${base}__RDP_trained.fasta -t ${TFILES}/${base}__RDP_taxonomy_trained.txt > rdp_train.out 2>&1"
      java -Xmx"$MEM"m -jar "$RDPPATH" train -o "${TFILES}/." -s "${TFILES}/${base}"__RDP_trained.fasta -t "${TFILES}/${base}"__RDP_taxonomy_trained.txt > rdp_train.out 2>&1
    fi
    cat rdp_train.out
    if grep -Fq "duplicate taxon name" rdp_train.out
    then
      echo "RDP training error, redoing with duplicate taxa"
      echo "python $CONSTAXPATH/FormatRefDB.py -d $DB -t $TFILES -f $FORMAT -p $CONSTAXPATH --dup"
      python "$CONSTAXPATH"/FormatRefDB.py -d "$DB" -t "$TFILES" -f $FORMAT -p "$CONSTAXPATH" --dup
      if [ $(command -v "$RDPPATH") ]
      then
        echo "$RDPPATH train -o ${TFILES}/. -s ${TFILES}/${base}__RDP_trained.fasta -t ${TFILES}/${base}__RDP_taxonomy_trained.txt -Xmx$MEMm > rdp_train.out 2>&1"
        "$RDPPATH" train -o "${TFILES}/." -s "${TFILES}/${base}"__RDP_trained.fasta -t "${TFILES}/${base}"__RDP_taxonomy_trained.txt -Xmx"$MEM"m > rdp_train.out 2>&1
      else
        echo "java -Xmx$MEMm -jar $RDPPATH train -o ${TFILES}/. -s ${TFILES}/${base}__RDP_trained.fasta -t ${TFILES}/${base}__RDP_taxonomy_trained.txt > rdp_train.out 2>&1"
        java -Xmx"$MEM"m -jar "$RDPPATH" train -o "${TFILES}/." -s "${TFILES}/${base}"__RDP_trained.fasta -t "${TFILES}/${base}"__RDP_taxonomy_trained.txt > rdp_train.out 2>&1
      fi
      if [ -s rdp_train.out ]
      then
        cat rdp_train.out
        exit 1
      else
        echo "RDP training error overcome, continuing with classification after SINTAX is retrained"
        if [ $(echo "$SINTAXPATH" | sed -e 's/.*usearch\([0-9]*\).*/\1/') -lt 11 2> /dev/null ]
        then
          echo "$SINTAXPATH -makeudb_sintax ${TFILES}/${base}__UTAX.fasta -output ${TFILES}/sintax.db"
          "$SINTAXPATH" -makeudb_sintax "${TFILES}/${base}"__UTAX.fasta -output ${TFILES}/sintax.db
        else
          echo "$SINTAXPATH -makeudb_usearch ${TFILES}/${base}__UTAX.fasta -output ${TFILES}/sintax.db"
          "$SINTAXPATH" -makeudb_usearch "${TFILES}/${base}"__UTAX.fasta -output ${TFILES}/sintax.db
        fi
      fi
      if [ -f rdp_train.out ]
      then
        rm rdp_train.out
      fi
    fi
    # The rRNAClassifier.properties file should be in one of these two places
    if [ -f "$CONSTAXPATH"/rRNAClassifier.properties ]
    then
      echo "cp $CONSTAXPATH/rRNAClassifier.properties ${TFILES}/"
      cp "$CONSTAXPATH"/rRNAClassifier.properties "${TFILES}"/
    elif [ -f "${RDPPATH%dist/classifier.jar}"/samplefiles/rRNAClassifier.properties ]
    then
      echo "cp ${RDPPATH%dist/classifier.jar}/samplefiles/rRNAClassifier.properties ${TFILES}/"
      cp "${RDPPATH%dist/classifier.jar}"/samplefiles/rRNAClassifier.properties "${TFILES}"/
    elif [ -f "${RDPPATH%.jar}"/samplefiles/rRNAClassifier.properties ]
    then
      echo "cp ${RDPPATH%.jar}/samplefiles/rRNAClassifier.properties ${TFILES}/"
      cp "${RDPPATH%.jar}"/samplefiles/rRNAClassifier.properties "${TFILES}"/
    else
      echo "Cannot locate rRNAClassifier.properties file, please place in $CONSTAXPATH or RDPTools/classifier/samplefiles"
    fi
    echo "Classifier training complete using BLAST: $BLAST" >> "${TFILES}"/training_check.txt
    if $BLAST; then echo "BLAST version $(blastn -version | grep -o "blastn: 2[.].*" | head -n1 | cut -d' ' -f2)" >> "${TFILES}"/training_check.txt; fi
    echo "SINTAX executable ${SINTAXPATH##*/}" >> "${TFILES}"/training_check.txt

  	# -Xmx set to memory in MB you want to use

  fi

  echo "__________________________________________________________________________"
  echo "Assigning taxonomy to OTU's representative sequences"
  echo "python $CONSTAXPATH/check_input_names.py -i $INPUT"
  FRM_INPUT=$(python "$CONSTAXPATH"/check_input_names.py -i "$INPUT" >&1)

  echo "$SINTAXPATH -sintax $FRM_INPUT -db ${TFILES}/sintax.db -tabbedout $TAX/otu_taxonomy.sintax -strand both -sintax_cutoff $CONF -threads $NTHREADS"
  "$SINTAXPATH" -sintax "$FRM_INPUT" -db "${TFILES}"/sintax.db -tabbedout "$TAX"/otu_taxonomy.sintax -strand both -sintax_cutoff $CONF -threads $NTHREADS
  if [[ ${SINTAXPATH##*/} == "vsearch" ]]
  then
    echo "sed -i'' -e 's|([0-1][.][0-9]\{2\}|&00|g' $TAX/otu_taxonomy.sintax"
    sed -i'' -e 's|([0-1][.][0-9]\{2\}|&00|g' "$TAX"/otu_taxonomy.sintax
  fi
  if $BLAST
  then

    if $MSU_HPCC && ! $TRAIN
    then
      echo "module load BLAST"
      module load BLAST
    fi
    # workaround code for blast getting stuck
    echo "python $CONSTAXPATH/split_inputs.py -i $FRM_INPUT"
    python "$CONSTAXPATH"/split_inputs.py -i "$FRM_INPUT"

    echo "> $TAX/blast.out"
    echo > "$TAX"/blast.out
    for i in ${FRM_INPUT%.fasta}_*".fasta"
    do
      echo "blastn -query $i -db $TFILES/$base__BLAST -num_threads $NTHREADS -outfmt 7 qacc sacc evalue bitscore pident qcovs -max_target_seqs $MAX_HITS >> $TAX/blast.out"
      blastn -query $i -db "$TFILES"/"$base"__BLAST -num_threads $NTHREADS -outfmt "7 qacc sacc evalue bitscore pident qcovs" -max_target_seqs $MAX_HITS >> "$TAX"/blast.out
      rm $i
    done

    echo "python $CONSTAXPATH/blast_to_df.py -i $TAX/blast.out -o $TAX/otu_taxonomy.blast -d $DB -t $TFILES -f $FORMAT"
    python "$CONSTAXPATH"/blast_to_df.py -i "$TAX"/blast.out -o "$TAX"/otu_taxonomy.blast -d "$DB" -t "$TFILES" -f $FORMAT
  else
    echo "$UTAXPATH -utax $FRM_INPUT -db ${TFILES}/utax.db -strand both -utaxout $TAX/otu_taxonomy.utax -utax_cutoff $CONF -threads $NTHREADS"
    "$UTAXPATH" -utax "$FRM_INPUT" -db "${TFILES}"/utax.db -strand both -utaxout "$TAX"/otu_taxonomy.utax -utax_cutoff $CONF -threads $NTHREADS

  fi

  if [ $(command -v "$RDPPATH") ]
  then
    echo "$RDPPATH classify --conf $CONF --format allrank --train_propfile ${TFILES}/rRNAClassifier.properties -o $TAX/otu_taxonomy.rdp $FRM_INPUT -Xmx$MEMm"
    "$RDPPATH" classify --conf $CONF --format allrank --train_propfile "${TFILES}"/rRNAClassifier.properties -o "$TAX"/otu_taxonomy.rdp "$FRM_INPUT" -Xmx"$MEM"m
  else
    echo "java -Xmx$MEMm -jar $RDPPATH classify --conf $CONF --format allrank --train_propfile ${TFILES}/rRNAClassifier.properties -o $TAX/otu_taxonomy.rdp $FRM_INPUT"
    java -Xmx"$MEM"m -jar "$RDPPATH" classify --conf $CONF --format allrank --train_propfile "${TFILES}"/rRNAClassifier.properties -o "$TAX"/otu_taxonomy.rdp "$FRM_INPUT"
  fi

  echo "__________________________________________________________________________"

  if [ -f "$ISOLATES" ] && [ -s "$ISOLATES" ]
  then
    echo "Comparing to Isolates"
    USE_ISOS=True

    if $MSU_HPCC && ! $BLAST
    then
      echo "module load BLAST"
      module load BLAST
    fi
    echo "python $CONSTAXPATH/check_input_names.py -i $ISOLATES -n $TAX/isolates_formatted.fasta"
    python "$CONSTAXPATH"/check_input_names.py -i "$ISOLATES" -n "$TAX/"isolates_formatted.fasta

    echo "makeblastdb -in $TAX/isolates_formatted.fasta -dbtype nucl -out $TAX/$(basename -- ${ISOLATES%.*})__BLAST"
    makeblastdb -in "$TAX/"isolates_formatted.fasta -dbtype nucl -out "$TAX/$(basename -- ${ISOLATES%.*})"__BLAST
    rm "$TAX/"isolates_formatted.fasta

    echo "blastn -query $FRM_INPUT -db $TAX/$(basename -- ${ISOLATES%.*})__BLAST -num_threads $NTHREADS -outfmt 7 qacc sacc evalue bitscore pident qcovs -max_target_seqs 1 -evalue 0.00001 > $TAX/isolates_blast.out"
    blastn -query "$FRM_INPUT" -db "$TAX/$(basename -- ${ISOLATES%.*})"__BLAST -num_threads $NTHREADS -outfmt "7 qacc sacc evalue bitscore pident qcovs" -max_target_seqs 1 -evalue 0.00001 > "$TAX"/isolates_blast.out
    rm "$TAX/$(basename -- ${ISOLATES%.*})"__BLAST.n*
  fi
  if [ -f "$HL_DB" ] && [ -s "$HL_DB" ]
  then
    echo "High Level Taxonomy Assignment"
    echo "python $CONSTAXPATH/detect_format.py -d $HL_DB 2>&1"
    HL_FMT=$(python "$CONSTAXPATH"/detect_format.py -d "$HL_DB" 2>&1)
    if [[ $HL_FMT == "INVALID" ]]
    then
      echo "High-level taxonomy database file $HL_DB must be in UNITE or SILVA format, exiting..."
      exit 1
    fi
    if $MSU_HPCC && ! $BLAST
    then
      module load BLAST
    fi
    echo "python $CONSTAXPATH/check_input_names.py -i $HL_DB -n $TAX/hl_formatted.fasta --filter"
    python "$CONSTAXPATH"/check_input_names.py -i "$HL_DB" -n "$TAX/"hl_formatted.fasta --filter

    echo "makeblastdb -in $TAX/hl_formatted.fasta -dbtype nucl -out $TAX/$(basename -- ${HL_DB%.*})__BLAST"
    makeblastdb -in "$TAX/"hl_formatted.fasta -dbtype nucl -out "$TAX/$(basename -- ${HL_DB%.*})"__BLAST
    rm "$TAX/"hl_formatted.fasta
    echo "blastn -query $FRM_INPUT -db $TAX/$(basename -- ${HL_DB%.*})__BLAST -num_threads $NTHREADS -outfmt 7 qacc sacc evalue bitscore pident qcovs -max_target_seqs 1 -evalue 0.001 > $TAX/hl_blast.out"
    blastn -query "$FRM_INPUT" -db "$TAX/$(basename -- ${HL_DB%.*})"__BLAST -num_threads $NTHREADS -outfmt "7 qacc sacc evalue bitscore pident qcovs" -max_target_seqs 1 -evalue 0.001 > "$TAX"/hl_blast.out
    rm "$TAX/$(basename -- ${HL_DB%.*})"__BLAST.n*
  else
    echo ""
  fi
  rm "$FRM_INPUT"
fi

echo "Combining Taxonomies"
if $BLAST
then
  echo "python $CONSTAXPATH/CombineTaxonomy.py -c $CONF -o $OUTPUT/ -x $TAX/ -b -e $EVALUE -m $MAX_HITS -p $P_IDEN -f $FORMAT -d $DB -t $TFILES -i $USE_ISOS --hl $HL_FMT --iso_qc $ISO_QC --iso_id $ISO_ID --hl_qc $HL_QC --hl_id $HL_ID -s $CONSERVATIVE -n $CONSISTENT"
  python "$CONSTAXPATH"/CombineTaxonomy.py -c $CONF -o "$OUTPUT/" -x "$TAX/" -b -e $EVALUE -m $MAX_HITS -p $P_IDEN -f $FORMAT -d "$DB" -t "$TFILES" -i $USE_ISOS --hl $HL_FMT --iso_qc $ISO_QC --iso_id $ISO_ID --hl_qc $HL_QC --hl_id $HL_ID -s $CONSERVATIVE -n $CONSISTENT
else
  echo "python $CONSTAXPATH/CombineTaxonomy.py -c $CONF -o $OUTPUT/ -x $TAX/ -f $FORMAT -d $DB -t $TFILES -i $USE_ISOS --hl $HL_FMT --iso_qc $ISO_QC --iso_id $ISO_ID --hl_qc $HL_QC --hl_id $HL_ID -s $CONSERVATIVE -n $CONSISTENT"
  python "$CONSTAXPATH"/CombineTaxonomy.py -c $CONF -o "$OUTPUT/" -x "$TAX/" -f $FORMAT -d "$DB" -t "$TFILES" -i $USE_ISOS --hl $HL_FMT --iso_qc $ISO_QC --iso_id $ISO_ID --hl_qc $HL_QC --hl_id $HL_ID -s $CONSERVATIVE -n $CONSISTENT
fi
if $MSU_HPCC
then
  echo "module load GCC/8.3.0  OpenMPI/3.1.4"
  module load GCC/8.3.0  OpenMPI/3.1.4
  echo "module load R"
  module load R
fi

# plot R
if $MAKE_PLOT && $BLAST
then
  echo "Rscript $CONSTAXPATH/ComparisonBars.R $OUTPUT/ TRUE $FORMAT"
  Rscript "$CONSTAXPATH"/ComparisonBars.R "$OUTPUT/" TRUE $FORMAT
elif $MAKE_PLOT
then
  echo "Rscript $CONSTAXPATH/ComparisonBars.R $OUTPUT/ FALSE $FORMAT"
  Rscript "$CONSTAXPATH"/ComparisonBars.R "$OUTPUT/" FALSE $FORMAT
fi
