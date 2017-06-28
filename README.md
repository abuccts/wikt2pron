enwiktionary2cmudict
====================

[![Join the chat at https://gitter.im/enwiktionary2cmudict/Lobby](https://badges.gitter.im/enwiktionary2cmudict/Lobby.svg)](https://gitter.im/enwiktionary2cmudict/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![BSD licensed](https://img.shields.io/badge/License-BSD-blue.svg)](LICENSE)

A Python toolkit converting pronunciation in enwiktionary xml dump to cmudict format. Support IPA and X-SAMPA format at present.

Requirements
------------
enwiktionary2cmudict requires:
* Python 3
* [python-mwxml](https://github.com/mediawiki-utilities/python-mwxml)

Installation
------------
```sh
# download the latest version
$ git clone https://github.com/abuccts/enwiktionary2cmudict.git
$ cd enwiktionary

# install and run test
$ python setup.py install
$ python setup.py -q test
```

Usage
-----

##### Extract pronunciation from Wiktionary XML dump

To be improved.

Please refer to [expr.py](expr.py) for examples at present.

##### Lookup pronunciation for a word

First, create an instance of `Wiktionary` class:
```py
>>> from pywiktionary import Wiktionary
>>> wikt = Wiktionary(x_sampa=True)
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
>>> wikt = Wiktionary(lang="English", x_sampa=True)
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
