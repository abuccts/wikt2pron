#!/usr/bin/env python

import os

SPLITS = ["train", "test"]

if __name__ == "__main__":
    for split in SPLITS:
        fileids, transcription = [], []
        diri = os.listdir("./wav/" + split + "-clean/")
        diri.sort(key=lambda x: int(x))
        for eachdiri in diri:
            dirj = os.listdir("./wav/" + split + "-clean/" + eachdiri)
            dirj.sort(key=lambda x: int(x))
            for eachdirj in dirj:
                inFile = "./wav/{}-clean/{}/{}/{}-{}.trans.txt".format(
                    split, eachdiri, eachdirj, eachdiri, eachdirj
                )
                with open(inFile) as f:
                    for line in f:
                        line = line.strip()
                        fn, trans = line.split(" ", 1)
                        fileids.append("{}-clean/{}/{}/{}\n".format(
                            split, eachdiri, eachdirj, fn
                        ))
                        transcription.append("<s> {} </s> ({})\n".format(
                            trans, fn
                        ))
        with open("./etc/librispeech_" + split + ".fileids", "w") as f:
            f.writelines(fileids)
        with open("./etc/librispeech_" + split + ".transcription", "w") as f:
            f.writelines(transcription)
