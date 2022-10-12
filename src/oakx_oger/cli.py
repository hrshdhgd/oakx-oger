"""Command line interface for oakx-oger."""
import logging

import click

from oakx_oger import __version__
from oakx_oger.oger_implementation import OGERImplementation

__all__ = [
    "main",
]

logger = logging.getLogger(__name__)


@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet")
@click.version_option(__version__)
def main(verbose: int, quiet: bool):
    """CLI for oakx-oger.

    :param verbose: Verbosity while running.
    :param quiet: Boolean to be quiet or verbose.
    """
    if verbose >= 2:
        logger.setLevel(level=logging.DEBUG)
    elif verbose == 1:
        logger.setLevel(level=logging.INFO)
    else:
        logger.setLevel(level=logging.WARNING)
    if quiet:
        logger.setLevel(level=logging.ERROR)


@main.command()
def run():
    """Run the oakx-oger's demo command."""
    impl = OGERImplementation()
    print(impl)


if __name__ == "__main__":
    main()
