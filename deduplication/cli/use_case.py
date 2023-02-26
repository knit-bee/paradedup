from dataclasses import dataclass
from typing import Protocol

from deduplication.pipeline import NddPipeline


@dataclass
class Request:
    directory: str
    output_file: str
    num_perm: int = 128
    threshold: float = 0.9
    shingle_size: int = 3
    use_token: bool = True
    case_insensitive: bool = False
    normalize_whitespace: bool = False
    ignore_nums: bool = False
    ignore_interpunctuation: bool = False


class DeduplicationUseCase(Protocol):
    def process(self, request: Request) -> None:
        ...


class DeduplicationUseCaseImpl:
    """Use case for deduplication pipeline call from command line"""

    def process(self, request: Request) -> None:
        pass
