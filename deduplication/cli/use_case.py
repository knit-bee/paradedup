from dataclasses import dataclass
from typing import Protocol


@dataclass
class Request:
    directory: str
    output_file: str


class DeduplicationUseCase(Protocol):
    def process(self, request: Request) -> None:
        ...


class DeduplicationUseCaseImpl:
    """Use case for deduplication pipeline call from command line"""

    def process(self, request: Request) -> None:
        pass
