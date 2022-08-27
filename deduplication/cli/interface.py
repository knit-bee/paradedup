import logging
import sys

from deduplication.cli.controller import DedupController
from deduplication.cli.use_case import DeduplicationUseCaseImpl

logging.basicConfig(
    filename="ndd.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s: %(message)s",
)
logger = logging.getLogger()


def main() -> None:
    args = sys.argv[1:]

    use_case = DeduplicationUseCaseImpl()
    controller = DedupController(use_case)
    controller.process_arguments(args)
