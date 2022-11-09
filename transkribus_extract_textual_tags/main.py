""" main.py

Main app. """

from transkribus_extract_textual_tags.client import Client

import os.path

DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
TESTS = f"{PARENT_DIR}/TESTS"

Client.extract_from_dir(dir_path=f"{TESTS}/data/",
                        save_file_path="test.csv")
