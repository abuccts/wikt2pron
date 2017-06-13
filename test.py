"""test.py

Test script for parsing xml dump.
"""

import sys
import pprint

import mwxml
from pywiktionary import Wiktionary


def main():
    """main
    """
    page_num = 10
    dump_file = "../enwiktionary-latest-pages-articles-multistream.xml"

    dump = mwxml.Dump.from_file((open(dump_file, "rb")))
    wikt = Wiktionary(
        lang=["English", "French"],
        cmubet=True,
        phoneme_only=False
    )
    stdout = open(sys.stdout.fileno(), "w", encoding="utf-8", closefd=False)

    entry_no = 0
    entry_dict = {}
    for page in dump:
        for revision in page:
            if revision.page.namespace == 0:
                title = revision.page.title
                text = revision.text
                entry_dict[title] = wikt.pronun(text)
        entry_no += 1
        if page_num and entry_no >= page_num:
            break

#   print(entry_dict, file=stdout)
    pprint.pprint(entry_dict, stream=stdout)


if __name__ == "__main__":
    main()
