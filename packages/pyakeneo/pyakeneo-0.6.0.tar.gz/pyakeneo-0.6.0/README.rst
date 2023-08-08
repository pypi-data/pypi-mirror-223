|Build Status|
|Documentation Status|


Python client for Akeneo PIM API
================================

A simple Python client to use the `Akeneo PIM API`_.

Dependencies are managed with `poetry`_
(list of dependencies available in `pyproject.toml`_).

You may install them with:

.. code:: bashasda

        poetry install --dev

Installation
------------

.. code:: bash

        poetry install pyakeneo
        
Usage
-----

A simple example is provided in `docs/example_exporter.py`_.

If you experience issues when importing modules, run the examples as follow:

.. code:: bash

        cd docs
        poetry run python example_exporter.py
        

.. _docs/example_exporter.py: https://raw.githubusercontent.com/kavetech/akeneo_api_client/master/docs/example.py

Tests
-----

Run tests as follow:

.. code:: bash

        poetry run nosetests
        
If tests don't pass in your environment, please check that dependencies match those described in pyproject.toml. One way to do it is to ensure that poetry runs commands in a dedicated virtualenv by setting environment variable as follow:

.. code:: bash

        poetry install --dev


Tests are provided with mocks, recorded with `VCR.py`_. In case you need
to (re)run tests, you should install the dataset in you PIM instance as
follow:

.. _Akeneo PIM API: https://api.akeneo.com/
.. _poetry: https://github.com/python-poetry/poetry
.. _VCR.py: http://vcrpy.readthedocs.io/en/latest/index.html
.. _pyproject.toml: https://python-poetry.org/docs/pyproject/

.. |Build Status| image:: https://travis-ci.org/matthieudelaro/akeneo_api_client.svg?branch=master
   :target: https://travis-ci.org/matthieudelaro/akeneo_api_client
.. |Documentation Status| image:: https://readthedocs.org/projects/akeneo-api-client/badge/?version=latest
   :target: http://akeneo-api-client.readthedocs.io/en/latest/
