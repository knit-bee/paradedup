from dataclasses import dataclass, field
from typing import Dict, List, Tuple
from uuid import UUID

from deduplication.candidate_ranker import CandidateRanker
from deduplication.candidate_searcher import CandidateSearcher
from deduplication.document_processing import DocumentProcessor
from deduplication.minhashing import DocumentSketch, MinHasher
from deduplication.preprocessor import Preprocessor


@dataclass
class NddPipeline:
    document_processor: DocumentProcessor
    preprocessor: Preprocessor
    minhasher: MinHasher
    candidate_searcher: CandidateSearcher
    candidate_ranker: CandidateRanker
    id_to_doc_sketch_mapping: Dict[UUID, DocumentSketch] = field(default_factory=dict)

    def process_files(self, directory: str) -> None:
        for file_name, content in self.document_processor.load_files(directory):
            self._add_file_to_database(file_name, content)

    def find_near_duplicates(self) -> Dict[str, List[Tuple[str, float]]]:
        nd_candidates = {}
        for file_id, doc_sketch in self.id_to_doc_sketch_mapping.items():
            candidates = [
                self.id_to_doc_sketch_mapping[candidate]
                for candidate in self.candidate_searcher.get_candidates_for_document(
                    doc_sketch
                )
            ]
            ranked = self.candidate_ranker.rank_candidates(doc_sketch, candidates)
            nd_candidates[doc_sketch.file_name] = [
                (self.id_to_doc_sketch_mapping[candidate].file_name, sim_score)
                for candidate, sim_score in ranked
            ]
        return nd_candidates

    def _add_file_to_database(self, file_name: str, file_content: str) -> None:
        processed = self.preprocessor.preprocess_document(file_content)
        shingles = self.preprocessor.create_shingle_set(processed)
        doc_sketch = self.minhasher.create_document_sketch(file_name, shingles)
        self.id_to_doc_sketch_mapping[doc_sketch.doc_id] = doc_sketch
        self.candidate_searcher.insert_document_sketch(doc_sketch)
