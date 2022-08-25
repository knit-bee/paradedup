import unittest

from deduplication.candidate_ranker import CandidateRanker
from deduplication.minhashing import MinHasher


class CandidateRankerTester(unittest.TestCase):
    def setUp(self):
        self.minhasher = MinHasher()
        self.candidate_ranker = CandidateRanker()

    def test_candidates_ranked_according_to_similarity_score(self):
        target = self.minhasher.create_document_sketch({"aa", "ab", "ba"})
        candidate1 = self.minhasher.create_document_sketch({"aa", "ab", "ba"})
        candidate2 = self.minhasher.create_document_sketch({"aa", "ab", "bc"})
        ranking = self.candidate_ranker.rank_candidates(
            target, [candidate1, candidate2]
        )
        expected = [(candidate1.doc_id, 1), (candidate2.doc_id, 0.5)]
        self.assertEqual(ranking, expected)

    def test_empty_candidate_list_returns_empty_ranking(self):
        target = self.minhasher.create_document_sketch({"aa", "ab", "ba"})
        ranking = self.candidate_ranker.rank_candidates(target, [])
        self.assertEqual(ranking, [])

    def test_tie_candidates_sorted_according_to_insertion_order(self):
        target = self.minhasher.create_document_sketch({"aa", "ab", "ba"})
        candidate1 = self.minhasher.create_document_sketch({"aa", "ab", "bc"})
        candidate1.doc_id = "c_first"
        candidate2 = self.minhasher.create_document_sketch({"aa", "ab", "bc"})
        candidate2.doc_id = "a_second"
        candidate3 = self.minhasher.create_document_sketch({"aa", "ab", "bc"})
        candidate3.doc_id = "b_third"
        ranking = self.candidate_ranker.rank_candidates(
            target, [candidate1, candidate2, candidate3]
        )
        self.assertEqual(
            ranking, [("c_first", 0.5), ("a_second", 0.5), ("b_third", 0.5)]
        )
