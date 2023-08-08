#!/usr/bin/env python3
"""Wrapper for Confluence Sphinx Builder

enables support for configuration through shell environment variables

.. warning::
    make sure to pin a concrete version of the ````
"""
__author__ = 'theodor.rodweil@victory-k.it'
__copyright__ = '2023 - Victory Karma IT'
__license__ = 'DL-DE-BY-2.0'
__version__ = '1.2.0'


from dataclasses import dataclass, fields, asdict
from typing import Any, Optional, Callable, Type
from os import environ


#: rudimentary typecasting of serialized Python built-ins
DEFAULT_TYPECASTS = {
    'str': lambda inp: str(inp),
    'bool': lambda inp: {'true': True, 'false': False}[inp.lower()]
}


def get_config_from_environ(
    typecasts: dict[str, Callable] = DEFAULT_TYPECASTS
) -> 'ConfluenceBuilderConfig':
    """get confluence builder config from environment

    :param typecasts: a collection of built-in typecast functions
    """
    props = {field.name:field.type for field in fields(ConfluenceBuilderConfig)}

    prop_names = props.keys()

    out = {}

    for environ_name in dict(environ).keys():

        env_name = environ_name

        if env_name in prop_names:

            type_name = props[env_name].__name__

            if type_name == 'Optional':

                type_name = props[env_name].__args__[0].__name__

            value = typecasts[type_name](
                environ[environ_name]
            )

            if value is not None:

                out[env_name] = value

    try:

        return ConfluenceBuilderConfig(**out)

    except TypeError as err:

        raise TypeError(f'error getting config from environ: {err}') from err


def apply_config(
    config: 'ConfluenceBuildConfig',
    env: dict = globals()
) -> None:
    """apply confluence builder config to runtime environment

    :param config: configuration instance object
    :param env: global runtime variables instance object
    """
    for key, value in asdict(config).items():

        env[key.lower()] = value


@dataclass
class ConfluenceBuilderConfig:
    """partial configuration of the Confluence builder for Sphinx

    see 
    `https://sphinxcontrib-confluencebuilder.readthedocs.io/en/stable/configuration/`_
    , for more information.

    """
    #: The URL for the Confluence instance to publish to.
    CONFLUENCE_SERVER_URL: str

    #: The username value used to authenticate with the Confluence instance.
    CONFLUENCE_SERVER_USER: Optional[str] = None

    #: Key of the space in Confluence to be used to publish generated documents
    CONFLUENCE_SPACE_KEY: Optional[str] = None

    #: The username value used to authenticate with the Confluence instance.
    CONFLUENCE_PUBLISH_DRYRUN: Optional[bool] = None

    #: A boolean that decides whether or not to allow publishing.
    CONFLUENCE_PUBLISH: bool = True

    #: A boolean value to whether or not nest pages in a hierarchical ordered.
    CONFLUENCE_PAGE_HIERARCHY: bool = True

    #: The password value used to authenticate with the Confluence instance.
    CONFLUENCE_SERVER_PASS: Optional[str] = None

    #: The personal access token value used to authenticate with the Confluence 
    #  instance
    CONFLUENCE_PUBLISH_TOKEN: Optional[str] = None

    #: The root page found inside the configured space (confluence_space_key) 
    #  where published pages will be a descendant of
    CONFLUENCE_PARENT_PAGE: Optional[str] = None

    @staticmethod
    def from_environ() -> 'ConfluenceBuilderConfig':
        """get a new configuration object
        """

        return get_config_from_environ()

    def apply(self: Type, env: dict = globals()) -> None:
        """apply the configuration to the current runtime environment
        """

        return apply_config(self, env)
