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
        output = "out.csv"
        self.controller.process_arguments(["test", "--output", output])
        self.assertEqual(self.use_case.request.output_file, output)

    def test_controller_extracts_output_file_name_with_short_handle(self):
        output = "out.csv"
        self.controller.process_arguments(["test", "-o", output])
        self.assertEqual(self.use_case.request.output_file, output)

    def test_default_for_output_file_set_if_not_passed(self):
        self.controller.process_arguments(["test"])
        self.assertEqual(self.use_case.request.output_file, "output.csv")
