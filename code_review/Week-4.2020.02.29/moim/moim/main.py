import argparse
from ._clean import moim_clean
from ._stats import moim_stats
from .about import __version__

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", "-v", action="version", version="%(prog)s {}".format(__version__))
    parser.set_defaults(func=lambda x: parser.print_usage())
    subparsers = parser.add_subparsers()

    # moim clean
    subparser_clean = subparsers.add_parser("clean", help="package for cleaning text data")
    subparser_clean.add_argument("--input_path", "-i", required=True, help="input file path you want to clean")
    subparser_clean.add_argument("--output_path", "-o", required=True, help="output path you want to save")
    subparser_clean.set_defaults(func=moim_clean)

    # moim stats
    subparser_stats = subparsers.add_parser("stats", help="package for statistics of text data")
    subparser_stats.add_argument("--input_path", "-i", required=True, help="input file path you want to know")
    subparser_stats.add_argument("--number", "-n", required=True, help="number of top frequent words you want to know")
    subparser_stats.set_defaults(func=moim_stats)

    args = parser.parse_args()

    func = args.func

    func(args)