"""test.py

Test script for parsing xml dump.
"""

import re
import sys
import json
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

    #print(entry_dict, file=stdout)
    pprint.pprint(entry_dict, stream=stdout)


def get_word_list():
    """get_word_list
    """
    page_num = 10
    dump_file = "../enwiktionary-latest-pages-articles-multistream.xml"
    out_file = "./word.lst.json"
    header2 = re.compile("(?:\A|\n)={2}([a-zA-Z0-9 -]+)={2}\n")
    header3 = re.compile("={3}Pronunciation={3}")

    dump = mwxml.Dump.from_file((open(dump_file, "rb")))
    stdout = open(sys.stdout.fileno(), "w", encoding="utf-8", closefd=False)

    lst = []
    entry_no = 0
    for page in dump:
        for revision in page:
            if revision.page.namespace == 0:
                text = revision.text
                header2_lst, header2_split = \
                    header2.findall(text), header2.split(text)
                i = 0
                lang = []
                while i < len(header2_split):
                    if header2_split[i] in header2_lst:
                        if header3.search(header2_split[i+1]):
                            lang.append((header2_split[i], 1))
                        else:
                            lang.append((header2_split[i], 0))
                        i += 1
                    i += 1
                lst.append({
                    "id": revision.page.id,
                    "title": revision.page.title,
                    "lang": lang,
                    "h2": header2_lst,
                })
        entry_no += 1
        if page_num and entry_no >= page_num:
            break

    #print(lst, file=stdout)
    with open(out_file, "w") as f:
        json.dump(lst, f)


if __name__ == "__main__":
    #main()
    get_word_list()
