import argparse
from typing import List

from deduplication.cli.use_case import DeduplicationUseCase, Request


class DedupController:
    def __init__(self, use_case: DeduplicationUseCase) -> None:
        self.use_case = use_case

    def process_arguments(self, arguments: List[str]) -> None:
        parser = argparse.ArgumentParser(description="""description goes here""")
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
        args = parser.parse_args(arguments)
        self.use_case.process(
            Request(
                directory=args.directory,
                output_file=args.output,
            )
        )
