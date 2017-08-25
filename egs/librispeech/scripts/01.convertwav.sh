#!/bin/bash

declare -a splits=("train-clean" "test-clean")

for split in "${splits[@]}"; do
  for diri in ./wav/${split}/*; do
    for dirj in ${diri}/*; do
      for flac in ${dirj}/*.flac; do
        sox ${flac%.*}.flac ${flac%.*}.wav
      done
    done
  done
done
