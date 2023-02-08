import uuid
from typing import List

import datasketch

from deduplication.minhashing import DocumentSketch


class CandidateSearcher:
    def __init__(self, lsh_threshold: float = 0.9, num_perm: int = 128):
        self.threshold = lsh_threshold
        self.lsh = datasketch.MinHashLSH(threshold=lsh_threshold, num_perm=num_perm)

    def insert_document_sketch(self, document_sketch: DocumentSketch) -> None:
        self.lsh.insert(
            document_sketch.doc_id, document_sketch.sketch, check_duplication=False
        )

    def get_candidates_for_document(
        self, document_sketch: DocumentSketch
    ) -> List[uuid.UUID]:
        candidates = [
            doc_id
            for doc_id in self.lsh.query(document_sketch.sketch)
            if doc_id != document_sketch.doc_id
        ]
        return candidates
