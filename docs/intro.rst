Introduction
============

wikt2pron is a Python toolkit converting pronunciation in
enwiktionary xml dump to cmudict format.
Support `IPA`_ and `X-SAMPA`_ format at present.

.. _IPA: https://en.wikipedia.org/wiki/International_Phonetic_Alphabet
.. _X-SAMPA: https://en.wikipedia.org/wiki/X-SAMPA

.. contents::
   :local:


Features
--------

* Extract pronunciation from `Wiktionary XML dump`_.

* Lookup pronunciation for a word in `Wiktionary`_.

* IPA -> X-SAMPA conversion.

.. _Wiktionary XML dump: https://dumps.wikimedia.org/enwiktionary/
.. _Wiktionary: https://en.wiktionary.org/


Requirements
------------

wikt2pron requires:

* Python 3

* `regex`_

* `python-mwxml`_

* `beautifulsoup4`_

.. _regex: https://pypi.python.org/pypi/regex/
.. _python-mwxml: https://github.com/mediawiki-utilities/python-mwxml
.. _beautifulsoup4: https://www.crummy.com/software/BeautifulSoup/


Installation
------------

.. code-block:: shell

    # download the latest version
    $ git clone https://github.com/abuccts/wikt2pron.git
    $ cd enwiktionary

    # install and run test
    $ python setup.py install
    $ python setup.py -q test

    # make documents
    $ make -C docs html

