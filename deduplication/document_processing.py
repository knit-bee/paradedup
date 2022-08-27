import os
from typing import Generator, Protocol, Tuple


class DocumentProcessor(Protocol):
    def load_files(self, directory: str) -> Generator[Tuple[str, str], None, None]:
        ...


class DocumentProcessorImpl:
    def load_files(self, directory: str) -> Generator[Tuple[str, str], None, None]:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path) as ptr:
                    yield file_path, ptr.read()
