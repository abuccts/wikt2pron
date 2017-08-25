#!/bin/bash

DATA_TRAIN_SRC="http://www.openslr.org/resources/12/train-clean-100.tar.gz"
DATA_TEST_SRC="http://www.openslr.org/resources/12/test-clean.tar.gz"
DATA_WAV=./wav


echo "--- Starting LibriSpeech data download (may take some time) ..."
wget DATA_TRAIN_SRC || exit 1
wget DATA_TEST_SRC || exit 1
 
mkdir -p ${DATA_WAV}

echo "--- Starting LibriSpeech archives extraction ..."
for a in ./*.tar.gz; do
  tar -C ${DATA_WAV} -xzf $a
done
