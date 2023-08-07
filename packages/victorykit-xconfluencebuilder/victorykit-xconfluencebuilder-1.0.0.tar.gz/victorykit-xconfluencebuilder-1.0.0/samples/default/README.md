# Default Sample

This is a sample/reference implementation of the `xconfluencebuilder`. It
provides a Sphinx build with 2 ancestrally related pages, where the child page 
contains an attachment.

Output is directed to the `build/` directory, which will contain the regular
``sphinxcontrib.confluencebuilder`` artifacts in addition to the publishing
manifest and referenced assets.

# Instructions

To run this reference implementation, you are required to have
[pipenv](https://pipenv.pypa.io/en/latest/) installed on your system.

Install the virtual environment by executing the following command from within
this directory:

```
$ python3 -m pipenv install
```

Afterwards, you can build all assets by issuing the following command

```
$ python3 -m pipenv run sphinx-build
```
