# MIT License
#
# Copyright (c) 2022, Rodolfo Olivieri
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Module that represents the `migration` command."""

import argparse
import logging
import os
from typing import Any

from alembic import command
from alembic.config import Config

logger = logging.getLogger(__name__)


def add_subparser(
    subparsers: Any,
    parents: list[argparse.ArgumentParser],
) -> None:
    """Add all init parsers.

    :param subparsers: subparser we are going to attach to
    :param parents: Parent parsers, needed to ensure tree structure argparse.
    """
    seed_parser = subparsers.add_parser(
        name="migration",
        parents=parents,
        help="Execute the database migration with Alembic.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    seed_parser.set_defaults(func=run)
    seed_parser.add_argument(
        "--downgrade",
        action="store_true",
        help="Downgrade a revision from database.",
    )
    seed_parser.add_argument(
        "--upgrade",
        action="store_false",
        help="Upgrade a revision from database.",
    )


def _load_alembic_init() -> Config:
    """Internal function to load the alembic config file."""
    ini_path = os.path.join(os.getcwd(), "alembic.ini")
    logger.debug(f"Loading configuration file from {ini_path}")

    # create Alembic config and feed it with paths
    config = Config(ini_path)
    return config


def run(args: argparse.Namespace) -> None:
    """Default method that is executed that is tied to the seed command.

    :param args: Arguments passed down to the command.
    """

    if args.downgrade and args.upgrade:
        raise AssertionError(
            "Can't do a downgrade and upgrade at the same time. Must specify "
            "one at a time.",
        )

    config = _load_alembic_init()

    revision = "head"
    if args.downgrade:
        logger.info(f"Downgrading database to {revision}")
        command.downgrade(config, revision, False, None)
    else:
        logger.info(f"Upgrading database to {revision}")
        command.upgrade(config, revision, False, None)

    logger.info("Migration finished successfully.")
