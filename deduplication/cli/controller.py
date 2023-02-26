import argparse
from typing import List

from deduplication.cli.use_case import DeduplicationUseCase, Request


class DedupController:
    def __init__(self, use_case: DeduplicationUseCase) -> None:
        self.use_case = use_case

    def process_arguments(self, arguments: List[str]) -> None:
        parser = argparse.ArgumentParser(
            description="""Find near-duplicates among documents by using minhashing
            and locality-sensitive hashing. See below for options for minhashing and
            preprocessing.""",
        )
        parser.add_argument(
            "directory",
            help="Directory of files to process",
            type=str,
        )
        parser.add_argument(
            "--output",
            "-o",
            help="""Name of output file to store results of near-duplicate detection.
             Default is 'output.csv'.""",
            default="output.csv",
        )
        parser.add_argument(
            "--permutations",
            "-p",
            help="""Number of permutations to use for minhashing. Default is 128.
             This value should be at least 2 and maximal 2**32.""",
            type=int,
            default=128,
        )
        parser.add_argument(
            "--lsh-threshold",
            "-l",
            help="""Threshold for locality sensitive hashing. Takes value between
             0.0 and 1.0. Default is 0.9""",
            type=float,
            default=0.9,
        )
        parser.add_argument(
            "--shingle-size",
            "-k",
            help="""Size of shingles/n-grams for set representation of documents.
            Default is 3.""",
            type=int,
            default=3,
        )
        parser.add_argument(
            "--character-shingle",
            "-s",
            help="""Create shingles/n-grams on character level. If this option is not used,
            shingles are created on token level which whitespace and word boundary
            tokenization performed.""",
            action="store_false",
        )
        parser.add_argument(
            "--case-insensitive",
            "-c",
            help="Convert documents to lowercase.",
            action="store_true",
        )
        parser.add_argument(
            "--ignore-numbers",
            "-n",
            help="Remove digits from documents.",
            action="store_true",
        )
        parser.add_argument(
            "--ignore-whitespace",
            "-w",
            help="""Strip whitespace characters from documents. This implies the use
            of --character-shingle.""",
            action="store_true",
        )
        parser.add_argument(
            "--ignore-punctuation",
            "-i",
            help="Strip punctuation and other special symbols from documents",
            action="store_true",
        )
        args = parser.parse_args(arguments)
        if args.permutations < 2 or args.permutations > 2**32:
            parser.error("Invalid input value for --permutations.")
        if not (1 >= args.lsh_threshold and 0 <= args.lsh_threshold):
            parser.error(
                "Invalid input value for --lsh-threshold: Should be between 0.0 and 1.0"
            )
        if args.shingle_size < 1:
            parser.error("Invalid value for --shingle-size: Should be at least 1.")
        char_level = False
        if args.ignore_whitespace:
            char_level = True
        self.use_case.process(
            Request(
                directory=args.directory,
                output_file=args.output,
                use_token=not char_level if char_level else args.character_shingle,
                shingle_size=args.shingle_size,
                num_perm=args.permutations,
                threshold=args.lsh_threshold,
                case_insensitive=args.case_insensitive,
                ignore_nums=args.ignore_numbers,
                normalize_whitespace=args.ignore_whitespace,
                ignore_interpunctuation=args.ignore_punctuation,
            )
        )
