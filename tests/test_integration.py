import unittest

from deduplication.cli.use_case import DeduplicationUseCaseImpl


class IntegrationTester(unittest.TestCase):
    def setUp(self):
        self.use_case = DeduplicationUseCaseImpl()
