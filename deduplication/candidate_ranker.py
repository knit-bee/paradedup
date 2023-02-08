from typing import List, Tuple
from uuid import UUID

from deduplication.minhashing import DocumentSketch


class CandidateRanker:
    def _compute_document_similarity(
        self, target_doc: DocumentSketch, other_doc: DocumentSketch
    ) -> float:
        return target_doc.sketch.jaccard(other_doc.sketch)

    def rank_candidates(
        self, target_doc: DocumentSketch, candidates: List[DocumentSketch]
    ) -> List[Tuple[UUID, float]]:
        candidate_ranking = []
        for doc in candidates:
            similarity_score = self._compute_document_similarity(target_doc, doc)
            candidate_ranking.append((doc.doc_id, similarity_score))

        return sorted(candidate_ranking, key=lambda x: x[1], reverse=True)
