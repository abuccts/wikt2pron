Usage
=====

Extract pronunciation from Wiktionary XML dump
----------------------------------------------

    First, create an instance of :class:`Wiktionary` class:
    
    .. code-block:: python

        >>> from pywiktionary import Wiktionary
        >>> wikt = Wiktionary(XSAMPA=True)

    Use the example XML dump in ``pywiktionary/data``:
    
    .. code-block:: python

        >>> dump_file = "pywiktionary/data/enwiktionary-test-pages-articles-multistream.xml"
        >>> pron = wikt.extract_IPA(dump_file)

    Here's the extracted result:
    
    .. code-block:: python

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


Lookup pronunciation for a word in Wiktionary
---------------------------------------------

    First, create an instance of :class:`Wiktionary` class:

    .. code-block:: python

        >>> from pywiktionary import Wiktionary
        >>> wikt = Wiktionary(XSAMPA=True)

    Lookup a word using ``lookup`` method:

    .. code-block:: python

        >>> word = wikt.lookup("present")

    The entry of word "present" is at https://en.wiktionary.org/wiki/present, and here is the lookup result:

    .. code-block:: python

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

    To lookup a word in a certain language, specify the ``lang`` parameter:

    .. code-block:: python

        >>> wikt = Wiktionary(lang="English", XSAMPA=True)
        >>> word = wikt.lookup("read")
        >>> pprint(word)
        [{'IPA': '/ɹiːd/', 'X-SAMPA': '/r\\i:d/', 'lang': 'en'},
         {'IPA': '/ɹɛd/', 'X-SAMPA': '/r\\Ed/', 'lang': 'en'}]


IPA -> X-SAMPA conversion
-------------------------

    .. code-block:: python

        >>> from pywiktionary import IPA
        >>> IPA_text = "/t͡ʃeɪnd͡ʒ/" # en: [[change]]
        >>> XSAMPA_text = IPA.IPA_to_XSAMPA(IPA_text)
        >>> XSAMPA_text
        "/t__SeInd__Z/"


Using the collected dictionaries
--------------------------------

    To use the collected dictionaries training G2P models or acoustic models, please refer to these blogs for details:

    1. `Grapheme to Phoneme Conversion`_

    2. `Training Acoustic Model on Voxforge Dataset`_

    3. `Training Acoustic Model on LibriSpeech`_

    .. _Grapheme to Phoneme Conversion: https://abuccts.blogspot.com/2017/07/gsoc-2017-with-cmusphinx-post-8.html
    .. _Training Acoustic Model on Voxforge Dataset: https://abuccts.blogspot.com/2017/08/gsoc-2017-with-cmusphinx-post-9-10.html
    .. _Training Acoustic Model on LibriSpeech: https://abuccts.blogspot.com/2017/08/gsoc-2017-with-cmusphinx-post-11.html

