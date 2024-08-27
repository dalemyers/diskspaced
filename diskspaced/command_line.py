#!/usr/bin/env python3

"""Command line handler for diskspaced."""

import argparse
import logging
import os
import sys

try:
    import diskspaced
except ImportError:
    # Insert the package into the PATH
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..")))
    import diskspaced


def _handle_arguments() -> int:
    """Handle command line arguments and call the correct method."""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--folder-path",
        dest="folder_path",
        action="store",
        required=True,
        help="The path to scan",
    )

    parser.add_argument(
        "--output-path",
        dest="output_path",
        action="store",
        required=True,
        help="Set the output path for the results to be written to",
    )

    parser.add_argument(
        "--format",
        dest="format",
        action="store",
        choices=[item.value for item in diskspaced.OutputFormat],
        required=True,
        help="Set the output path for the results to be written to",
    )

    parser.add_argument(
        "--pretty-print",
        dest="pretty_print",
        action="store_true",
        default=False,
        required=False,
        help="Set this to pretty print the output (if supported by the format)",
    )

    parser.add_argument(
        "--print-after-n-files",
        dest="print_after_n_files",
        action="store",
        default=0,
        type=int,
        required=False,
        help="Set this to print out the currently processed file after N files. Setting to 0 (the default) never prints.",
    )

    parser.add_argument(
        "--alphabetical",
        dest="alphabetical",
        action="store_true",
        default=False,
        required=False,
        help="Set this to process the files in alphabetical order",
    )

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    try:
        diskspaced.scan(
            args.folder_path,
            args.output_path,
            diskspaced.OutputFormat(args.format),
            args.print_after_n_files,
            args.alphabetical,
            args.pretty_print,
        )
    # pylint: disable=broad-except
    except Exception as e:
        # pylint: enable=broad-except
        logging.error(f"{e}", exc_info=True)
        return 1

    return 0


def run() -> int:
    """Entry point for poetry generated command line tool."""
    return _handle_arguments()


if __name__ == "__main__":
    sys.exit(_handle_arguments())
