wikt2pron
=========

[![Build Status](https://travis-ci.org/abuccts/wikt2pron.svg?branch=master)](https://travis-ci.org/abuccts/wikt2pron)
[![Documentation Status](https://readthedocs.org/projects/wikt2pron/badge/?version=latest)](http://wikt2pron.readthedocs.io/en/latest/?badge=latest)
[![Join the chat at https://gitter.im/enwiktionary2cmudict/Lobby](https://badges.gitter.im/enwiktionary2cmudict/Lobby.svg)](https://gitter.im/enwiktionary2cmudict/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![BSD licensed](https://img.shields.io/badge/License-BSD-blue.svg)](LICENSE)

_Wiktionary pronunciation collector_

A Python toolkit converting pronunciation in enwiktionary xml dump to cmudict format. Support [IPA](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet) and [X-SAMPA](https://en.wikipedia.org/wiki/X-SAMPA) format at present.

This project is developed in [GSoC 2017](https://summerofcode.withgoogle.com/dashboard/student/proposal/5169382905872384/) with [CMU Sphinx](https://cmusphinx.github.io/).

Collected pronunciation dictionaries and related example models can be downloaded at [Dropbox](https://www.dropbox.com/sh/1anleakrnm5ednt/AAAXeSY0abHxFLcXOr4OkVJ9a?dl=0).

Requirements
------------
wikt2pron requires:
* Python 3
* [regex](https://pypi.python.org/pypi/regex/)
* [python-mwxml](https://github.com/mediawiki-utilities/python-mwxml)
* [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/)

Installation
------------
```sh
# download the latest version
$ git clone https://github.com/abuccts/wikt2pron.git
$ cd wikt2pron

# install and run test
$ python setup.py install
$ python setup.py -q test

# make documents
$ make -C docs html
```

Usage
-----

##### Extract pronunciation from Wiktionary XML dump

First, create an instance of `Wiktionary` class:
```py
>>> from pywiktionary import Wiktionary
>>> wikt = Wiktionary(XSAMPA=True)
```
Use the example XML dump in [[pywiktionary/data]](pywiktionary/data):
```py
>>> dump_file = "pywiktionary/data/enwiktionary-test-pages-articles-multistream.xml"
>>> pron = wikt.extract_IPA(dump_file)
```
Here's the extracted result:
```py
>>> from pprint import pprint
>>> pprint(pron)
[{'id': 16,
  'pronunciation': {'English': [{'IPA': '/ˈdɪkʃ(ə)n(ə)ɹɪ/',
                                 'X-SAMPA': '/"dIkS(@)n(@)r\\I/',
                                 'lang': 'en'},
                                {'IPA': '/ˈdɪkʃənɛɹi/',
                                 'X-SAMPA': '/"dIkS@nEr\\i/',
                                 'lang': 'en'}]},
  'title': 'dictionary'},
 {'id': 65195,
  'pronunciation': {'English': 'IPA not found.'},
  'title': 'battleship'},
 {'id': 39478,
  'pronunciation': {'English': [{'IPA': '/ˈmɜːdə(ɹ)/',
                                 'X-SAMPA': '/"m3:d@(r\\)/',
                                 'lang': 'en'},
                                {'IPA': '/ˈmɝ.dɚ/',
                                 'X-SAMPA': '/"m3`.d@`/',
                                 'lang': 'en'}]},
  'title': 'murder'},
 {'id': 80141,
  'pronunciation': {'English': [{'IPA': '/ˈdæzəl/',
                                 'X-SAMPA': '/"d{z@l/',
                                 'lang': 'en'}]},
  'title': 'dazzle'}]
```

##### Lookup pronunciation for a word

First, create an instance of `Wiktionary` class:
```py
>>> from pywiktionary import Wiktionary
>>> wikt = Wiktionary(XSAMPA=True)
```
Lookup a word using `lookup` method:
```py
>>> word = wikt.lookup("present")
```
The entry of word "present" is at https://en.wiktionary.org/wiki/present, and here is the lookup result:
```py
>>> from pprint import pprint
>>> pprint(word)
{'Catalan': 'IPA not found.',
 'Danish': [{'IPA': '/prɛsanɡ/', 'X-SAMPA': '/prEsang/', 'lang': 'da'},
            {'IPA': '[pʰʁ̥ɛˈsɑŋ]', 'X-SAMPA': '[p_hR_0E"sAN]', 'lang': 'da'}
],
 'English': [{'IPA': '/ˈpɹɛzənt/', 'X-SAMPA': '/"pr\\Ez@nt/', 'lang': 'en'},
             {'IPA': '/pɹɪˈzɛnt/', 'X-SAMPA': '/pr\\I"zEnt/', 'lang': 'en'},
             {'IPA': '/pɹəˈzɛnt/', 'X-SAMPA': '/pr\\@"zEnt/', 'lang': 'en'}],
 'Ladin': 'IPA not found.',
 'Middle French': 'IPA not found.',
 'Old French': 'IPA not found.',
 'Swedish': [{'IPA': '/preˈsent/', 'X-SAMPA': '/pre"sent/', 'lang': 'sv'}]}
```

To lookup a word in a certain language, specify the `lang` parameter:
```py
>>> wikt = Wiktionary(lang="English", XSAMPA=True)
>>> word = wikt.lookup("read")
>>> pprint(word)
[{'IPA': '/ɹiːd/', 'X-SAMPA': '/r\\i:d/', 'lang': 'en'},
 {'IPA': '/ɹɛd/', 'X-SAMPA': '/r\\Ed/', 'lang': 'en'}]
```

##### IPA -> X-SAMPA conversion
```py
>>> from pywiktionary import IPA
>>> IPA_text = "/t͡ʃeɪnd͡ʒ/" # en: [[change]]
>>> XSAMPA_text = IPA.IPA_to_XSAMPA(IPA_text)
>>> XSAMPA_text
"/t__SeInd__Z/"
```
