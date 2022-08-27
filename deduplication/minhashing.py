import uuid
from dataclasses import dataclass, field
from typing import Set

import datasketch


@dataclass
class DocumentSketch:
    doc_id: uuid.UUID
    sketch: datasketch.MinHash
    file_name: str
    candidates: list = field(default_factory=list)


class MinHasher:
    def __init__(self, num_perm: int = 128):
        self._num_perm = num_perm

    def create_document_sketch(
        self, file_name: str, shingle_set: Set[str]
    ) -> DocumentSketch:
        return DocumentSketch(
            doc_id=uuid.uuid4(),
            sketch=self.create_minhash_from_shingle_set(shingle_set),
            file_name=file_name,
        )

    def create_minhash_from_shingle_set(self, shingles: Set[str]) -> datasketch.MinHash:
        minhash = datasketch.MinHash(self._num_perm)
        minhash.update_batch([shingle.encode("utf-8") for shingle in shingles])
        return minhash
