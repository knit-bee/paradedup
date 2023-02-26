import unittest
from typing import Optional

from deduplication.cli.controller import DedupController
from deduplication.cli.use_case import Request


class MockUseCase:
    def __init__(self) -> None:
        self.request: Optional[Request] = None

    def process(self, request: Request) -> None:
        assert not self.request
        self.request = request


class DedupControllerTester(unittest.TestCase):
    def setUp(self):
        self.use_case = MockUseCase()
        self.controller = DedupController(self.use_case)

    def test_controller_extracts_input_dir_name(self):
        dir_name = "test"
        self.controller.process_arguments([dir_name])
        self.assertEqual(self.use_case.request.directory, dir_name)

    def test_controller_extracts_output_file_name(self):
        output = "out.json"
        self.controller.process_arguments(["test", "--output", output])
        self.assertEqual(self.use_case.request.output_file, output)

    def test_controller_extracts_output_file_name_with_short_handle(self):
        output = "out.json"
        self.controller.process_arguments(["test", "-o", output])
        self.assertEqual(self.use_case.request.output_file, output)

    def test_default_for_output_file_set_if_not_passed(self):
        self.controller.process_arguments(["test"])
        self.assertEqual(self.use_case.request.output_file, "output.json")

    def test_controller_extracts_character_level(self):
        self.controller.process_arguments(["test", "--character-shingle"])
        self.assertEqual(self.use_case.request.use_token, False)

    def test_controller_extracts_character_level_with_flag(self):
        self.controller.process_arguments(["test", "-s"])
        self.assertEqual(self.use_case.request.use_token, False)

    def test_default_for_processing_options(self):
        self.controller.process_arguments(["test"])
        expected = Request(
            directory="test",
            output_file="output.json",
            use_token=True,
            shingle_size=3,
            case_insensitive=False,
            ignore_nums=False,
            normalize_whitespace=False,
            ignore_interpunctuation=False,
            num_perm=128,
            threshold=0.9,
        )
        self.assertEqual(self.use_case.request, expected)

    def test_controller_extracts_shingle_size(self):
        self.controller.process_arguments(["test", "--shingle-size", "4"])
        self.assertEqual(self.use_case.request.shingle_size, 4)

    def test_controller_extracts_shingle_size_with_flag(self):
        self.controller.process_arguments(["test", "-k", "11"])
        self.assertEqual(self.use_case.request.shingle_size, 11)

    def test_invalid_input_rejected_for_shingle_size(self):
        shingle_size_input = ["0", "1.5", "three", "0.4", "1.1", "abc", "-1"]
        for size in shingle_size_input:
            with self.subTest():
                with self.assertRaises(SystemExit):
                    self.controller.process_arguments(["test", "-k", size])

    def test_controller_extracts_case_option(self):
        self.controller.process_arguments(["test", "--case-insensitive"])
        self.assertTrue(self.use_case.request.case_insensitive)

    def test_controller_extracts_case_option_with_flag(self):
        self.controller.process_arguments(["test", "-c"])
        self.assertTrue(self.use_case.request.case_insensitive)

    def test_controller_extracts_number_option(self):
        self.controller.process_arguments(["test", "--ignore-numbers"])
        self.assertTrue(self.use_case.request.ignore_nums)

    def test_controller_extracts_number_option_with_flag(self):
        self.controller.process_arguments(["test", "-n"])
        self.assertTrue(self.use_case.request.ignore_nums)

    def test_controller_extracts_whitespace_option(self):
        self.controller.process_arguments(["test", "--ignore-whitespace"])
        self.assertTrue(self.use_case.request.normalize_whitespace)

    def test_controller_extracts_whitespace_option_with_flag(self):
        self.controller.process_arguments(["test", "-w"])
        self.assertTrue(self.use_case.request.normalize_whitespace)

    def test_controller_extracts_punctuation_option(self):
        self.controller.process_arguments(["test", "--ignore-punctuation"])
        self.assertTrue(self.use_case.request.ignore_interpunctuation)

    def test_controller_extracts_punctuation_option_with_flag(self):
        self.controller.process_arguments(["test", "-i"])
        self.assertTrue(self.use_case.request.ignore_interpunctuation)

    def test_controller_extracts_number_of_permutations(self):
        self.controller.process_arguments(["test", "--permutations", "64"])
        self.assertEqual(self.use_case.request.num_perm, 64)

    def test_controller_extracts_number_of_permutations_with_flag(self):
        self.controller.process_arguments(["test", "-p", "44"])
        self.assertEqual(self.use_case.request.num_perm, 44)

    def test_invalid_values_for_permutaiton_rejected(self):
        invalid_values = ["0", "1", "-1", "0.4", "3.6", f"{(2**32)+1}"]
        for num_perm in invalid_values:
            with self.subTest():
                with self.assertRaises(SystemExit):
                    self.controller.process_arguments(
                        ["test", "--permutations", num_perm]
                    )

    def test_controller_extracts_lsh_threshold(self):
        self.controller.process_arguments(["test", "--lsh-threshold", "0.5"])
        self.assertEqual(self.use_case.request.threshold, 0.5)

    def test_controller_extracts_lsh_threshold_with_flag(self):
        self.controller.process_arguments(["test", "-l", "0.75"])
        self.assertEqual(self.use_case.request.threshold, 0.75)

    def test_invalid_values_for_lsh_rejected(self):
        invalid_values = ["1.1", "-0.1", "2", "1.5"]
        for lsh in invalid_values:
            with self.subTest():
                with self.assertRaises(SystemExit):
                    self.controller.process_arguments(["test", "--lsh-threshold", lsh])

    def test_use_of_whitespace_option_defaults_to_character_level(self):
        self.controller.process_arguments(["test", "--ignore-whitespace"])
        self.assertEqual(self.use_case.request.use_token, False)
