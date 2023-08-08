###############
Default Sample~
###############

.. note::

    ``confluence_conf.py`` is not required, it's just a helper module to be 
    able to configure ``sphinxcontrib.confluencebuilder`` through environment 
    variables.

To run this sample, `pipenv <https://pypi.org/project/pipenv/>`_ is required.

First, install the *venv* by executing the following command from within the
``samples/default/`` directory:

.. code-block::

    $ python3 -m pipenv install

.. note::

    To contain the virtual environment within the current directory, create an
    empty directory named ``.venv``.

Afterwards, execute the following command:

.. code-block::

    $ python3 -m pipenv run build-sphinx

The backend for the command can be inspected in ``Pipfile``.

You should now have a directory

.. toctree::
    :caption: Important Content
    
    cats
