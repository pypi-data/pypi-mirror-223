# xconfluencebuilder

This program is a drop-in replacement for the [Atlassian Confluence Builder for
Sphinx](https://github.com/sphinx-contrib/confluencebuilder). It
exports/dumps/archives the build output of the confluencebuilder Sphinx builder
into a generic interchangeable format, which can be used in conjunction with
other publishers than the built-in one. The program does not require
connectivity to a Confluence instance.

The program may be useful in circumstances where a Python3 runtime is not
available on the machine responsible for publishing to Confluence. 

For more information on why this program exists, please refer to
[confluencebuilder Issue
823](https://github.com/sphinx-contrib/confluencebuilder/issues/823).

For a reference implementation of an external publisher, please refer to
[PSConfluencePublisher](https://bitbucket.org/victorykit/psconfluencepublisher),
a standalone PowerShell publisher for *Atlassian Confluence Builder for Sphinx*.

The following is a sample manifest generated from the default sample:

```
{
    "Pages": [
        {
            "Title": "Default Sample~",
            "Ref": "pages/Default+Sample~.xml"
        },
        {
            "Title": "Cats",
            "Ref": "pages/Cats.xml",
            "AncestorTitle": "Default Sample~"
        }
    ],
    "Attachments": [
        {
            "Name": "pexels-just-a-couple-photos-3777622.jpg",
            "ContainerPageTitle": "Cats",
            "MimeType": "image/jpeg",
            "Ref": "attachments/Cats/pexels-just-a-couple-photos-3777622.jpg"
        },
        {
            "Name": "pexels-sami-aksu-14356302.jpg",
            "ContainerPageTitle": "Cats",
            "MimeType": "image/jpeg",
            "Ref": "attachments/Cats/pexels-sami-aksu-14356302.jpg"
        },
        {
            "Name": "objects.inv",
            "ContainerPageTitle": "Default Sample~",
            "MimeType": "application/octet-stream",
            "Ref": "attachments/Default+Sample~/objects.inv"
        }
    ]
}
```

> **NOTE**: The manifest's schema is currently part of the
  [PSConfluencePublisher](https://bitbucket.org/victorykit/psconfluencepublisher)

## Installing

You can install this extension via PyPI (through pip):

```
python3 -m pip install victorykit-xconfluencebuilder
```

or via the sources by cloning the repository (then changing into the directory),
and also using pip

```
$ git clone https://bitbucket.org/victorykit/xconfluencebuilder.git
...
$ python3 -m pip install .
```

## Usage

In addition to the basic configuration outlined here, you can find a usage 
example under `samples/`.

* Register the extension sphinxcontrib.confluencebuilder in the project's 
  configuration script (conf.py):

```
extensions = [
    'xconfluencebuilder'
]
```

* Run sphinx-build with the builder confluence:

```
sphinx-build -b xconfluence . _build/confluence -E -a
 (or)
 python -m sphinx -b xconfluence . _build/confluence -E -a
```

Afterwards, archive the output directory and use it for interchange with an
external publisher like the aforementioned 
[PSConfluencePublisher](https://bitbucket.org/victorykit/psconfluencepublisher).

More information on the usage of this extension can be obtained from the
extension's documentation this is a drop-in for:

> [Atlassian Confluence Builder for Sphinx Tutorial](https://sphinxcontrib-confluencebuilder.readthedocs.io/tutorial)

## Configuration

In addition to the configuration parameters provided by
`sphinxcontrib.confluencebuilder`, the following parameters are available:

* `xconfluence_outdir` - base directory for archive output (default:
  `{outdir}/confluence.out`)
* `xconfluence_manifest_basename` - basename of the asset manifest

The following `confluencebuilder` configuration parameters are not available: 

* `confluence_publish_dry_run` (as if set to `False`)

The `confluence_publish` parameter must still however be set (to `True`), as 
well as all other configuration parameters which would be required for a minimal
configuration of `confluencebuilder`. Please refer to [confluencebuilder
documentation](https://sphinxcontrib-confluencebuilder.readthedocs.io/tutorial) 
on how to do so.

## Testing

We're patching/mocking a couple of things of the original extension, to make
this work. Writing proper unit tests for this would take some time to figure out.
We'll discuss this with the original author of the extension.

## Issue Tracking

Will be provided shortly.
