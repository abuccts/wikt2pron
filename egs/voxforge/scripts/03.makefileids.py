#!/usr/bin/env python

import os
import re
import random

PROMPTS_FILE = "./etc/PROMPTS"
WAVLIST_FILE = "./etc/wav.lst"

NUMBERS = ["ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"]
PATTERNS = [
    (re.compile("&"), " AND "),
    (re.compile(r"[\-_/\\]"), " "),
    (re.compile("2000"), " TWO THOUSANDS "),
]
PATTERN_NUM = re.compile("[0-9]")
PATTERN_LOW = re.compile("[a-z]")


if __name__ == "__main__":
    prompts = []
    with open(PROMPTS_FILE) as f:
        for line in f:
            line = line.strip()
            if len(line.split()[0].split("/")) != 3:
                continue
            prompts.append(line)

    wavlst = set()
    with open(WAVLIST_FILE) as f:
        for line in f:
            line = line.strip()
            wavlst.add(line)

    no = 0
    fileids, transcription, vocab = [], [], []
    for prompt in prompts:
        filename, sentence = prompt.split(" ", 1)
        filename = filename.split("/")
        if "{}.{}.wav".format(filename[0], filename[2]) not in wavlst:
            continue
        for pattern, string in PATTERNS:
            sentence = pattern.sub(string, sentence)
        sentence = PATTERN_NUM.sub(
            lambda x: " {} ".format(NUMBERS[int(x.group())]), sentence
        )
        sentence = PATTERN_LOW.sub(lambda x: x.group().upper(), sentence)
        sentence = " ".join(sentence.split())
        fileids.append("{}/wav/{}.{}\n".format(
            filename[0], filename[0], filename[2]
        ))
        transcription.append("<s> {} </s> ({}.{})\n".format(
            sentence, filename[0], filename[2]
        ))
        vocab += sentence.split()
        no += 1
        if no % 1000 == 0:
            print "Process {} prompts.".format(no)

    vocab = list(set(vocab))
    vocab.sort()
    vocab = map(lambda x: x + "\n", vocab)
    with open("./etc/voxforge.vocab", "w") as f:
        f.writelines(vocab)

    assert len(fileids) == len(transcription)
    num = len(fileids)
    print "Get {} fileids and transcription, {} vocab.".format(
        num, len(vocab)
    )

    idx = range(num)
    random.shuffle(idx)
    train_fileids, train_transcription = [], []
    test_fileids, test_transcription = [], []
    for i in idx[num//10:]:
        train_fileids.append(fileids[i])
        train_transcription.append(transcription[i])
    for i in idx[:num//10]:
        test_fileids.append(fileids[i])
        test_transcription.append(transcription[i])

    with open("./etc/voxforge_train.fileids", "w") as f:
        f.writelines(train_fileids)
    with open("./etc/voxforge_train.transcription", "w") as f:
        f.writelines(train_transcription)
    with open("./etc/voxforge_test.fileids", "w") as f:
        f.writelines(test_fileids)
    with open("./etc/voxforge_test.transcription", "w") as f:
        f.writelines(test_transcription)

