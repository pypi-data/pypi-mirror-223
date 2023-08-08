#!/usr/bin/env python3
"""Publishment delay wrapper sphinxcontrib.confluencebuilder

The builder name is ``xconfluence``

``Publisher``, ``Builder``, as well as ``Rest`` instances are mocked and are 
supressing any HTTP connectivity should the ``confluence_publish_dry_run`` be 
set to ``True``. 

.. warning::

    ``confluence_publish_dry_run`` MUST be set to ``True``

Content (pages) and attachments are dumped into separate file_s and indexed. 

The output directory can be set through ``x_confluence_outdir``.

The use-case for this implementation is as follows:

    I am currently facing the situation where i need to publish to an 
    air-gapped Confluence server inside a virtualised and privatised 
    environment (over Windows VDI). In addition, company policy forbids me from 
    using, or installing Python 
    on the VDI. I can freeload a perl executable that came bundled with Git for 
    Windows, but there are no other scripting means besides Windows PowerShell.

"""
__author__ = 'theodor.rodweil@victory-k.it'
__copyright__ = '2023 - Victory Karma IT'
__license__ = 'DL-DE-BY-2.0'

from dataclasses import dataclass, asdict
import json
from pathlib import Path
from typing import Any, Optional, ByteString, Dict, Tuple, List
from unittest.mock import patch
from urllib.parse import quote_plus

from sphinx.application import Sphinx
from sphinx.util import logging

from sphinxcontrib.confluencebuilder import setup as _setup
from sphinxcontrib.confluencebuilder.builder import (
    ConfluenceBuilder as _ConfluenceBuilder
)
from sphinxcontrib.confluencebuilder.publisher import (
    ConfluencePublisher as _ConfluencePublisher
)
from sphinxcontrib.confluencebuilder.rest import Rest as _Rest


logger = logging.getLogger(__name__)


@dataclass
class PageMeta:
    """
    see
    `https://docs.atlassian.com/ConfluenceServer/rest/8.4.0/#api/content-createContent`_,
    for more information
    """
    #: title of page
    title: str
    #: Local filesystem reference/path. The reference MUST be relative.
    ref: str
    #: title of Confluence page this page is a child of
    ancestor_title: Optional[str] = None


@dataclass
class AttachmentMeta:
    """
    """
    #: name of attachment, which must be unique within the container page
    name: str
    #: title of confluence page this attachment is contained in the title must
    #  be a property key of the pages object
    container_page_title: str
    #: MIME type of attachment 
    mime_type: str
    #: Local filesystem reference/path. The reference MUST be relative.
    ref: str


@dataclass
class Manifest:
    """
    """
    #: 
    pages: List[PageMeta]

    #: 
    attachments: List[AttachmentMeta]


page_meta_key_map = {
    'title': 'Title',
    'ref': 'Ref',
    'ancestor_title': 'AncestorTitle'
}


attachment_meta_key_map = {
    'name': 'Name',
    'container_page_title': 'ContainerPageTitle',
    'mime_type': 'MimeType',
    'ref': 'Ref'
}


manifest_key_map = {
    'pages': 'Pages',
    'attachments': 'Attachments'
}


def sanitize_dict_keys(
    obj: dict,
    key_map: dict,
) -> dict:
    """transform the keys of a dictionary in accordance with a map

    key-value pairs where the value is ``None`` will be discarded entirely

    :param obj: the dictionary to transform
    :param key_map: a map of the keys to transform, where the key is the
                    original key and the value is the key to transform to

    :returns: the transformed dictionary
    """
    return {key_map[k]:v for k, v in obj.items() if v is not None}


class Rest(_Rest):
    """
    """
    def __init__(self, config):
        """
        """

        super().__init__(config)

    def __getattr__(self, name: str) -> Any:
        """
        """
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        """
        """
        return super().__setattr__(name, value)

    def get(self, key, params=None):
        """
        
        .. note::
            this is a non-sensical mock just to make the backend happy. This
            isn't required for dumping the content.
        """
        return {'results': [
            {
                'id': 1234567890,
                'key': 'NULL',
                'name': 'NULL',
                'type': 'NULL'
            }
        ], 'size': 1, 'limit': 1, 'start': 0}


class ConfluencePublisher(_ConfluencePublisher):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

        self.dump = Manifest(
            pages = [],
            attachments = []
        )

    def __getattr__(self, name: str) -> Any:
        """
        """
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        """
        """
        return super().__setattr__(name, value)

    def connect(self):
        """initialize a REST client and probe the target Confluence instance

        .. note::

            Actually, i don't want the extension to initialize a connection, 
            but there is too much entanglement, so we're mocking the absolute
            minimum for the publisher object to assume everything is fine
        """
        with patch('sphinxcontrib.confluencebuilder.publisher.Rest', Rest):

            return super().connect()

    def get_page_by_id(self, page_id, expand = 'version') -> Tuple[None, List]:
        """get page information with the provided page name

        :param page_id: the page identifier
        :param expand: data to expand on

        :returns: page id and page object
        """
        return (None, [])

    def store_attachment(
        self,
        page_id: str,
        name: str,
        data: Any,
        mimetype: Any,
        hash_: str,
        force: bool = False
    ) -> str:
        """request to store an attachment on a provided page

        :returns: the attachment identifier
        """
        logger.info('pass-through intercept: store_attachment')

        file_name = quote_plus(name)

        output_basepath = Path(getattr(self.config, 'xconfluence_outdir'))

        file_ = output_basepath / 'attachments' / quote_plus(page_id) / file_name

        file_.parent.mkdir(parents = True, exist_ok = True)

        file_.write_bytes(data)

        self.dump.attachments.append(AttachmentMeta(
            name = name,
            container_page_title = page_id,
            mime_type = mimetype,
            ref = str(file_.relative_to(output_basepath))
        ))

        return name

    def store_page(
        self,
        page_name: str,
        data: Any,
        parent_id: Optional[str] = None
    ) -> str:
        """request to store page information to a confluence instance

        :param page_name: the page title to use on the updated page
        :param data:  the page data to apply
        :param parent_id: the id of the ancestor to use

        :returns: id of uploaded page
        """
        logger.info('pass-through intercept: store_page')

        output_basepath = Path(getattr(self.config, 'xconfluence_outdir'))

        file_name = f"{quote_plus(page_name)}.xml"

        file_ = output_basepath / 'pages' / file_name

        file_.parent.mkdir(parents=True, exist_ok=True)

        file_.write_bytes(data['content'].encode('utf-8'))

        meta = {
            'title': page_name,
            'ref': str(file_.relative_to(output_basepath))
        }

        if parent_id:
            meta['ancestor_title'] = parent_id

        self.dump.pages.append(PageMeta(**meta))

        return page_name

    def store_page_by_id(
        self,
        page_name: str,
        page_id: str,
        data: Any
    ) -> str:
        """request to store page information on the page with a matching id

        :param page_name: the page title to use on the updated page
        :param data:  the page data to apply
        :param parent_id: the id of the ancestor to use

        :returns: id of uploaded page
        """
        logger.info('pass-through intercept: store_page_by_id')

        return 'NULL'

    def disconnect(self):
        """terminate the REST client

        we're not actually terminating anything, since we mocked the connection
        to make the backend happy.

        We're using this method to dump the assets and the manifest. The
        manifest is transformed prior to being serialized, since the manifest's
        property keys are capitalized. We think it's better to have this loosely
        coupled so that pythonic variable names don't enforce the structure of
        the manifest schema.
        """
        file_ = (Path(getattr(self.config, 'xconfluence_outdir')) / 
                 'manifest.json')

        file_.parent.mkdir(parents = True, exist_ok=True)

        pre_serialize = asdict(self.dump)

        pages = [
            sanitize_dict_keys(page_meta, page_meta_key_map)
            for page_meta in pre_serialize['pages']
        ]

        attachments = [
            sanitize_dict_keys(attachment_meta, attachment_meta_key_map)
            for attachment_meta in pre_serialize['attachments']
        ]

        pre_serialize = {
            manifest_key_map['pages']: pages,
            manifest_key_map['attachments']: attachments
        }

        raw = json.dumps(pre_serialize, indent=4)

        file_.write_text(raw)

        logger.info(f'content dump count: {len(self.dump.pages)}')

        logger.info(f'attachments dump count: {len(self.dump.attachments)}')

        logger.info(f'dump index: {file_}')


class ConfluenceBuilder(_ConfluenceBuilder):
    """
    """
    name = 'xconfluence'

    def __init__(self, app: Sphinx, env = None):
        """
        """
        patch_target = ('sphinxcontrib.confluencebuilder'
                        '.builder.ConfluencePublisher')

        with patch(patch_target, ConfluencePublisher):

            super().__init__(app, env)

    def __getattribute__(self, name: str) -> Any:
        """
        """
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        """
        """
        return super().__setattr__(name, value)


def setup(app: Sphinx):
    """
    """
    patch_target = 'sphinxcontrib.confluencebuilder.ConfluenceBuilder'

    app.add_config_value(
        name = 'xconfluence_outdir',
        default = str(Path(app.outdir) / 'confluence.out'),
        rebuild = True
    )

    app.add_config_value(
        name = 'xconfluence_manifest_basename',
        default = 'manifest.json',
        rebuild = True
    )

    with patch(patch_target, ConfluenceBuilder):

        logger.info(f'patching: {patch_target}')

        return _setup(app)
