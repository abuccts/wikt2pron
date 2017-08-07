#!/bin/bash

DATA_WAV=./wav
WAVLIST_FILE=./etc/wav.lst

for dir in ${DATA_WAV}/*; do
  base=$(basename $dir)
  if [ -d ${dir}/flac ]; then
    mkdir -p ${dir}/wav 2>/dev/null
    for flac in ${dir}/flac/*; do
      fname=$(basename "$flac")
      ffmpeg -i ${flac} ${dir}/wav/${fname%.*}.wav
    done
  fi
  for wav in ${dir}/wav/*; do
    mv ${wav} ${dir}/wav/${base}.$(basename "$wav")
  done
done

if [ -f ${WAVLIST_FILE} ]; then
  mv ${WAVLIST_FILE} ${WAVLIST_FILE}.$(date -d "today" +"%Y%m%d%H%M")
fi
for dir in ${DATA_WAV}/*; do
  ls ${dir}/wav >> ${WAVLIST_FILE}
done
