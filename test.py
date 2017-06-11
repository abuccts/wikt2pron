# -*- coding: utf-8  -*-

import sys
import mwxml
import pprint
from pywiktionary import Wiktionary

if __name__ == "__main__":
    pageNum = 100
    dumpFile = "../enwiktionary-latest-pages-articles-multistream.xml"

    dump = mwxml.Dump.from_file((open(dumpFile, "rb")))
    wikt = Wiktionary(lang=["English", "French"], CMUBET=True, phoneme_only=False)
    stdout = open(sys.stdout.fileno(), "w", encoding="utf-8", closefd=False)

    entryno = 0
    entrydict = {}
    for page in dump:
        for revision in page:
            if revision.page.namespace == 0:
                title = revision.page.title
                text = revision.text
                entrydict[title] = wikt.pronun(text)
        entryno += 1
        if pageNum is not None and entryno >= pageNum:
            break

#   print(entrydict, file=stdout)
    pprint.pprint(entrydict, stream=stdout)
