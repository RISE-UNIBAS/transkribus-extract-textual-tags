""" main.py

"""

from __future__ import annotations
from lxml import etree

import os.path
import re


DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
TESTS = f"{PARENT_DIR}/TESTS"


"""
outline

- load page xml à la transkribus from file or folder
- indicate which tags to export, default all
- save tags as csv json or similar

"""


def main(file_path: str) -> None:
    """

    :param file_path:
    """

    tree = etree.parse(file_path)

    text_lines = []
    for element in tree.findall(".//{http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15}TextLine"):
        text_lines.append(TextLine(element=element))


    for text_line in text_lines:
        print(text_line.get_id())
        print(text_line.get_custom())
        print(text_line.get_coords_points())
        print(text_line.get_baseline_points())
        print(text_line.get_text())

        text_line.extract_tags()

        exit()


class TextLine:
    """ A representation of a Transkribus PAGE XML 'TextLine' element. """

    def __init__(self,
                 element: etree._Element
                 ) -> None:
        self.element = element

    def get_id(self) -> str:
        """ Get 'id' attribute. """

        return self.element.attrib["id"]

    def get_custom(self) -> str:
        """ Get 'custom' attribute. """

        return self.element.attrib["custom"]

    def get_coords_points(self) -> str:
        """ Get 'points' attribute from 'Coords' subelement. """

        for subelement in self.element.findall(".//{http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15}Coords"):
            return subelement.attrib["points"]

    def get_baseline_points(self) -> str:
        """ Get 'points' attribute from 'Baseline' subelement. """

        for subelement in self.element.findall(".//{http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15}Baseline"):
            return subelement.attrib["points"]

    def get_text(self) -> str:
        """ Get text from 'Unicode' sub-subelement (subelement of 'TextEquiv'). """

        for subelement in self.element.findall(".//{http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15}Unicode"):
            return subelement.text

    def extract_tags(self, tags: list[str] = None):
        """ Extract tags from TextLine.

         If not tags are specified, all tags are extracted.

         :param tags: tags to be extracted, defaults to None
         """
        unparsed = self.get_custom()
        result = unparsed.split(";}")
        """pattern = "\A[a-z].*[} ]"
        result = re.findall(pattern=pattern,
                            string=unparsed)"""

        print(result)






    def map_tag(self):
        """ Map tag coordinates to string"""
        pass

main(file_path=f"{TESTS}/data/input.xml")