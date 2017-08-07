#!/bin/bash

DATA_WAV=./wav
DATA_ETC=./etc
PROMPTS_FILE=${DATA_ETC}/PROMPTS

mkdir -p ${DATA_ETC} 2>/dev/null

if [ -f ${PROMPTS_FILE} ]; then
  mv ${PROMPTS_FILE} ${PROMPTS_FILE}.$(date -d "today" +"%Y%m%d%H%M")
fi

for dir in ${DATA_WAV}/*; do
  while read line; do
    echo $line >> ${PROMPTS_FILE}
  done < ${dir}/etc/PROMPTS
done
