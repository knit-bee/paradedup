import unittest
from typing import Generator, Tuple
from uuid import UUID

from deduplication.candidate_ranker import CandidateRanker
from deduplication.candidate_searcher import CandidateSearcher
from deduplication.minhashing import DocumentSketch, MinHasher
from deduplication.pipeline import NddPipeline
from deduplication.preprocessor import Preprocessor


class MockDocumentProcessor:
    test_data = [
        # file0
        "Lorem ipsum dolor sit amet, consectetur adipisici elit, sed"
        " eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim"
        " veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex ea commodi consequat.",
        # file1
        " eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim"
        "Lorem ipsum dolor sit amet, consectetur adipisici elit, sed"
        " veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex ea commodi consequät.",
        # file2
        " eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim"
        "Lorem ipsum dolor sit amet, consectetur adipisici elit, sed"
        " veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex ea commodi consequat.",
        # file3
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
        self.searcher = CandidateSearcher(lsh_threshold=0.3)
        self.ranker = CandidateRanker()
        self.pipeline = NddPipeline(
            document_processor=self.doc_processor,
            preprocessor=self.preprocessor,
            minhasher=self.minhasher,
            candidate_searcher=self.searcher,
            candidate_ranker=self.ranker,
        )

    def test_process_files(self):
        self.pipeline.process_files("mock_dir")
        self.assertTrue(
            isinstance(list(self.pipeline.id_to_doc_sketch_mapping.keys())[0], UUID)
        )
        self.assertTrue(
            isinstance(
                list(self.pipeline.id_to_doc_sketch_mapping.values())[0], DocumentSketch
            )
        )

    def test_candidates_found(self):
        self.pipeline.process_files("mock_dir")
        ranked = self.pipeline.find_near_duplicates()
        result = {
            key: [filename for filename, score in val] for key, val in ranked.items()
        }
        self.assertEqual(
            result,
            {
                "file0": ["file2", "file1"],
                "file1": ["file2", "file0"],
                "file2": ["file1", "file0"],
                "file3": [],
            },
        )

    def test_candidates_ranked(self):
        self.pipeline.process_files("mock_dir")
        ranked = self.pipeline.find_near_duplicates()
        for file, results in ranked.items():
            with self.subTest():
                self.assertEqual(
                    sorted(results, key=lambda x: x[1], reverse=True), results
                )
