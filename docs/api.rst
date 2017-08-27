pywiktionary API
================

.. module:: pywiktionary

The library provides classes which are usable by third party tools.

.. contents::
   :local:


.. ``Wiktionary`` Class

``Wiktionary`` Class
--------------------

.. autoclass:: Wiktionary
    :members:


.. ``Parser`` Class

``Parser`` Class
----------------

.. autoclass:: Parser
    :members:


Utilities
---------

.. automodule:: IPA.IPA
    :members:

    
Convert spelling text in ``{{*-IPA}}`` to IPA pronunciation.

Most are modified from Wiktionary Lua Module.

.. autofunction:: IPA.fr_pron.to_IPA

.. autofunction:: IPA.ru_pron.to_IPA

.. autofunction:: IPA.hi_pron.to_IPA

.. autofunction:: IPA.es_pron.to_IPA

.. autofunction:: IPA.cmn_pron.to_IPA

