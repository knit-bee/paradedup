import unittest

from deduplication.preprocessor import Preprocessor


class PreprocessorTester(unittest.TestCase):
    def setUp(self):
        self.doc = """This is   a  test Text with  numbers like 1, 2, 3 and five
and interpunction and other symbols like @, ! [] for testing. It also contains
German letters like ä, Ö & ßẞ  !"""

    def test_preprocessing_whitespace_removed(self):
        preprocessor = Preprocessor(normalize_whitespace=True)
        result = preprocessor.preprocess_document(self.doc)
        self.assertEqual(
            result,
            "This is a test Text with numbers like 1, 2, 3 and five and "
            "interpunction and other symbols like @, ! [] for testing. It also "
            "contains German letters like ä, Ö & ßẞ !",
        )

    def test_preprocessing_numbers_removed(self):
        preprocessor = Preprocessor(ignore_nums=True)
        result = preprocessor.preprocess_document(self.doc)
        self.assertEqual(
            result,
            "This is   a  test Text with  numbers like , ,  and five "
            "and interpunction and other symbols like @, ! [] for testing. It also contains "
            "German letters like ä, Ö & ßẞ  !",
        )

    def test_preprocessing_interpunction_removed(self):
        preprocessor = Preprocessor(ignore_interpunctuation=True)
        result = preprocessor.preprocess_document(self.doc)
        self.assertEqual(
            result,
            "This is   a  test Text with  numbers like 1 2 3 and five "
            "and interpunction and other symbols like    for testing It also contains "
            "German letters like ä Ö  ßẞ  ",
        )

    def test_preprocessing_case_normalized(self):
        preprocessor = Preprocessor(case_insensitive=True)
        result = preprocessor.preprocess_document(self.doc)
        self.assertEqual(
            result,
            "this is   a  test text with  numbers like 1, 2, 3 and five "
            "and interpunction and other symbols like @, ! [] for testing. it also contains "
            "german letters like ä, ö & ßß  !",
        )

    def test_preprocessing_shingling_token(self):
        expected_outcome = {
            1: {
                "This",
                "is",
                "a",
                "test",
                "Text",
                "with",
                "numbers",
                "like",
                "1",
                ",",
            },
            2: {
                "This~is",
                "is~a",
                "a~test",
                "test~Text",
                "Text~with",
                "with~numbers",
                "numbers~like",
                "like~1",
                "1~,",
            },
            3: {
                "This~is~a",
                "is~a~test",
                "a~test~Text",
                "test~Text~with",
                "Text~with~numbers",
                "with~numbers~like",
                "numbers~like~1",
                "like~1~,",
                "1~,~",
                ",~~",
            },
            4: {
                "This~is~a~test",
                "is~a~test~Text",
                "a~test~Text~with",
                "test~Text~with~numbers",
                "Text~with~numbers~like",
                "with~numbers~like~1",
                "numbers~like~1~,",
                "like~1~,~",
                "1~,~~",
            },
            7: {
                "This~is~a~test~Text~with~numbers",
                "is~a~test~Text~with~numbers~like",
                "a~test~Text~with~numbers~like~1",
                "test~Text~with~numbers~like~1~,",
                "Text~with~numbers~like~1~,~",
                "with~numbers~like~1~,~~",
                "numbers~like~1~,~~~",
                "like~1~,~~~~",
            },
        }
        for k, expected in expected_outcome.items():
            preprocessor = Preprocessor(shingle_size=k)
            with self.subTest(i=k):
                result = preprocessor.create_shingle_set(self.doc[:44])
                self.assertEqual(result, expected)

    def test_preprocess_shingling_character(self):
        expected_outcome = {
            3: {
                "Thi",
                "his",
                "is ",
                "s i",
                " is",
                "s  ",
                "   ",
                "  a",
                " a ",
                "a  ",
                "  t",
                " te",
                "tes",
                "est",
                "st ",
            },
            4: {
                "This",
                "his ",
                "is i",
                "s is",
                " is ",
                "is  ",
                "s   ",
                "   a",
                "  a ",
                " a  ",
                "a  t",
                "  te",
                " tes",
                "test",
                "est ",
            },
            5: {
                "This ",
                "his i",
                "is is",
                "s is ",
                " is  ",
                "is   ",
                "s   a",
                "   a ",
                "  a  ",
                " a  t",
                "a  te",
                "  tes",
                " test",
                "test ",
            },
            6: {
                "This i",
                "his is",
                "is is ",
                "s is  ",
                " is   ",
                "is   a",
                "s   a ",
                "   a  ",
                "  a  t",
                " a  te",
                "a  tes",
                "  test",
                " test ",
            },
        }
        for k, expected in expected_outcome.items():
            preprocessor = Preprocessor(shingle_size=k, use_token=False)
            with self.subTest(i=k):
                result = preprocessor.create_shingle_set(self.doc[:20])
                self.assertEqual(result, expected)

    def test_shingles_padded_mit_empty_string_if_count_less_than_shingle_size(self):
        test_doc = "Wesensunterschied Transformation"
        preprocessor = Preprocessor(shingle_size=3)
        result = preprocessor.create_shingle_set(test_doc)
        self.assertEqual(result, {"Wesensunterschied~Transformation~"})
