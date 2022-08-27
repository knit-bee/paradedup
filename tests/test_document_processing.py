import os
import unittest

from deduplication.document_processing import DocumentProcessorImpl


class FileProcessorTester(unittest.TestCase):
    def setUp(self):
        self.processor = DocumentProcessorImpl()
        self.test_data = os.path.join("tests", "testdata")

    def test_all_files_from_directory_loaded(self):
        test_dir = os.path.join(self.test_data, "txt")
        file_content = sorted(
            [content.strip() for _, content in self.processor.load_files(test_dir)]
        )
        expected = [
            "first sentence, text. more text.",
            "sentence with some text. second sentence with some text.",
            "some text that is only a paragraph.",
        ]
        self.assertEqual(file_content, expected)

    def test_all_file_from_directory_with_subdirs_loaded(self):
        test_dir = os.path.join(self.test_data, "nested")
        no_files = len(list(self.processor.load_files(test_dir)))
        self.assertEqual(no_files, 9)

    def test_empty_directory_returns_empty_directory(self):
        test_dir = os.path.join(self.test_data, "empty")
        result = list(self.processor.load_files(test_dir))
        self.assertEqual(result, [])
