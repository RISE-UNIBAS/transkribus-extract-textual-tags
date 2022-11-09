""" test.py

Unittest. """

import os.path
import unittest
from transkribus_extract_textual_tags.client import Client

DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(os.path.dirname(__file__))


class TestClient(unittest.TestCase):
    """ Test GoldStandard. """

    def setUp(self) -> None:
        self.input = DIR + "/data"
        self.client = Client
        self.benchmark = DIR + "/benchmark.csv"
        self.output = DIR + "/output.csv"

    def test_extract_from_dir(self):
        """ Test extract_from_dir method. """

        with open(self.benchmark, mode="r", encoding="utf-8") as file:
            benchmark = file.read()
        self.client.extract_from_dir(dir_path=self.input,
                                     save_file_path=self.output)
        with open(self.output, mode="r", encoding="utf-8") as file:
            output = file.read()
        self.assertEqual(benchmark, output)


if __name__ == '__main__':
    unittest.main()
