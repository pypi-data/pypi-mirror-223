"""
MarkUs Exam Matcher: __main__.py

Information
===============================
Environment for top-level code (entry point into package).
"""
import sys
from argparse import ArgumentParser

from .core.char_types import CharType
from .image_processing import read_chars


def config_arg_parser() -> ArgumentParser:
    """
    Configure a command line argument parser.
    :return: Command line argument parser.
    """
    # Initialize parser
    parser = ArgumentParser(
        prog="run_scanner.py", description="Predict handwritten characters in rectangular grids."
    )

    # Positional arguments
    parser.add_argument("image", type=str, help="Path to image to predict characters from.")
    parser.add_argument(
        "char_type",
        choices=["digit", "letter"],
        help="Type of character to classify. Only digits and letters are supported.",
    )

    # Optional arguments
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Specify whether to run program with debug mode enabled.",
    )

    return parser


if __name__ == "__main__":
    # Parse command line arguments
    parser = config_arg_parser()
    args = parser.parse_args(sys.argv[1:])
    char_type = CharType.DIGIT if args.char_type == "digit" else CharType.LETTER

    # Make prediction
    pred = read_chars.run(args.image, char_type=char_type, debug=args.debug)
    print(pred)
