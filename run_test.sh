#!/bin/bash -login

./constax.sh -c 0.8 -b -t -i ./test_data/silva_test_query.fa -n 4 -d ./test_data/silva_test_ref.fa -f tf_test_sil -x tax_test_sil -o out_test_sil \
  --mem 4000 -m 3 --isolates ./test_data/silva_test_isos.fa --conservative

./constax.sh -c 0.8 -b -t -i ./test_data/unite_test_query.fa -n 4 -d ./test_data/unite_test_ref.fa -f tf_test_uni -x tax_test_uni -o out_test_uni \
  --mem 4000 -m 3 --isolates ./test_data/unite_test_isos.fa
