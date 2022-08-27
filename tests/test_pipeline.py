import unittest
from typing import Generator, Tuple

from deduplication.candidate_ranker import CandidateRanker
from deduplication.candidate_searcher import CandidateSearcher
from deduplication.minhashing import MinHasher
from deduplication.pipeline import NddPipeline
from deduplication.preprocessor import Preprocessor


class MockDocumentProcessor:
    test_data = [
        "Lorem ipsum dolor sit amet, consectetur adipisici elit, sed"
        " eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim"
        " veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex ea commodi consequat.",
        " eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim"
        "Lorem ipsum dolor sit amet, consectetur adipisici elit, sed"
        " veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex ea commodi consequat.",
        "ein anderer Text, der ganz anders ist und nicht als Duplikat gefunden werden sollte",
    ]

    def load_files(self, directory: str) -> Generator[Tuple[str, str], None, None]:
        for i, doc in enumerate(self.test_data):
            yield f"file{i}", doc


class NddPipelineTester(unittest.TestCase):
    def setUp(self):
        self.doc_processor = MockDocumentProcessor()
        self.preprocessor = Preprocessor()
        self.minhasher = MinHasher()
        self.searcher = CandidateSearcher()
        self.ranker = CandidateRanker()
        self.pipeline = NddPipeline(
            document_processor=self.doc_processor,
            preprocessor=self.preprocessor,
            minhasher=self.minhasher,
            candidate_searcher=self.searcher,
            candidate_ranker=self.ranker,
        )

    def test_run_pipeline(self):
        result = self.pipeline.find_near_duplicates("mock_dir")
        self.assertEqual(result, {"file0": ["file1"], "file1": ["file0"], "file2": []})
