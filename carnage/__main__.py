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
"""Main module entrypoint for carnage."""

import argparse
import logging
import sys

from carnage.cli import migration, seed, serve
from carnage.logger import setup_logger_handler


def create_argument_parser() -> argparse.ArgumentParser:
    """Create the base argument parser for carnage CLI."""
    parser = argparse.ArgumentParser(
        prog="carnage",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Command-line for Carnage.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Enable debug logging",
    )

    parent_parsers = [argparse.ArgumentParser(add_help=False)]
    subparsers = parser.add_subparsers(help="Carnage sub-commands")

    seed.add_subparser(subparsers, parents=parent_parsers)
    serve.add_subparser(subparsers, parents=parent_parsers)
    migration.add_subparser(subparsers, parents=parent_parsers)

    return parser


def main() -> int:
    """Main entrypoint for Carnage API."""
    arg_parser = create_argument_parser()
    cmdline_arguments = arg_parser.parse_args()

    setup_logger_handler(debug=cmdline_arguments.debug)
    logger = logging.getLogger(__name__)
    try:
        if hasattr(cmdline_arguments, "func"):
            cmdline_arguments.func(cmdline_arguments)
        else:
            # user has not provided a subcommand, let's print the help
            logger.warning("No command specified.")
            arg_parser.print_help()
            return 1
    except Exception as e:
        logger.error(
            "Failed to run CLI command due to an exception.",
        )
        logger.exception("%s", e)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
