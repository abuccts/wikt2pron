Introduction
============

enwiktionary2cmudict is a Python toolkit converting pronunciation in
enwiktionary xml dump to cmudict format. Support IPA and X-SAMPA format
at present.

.. contents::
   :local:


Features
--------

* Extract pronunciation from Wiktionary XML dump.

* Lookup pronunciation for a word in `Wiktionary`_.

* IPA -> X-SAMPA conversion.

.. _Wiktionary: https://en.wiktionary.org/


Requirements
------------

enwiktionary2cmudict requires:

* Python 3

* `python-mwxml`_

* `beautifulsoup4`_

.. _python-mwxml: https://github.com/mediawiki-utilities/python-mwxml
.. _beautifulsoup4: https://www.crummy.com/software/BeautifulSoup/


Installation
------------

::

    # download the latest version
    $ git clone https://github.com/abuccts/enwiktionary2cmudict.git
    $ cd enwiktionary
    
    # install and run test
    $ python setup.py install
    $ python setup.py -q test


