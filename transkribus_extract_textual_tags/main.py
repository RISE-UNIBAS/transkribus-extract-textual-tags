""" main.py

Main app. """

from transkribus_extract_textual_tags.client import Client
import os.path

PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
SAMPLE_DIR = f"{PARENT_DIR}/sample"


def main():
    """ Run the app on the sample data. """

    Client.extract_from_dir(dir_path=f"{SAMPLE_DIR}",
                            save_file_path=f"{SAMPLE_DIR}/sample.csv")


if __name__ == "__main__":
    main()
