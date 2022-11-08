""" main.py

"""

from __future__ import annotations
from dataclasses import dataclass
from lxml import etree
from typing import List, Optional

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
        print(text_line.get_reading_order())
        print(text_line.get_tags())
        for tag in text_line.get_tags():
            print(tag.get_name())
            print(tag.get_parameters())
            print(tag.get_tagged_string(text=text_line.get_text()))
        print("-" * 20)


@dataclass
class TextLine:
    """ A representation of a Transkribus PAGE XML 'TextLine' element. """

    element: etree._Element

    def get_id(self) -> str:
        """ Get 'id' attribute. """

        return self.element.attrib["id"]

    def get_custom(self) -> str:
        """ Get 'custom' attribute. """

        return self.element.attrib["custom"]

    def get_coords_points(self) -> str:
        """ Get 'points' attribute from 'Coords' subelement. """

        for subelement in self.element.findall(
                ".//{http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15}Coords"):
            return subelement.attrib["points"]

    def get_baseline_points(self) -> str:
        """ Get 'points' attribute from 'Baseline' subelement. """

        for subelement in self.element.findall(
                ".//{http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15}Baseline"):
            return subelement.attrib["points"]

    def get_text(self) -> str:
        """ Get text from 'Unicode' sub-subelement (subelement of 'TextEquiv'). """

        for subelement in self.element.findall(
                ".//{http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15}Unicode"):
            return subelement.text

    def get_reading_order(self) -> int:
        """ Get reading order. """

        return int(re.search(pattern="\d+",
                             string=self.get_custom().split(";}")[0] + ";}").group())

    def get_tags(self) -> List[Optional[Tag]]:
        """ Get textual tags. """

        return [Tag(item.strip() + "}") for item in self.get_custom().split(";}")][1:-1]


@dataclass
class Tag:
    """ A representation of a Transkribus textual tag. """

    raw: str

    def get_name(self) -> str:
        """ Get the tag name. """

        return self.raw.split(" ")[0]

    def get_parameters(self) -> dict:
        """ Get dictionary of tag's parameters (offset, length, continued, and other custom ones). """

        return {item.strip().split(":")[0]: item.strip().split(":")[1] for item in self.raw.split(self.get_name())[1].strip()[1:-1].split(";")}

    def get_tagged_string(self,
                          text: str) -> str:
        """ Get the tagged string.

        :param text: the text"""

        offset = int(self.get_parameters()["offset"])
        length = int(self.get_parameters()["length"])

        return text[offset:offset + length]


main(file_path=f"{TESTS}/data/1.xml")