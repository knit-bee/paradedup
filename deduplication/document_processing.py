import os
from typing import Generator, Protocol


class DocumentProcessor(Protocol):
    def load_files(self, directory: str) -> Generator[str, None, None]:
        ...


class DocumentProcessorImpl:
    def load_files(self, directory: str) -> Generator[str, None, None]:
        for root, dirs, files in os.walk(directory):
            for file in files:
                with open(os.path.join(root, file)) as ptr:
                    yield ptr.read()
