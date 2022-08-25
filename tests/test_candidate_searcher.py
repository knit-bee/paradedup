import unittest

import datasketch

from deduplication.candidate_searcher import CandidateSearcher
from deduplication.minhashing import MinHasher


class CandidateSearcherTester(unittest.TestCase):
    def setUp(self):
        self.minhasher = MinHasher()

    def test_lsh_initialized(self):
        searcher = CandidateSearcher()
        self.assertTrue(isinstance(searcher.lsh, datasketch.MinHashLSH))

    def test_doc_sketch_inserted_in_lsh(self):
        searcher = CandidateSearcher()
        doc_sketch = self.minhasher.create_document_sketch({"a", "b", "c"})
        searcher.insert_document_sketch(doc_sketch)
        self.assertTrue(doc_sketch.doc_id in searcher.lsh)

    def test_get_candidates_for_document(self):
        searcher = CandidateSearcher(lsh_threshold=0.5)
        doc_sketch1 = self.minhasher.create_document_sketch({"aa", "ab"})
        doc_sketch2 = self.minhasher.create_document_sketch({"aa", "ab", "bb"})
        searcher.insert_document_sketch(doc_sketch1)
        searcher.insert_document_sketch(doc_sketch2)
        candidates = searcher.get_candidates_for_document(doc_sketch1)
        self.assertTrue(doc_sketch2.doc_id in candidates)

    def test_query_doc_excluded_from_candidates(self):
        searcher = CandidateSearcher()
        doc_sketch = self.minhasher.create_document_sketch({"aa", "ab"})
        searcher.insert_document_sketch(doc_sketch)
        candidates = searcher.get_candidates_for_document(doc_sketch)
        self.assertEqual(candidates, [])

    def test_empty_list_returned_for_when_no_candidates_above_threshold(self):
        searcher = CandidateSearcher(lsh_threshold=0.9)
        doc_sketch1 = self.minhasher.create_document_sketch({"aa", "ab"})
        doc_sketch2 = self.minhasher.create_document_sketch({"aa", "ab", "bb"})
        searcher.insert_document_sketch(doc_sketch1)
        searcher.insert_document_sketch(doc_sketch2)
        candidates = searcher.get_candidates_for_document(doc_sketch1)
        self.assertEqual(candidates, [])
