import unittest
from uuid import UUID

from datasketch import MinHash

from deduplication.minhashing import DocumentSketch, MinHasher


class MinHasherTester(unittest.TestCase):
    def test_returns_minhash(self):
        minhasher = MinHasher()
        shingle_set = {"a", "b", "c"}
        result = minhasher.create_minhash_from_shingle_set(shingle_set)
        self.assertTrue(isinstance(result, MinHash))

    def test_entering_same_strings_results_in_same_minhash(self):
        minhasher = MinHasher()
        shingle_set1 = {"a", "b", "c"}
        shingle_set2 = {"a", "b", "c"}
        minhash1 = minhasher.create_minhash_from_shingle_set(shingle_set1)
        minhash2 = minhasher.create_minhash_from_shingle_set(shingle_set2)
        self.assertEqual(minhash1, minhash2)

    def test_different_strings_result_in_different_minhash(self):
        minhasher = MinHasher()
        shingle_set1 = {"a", "b", "c"}
        shingle_set2 = {"a", "d", "e"}
        minhash1 = minhasher.create_minhash_from_shingle_set(shingle_set1)
        minhash2 = minhasher.create_minhash_from_shingle_set(shingle_set2)
        self.assertTrue(minhash1 != minhash2)

    def test_differnt_number_of_permutations_results_in_different_minhash(self):
        minhasher1 = MinHasher(128)
        minhasher2 = MinHasher(64)
        shingle_set = {"a", "b", "c"}
        minhash1 = minhasher1.create_minhash_from_shingle_set(shingle_set)
        minhash2 = minhasher2.create_minhash_from_shingle_set(shingle_set)
        self.assertTrue(minhash1 != minhash2)

    def test_id_of_document_sketch_is_UUID(self):
        minhasher = MinHasher()
        shingle_set = {"a", "b", "c"}
        doc = minhasher.create_document_sketch(shingle_set)
        self.assertTrue(isinstance(doc.doc_id, UUID))

    def test_returns_document_sketch(self):
        minhasher = MinHasher()
        shingle_set = {"a", "b", "c"}
        doc = minhasher.create_document_sketch(shingle_set)
        self.assertTrue(isinstance(doc, DocumentSketch))

    def test_candidate_list_of_document_empty_after_creation(self):
        minhasher = MinHasher()
        shingle_set = {"a", "b", "c"}
        doc = minhasher.create_document_sketch(shingle_set)
        self.assertEqual(doc.candidates, [])

    def test_document_sketch_contains_minhash(self):
        minhasher = MinHasher()
        shingle_set = {"a", "b", "c"}
        doc = minhasher.create_document_sketch(shingle_set)
        self.assertTrue(isinstance(doc.sketch, MinHash))
