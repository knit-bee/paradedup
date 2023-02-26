import json
from dataclasses import dataclass
from typing import Protocol

from deduplication.candidate_ranker import CandidateRanker
from deduplication.candidate_searcher import CandidateSearcher
from deduplication.document_processing import DocumentProcessorImpl
from deduplication.minhashing import MinHasher
from deduplication.pipeline import NddPipeline
from deduplication.preprocessor import Preprocessor


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
        preprocessor = Preprocessor(
            shingle_size=request.shingle_size,
            case_insensitive=request.case_insensitive,
            ignore_nums=request.ignore_nums,
            normalize_whitespace=request.normalize_whitespace,
            ignore_interpunctuation=request.ignore_interpunctuation,
            use_token=request.use_token,
        )
        minhasher = MinHasher(num_perm=request.num_perm)
        doc_processor = DocumentProcessorImpl()
        candidate_searcher = CandidateSearcher(
            lsh_threshold=request.threshold, num_perm=request.num_perm
        )
        candidate_ranker = CandidateRanker()
        pipeline = NddPipeline(
            doc_processor, preprocessor, minhasher, candidate_searcher, candidate_ranker
        )
        pipeline.process_files(request.directory)
        nd_candidates = pipeline.find_near_duplicates()
        with open(request.output_file, "w") as fh:
            json.dump(nd_candidates, fh)
