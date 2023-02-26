import json
import os
import unittest

from deduplication.cli.use_case import DeduplicationUseCaseImpl, Request


class IntegrationTester(unittest.TestCase):
    def setUp(self):
        self.use_case = DeduplicationUseCaseImpl()
        self.out_file = os.path.join("tests", "test.out.json")

    def tearDown(self):
        if os.path.exists(self.out_file):
            os.remove(self.out_file)

    def test_run_deduplication_with_directory(self):
        test_dir = os.path.join("tests", "testdata", "txt")
        request = Request(directory=test_dir, output_file=self.out_file)
        self.use_case.process(request)
        with open(self.out_file, "r") as fh:
            content = json.load(fh)
        self.assertEqual(
            list(content.keys()),
            [
                os.path.join("tests", "testdata", "txt", "file2.txt"),
                os.path.join("tests", "testdata", "txt", "file3.txt"),
                os.path.join("tests", "testdata", "txt", "file1.txt"),
            ],
        )

    def test_run_deduplication_with_empty_directory(self):
        test_dir = os.path.join("tests", "testdata", "empty")
        request = Request(directory=test_dir, output_file=self.out_file)
        self.use_case.process(request)
        with open(self.out_file, "r") as fh:
            content = json.load(fh)
        self.assertEqual(
            list(content.keys()),
            [],
        )

    def test_run_deduplication_with__char_shingle_option(self):
        test_dir = os.path.join("tests", "testdata", "nested")
        request = Request(
            directory=test_dir, output_file=self.out_file, use_token=False
        )
        self.use_case.process(request)
        with open(self.out_file, "r") as fh:
            content = json.load(fh)
        result = {
            os.path.basename(file): sorted(
                [os.path.basename(candidate[0]) for candidate in candidates]
            )
            for file, candidates in content.items()
        }
        self.assertEqual(
            result,
            {
                "file111.txt": ["file121.txt", "file211.txt"],
                "file112.txt": ["file122.txt", "file212.txt"],
                "file113.txt": ["file123.txt", "file213.txt"],
                "file121.txt": ["file111.txt", "file211.txt"],
                "file122.txt": ["file112.txt", "file212.txt"],
                "file123.txt": ["file113.txt", "file213.txt"],
                "file211.txt": ["file111.txt", "file121.txt"],
                "file212.txt": ["file112.txt", "file122.txt"],
                "file213.txt": ["file113.txt", "file123.txt"],
            },
        )

    def test_run_deduplication_with_other_options(self):
        test_dir = os.path.join("tests", "testdata", "nested", "subdir1", "dir1")
        request = Request(
            directory=test_dir,
            output_file=self.out_file,
            use_token=False,
            shingle_size=3,
            num_perm=8,
            threshold=0.4,
        )
        self.use_case.process(request)
        with open(self.out_file, "r") as fh:
            content = json.load(fh)
        result = {
            os.path.basename(file): [
                os.path.basename(candidate[0]) for candidate in candidates
            ]
            for file, candidates in content.items()
        }
        self.assertEqual(
            result,
            {
                "file111.txt": ["file113.txt"],
                "file112.txt": [],
                "file113.txt": ["file111.txt"],
            },
        )
