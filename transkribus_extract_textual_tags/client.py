""" client.py

Client class. """

from transkribus_extract_textual_tags.tags import Document
from transkribus_extract_textual_tags.utility import Utility
import os


class Client:
    """ Standalone client. """

    @staticmethod
    def extract_from_file(file_path: str) -> None:
        """ Extract tags from file with Transkribus PAGE XML documents.

        :param file_path:
        """

        tags = Document(file_path=file_path).get_tags()

        pass

    @staticmethod
    def extract_from_dir(dir_path: str,
                         save_file_path: str) -> None:
        """ Extract tags from directory with Transkribus PAGE XML documents.

        :param dir_path: the complete path to the directory
        :param save_file_path: the complete path to the save file (need not exist yet)
        """

        try:
            os.path.exists(dir_path)
        except FileNotFoundError:
            raise

        tags = []
        for file in os.listdir(dir_path):
            if not file.endswith(".xml"):
                continue
            tags = tags + Document(file_path=f"{dir_path}/{file}").get_tags()

        Utility.write_csv(save_file_path=save_file_path,
                          tags=tags)
