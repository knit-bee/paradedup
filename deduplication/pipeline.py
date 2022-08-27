from dataclasses import dataclass, field
from typing import Dict
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

    def find_near_duplicates(self, directory: str) -> Dict[str, list]:
        for file_name, content in self.document_processor.load_files(directory):
            self._add_file_to_database(file_name, content)
        nd_candidates = {}
        for file_id, doc_sketch in self.id_to_doc_sketch_mapping.items():
            candidates = self.candidate_searcher.get_candidates_for_document(doc_sketch)
            nd_candidates[doc_sketch.file_name] = [
                self.id_to_doc_sketch_mapping[candidate].file_name
                for candidate in candidates
            ]
        return nd_candidates

    def _add_file_to_database(self, file_name: str, file_content: str) -> None:
        shingles = self.preprocessor.preprocess_document(file_content)
        doc_sketch = self.minhasher.create_document_sketch(file_name, shingles)
        self.id_to_doc_sketch_mapping[doc_sketch.doc_id] = doc_sketch
        self.candidate_searcher.insert_document_sketch(doc_sketch)
