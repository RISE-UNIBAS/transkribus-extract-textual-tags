""" main.py

"""

from __future__ import annotations
from dataclasses import dataclass, InitVar
from lxml import etree
from typing import List, Optional

import csv
import os.path
import re

DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
TESTS = f"{PARENT_DIR}/TESTS"


@dataclass
class Document:
    """ A representation of a Transkribus PAGE XML document. """

    file_path: InitVar[str]
    tree: etree._Element = None

    def __post_init__(self, file_path):
        if self.tree is None:
            self.tree = etree.parse(file_path)

    def get_text_regions(self):
        """ Get all 'TextRegion' elements of the document. """

        return [TextRegion(element=element) for element in
                self.tree.findall(".//{http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15}TextRegion")]

    def get_tags(self) -> List[Optional[Tag]]:
        """ Get all textual tags from the document. """

        tags = []
        for text_region in self.get_text_regions():
            for text_line in text_region.get_text_lines():
                for tag in text_line.get_tags():
                    try:
                        # continued tags come in pairs:
                        if "continued" in tags[-1].get_parameters().keys() and tag.get_name() == tags[-1].get_name():
                            continued_tagged_string = tags[-1].get_tagged_string(tags[-1].text_line_text) + " " + tag.get_tagged_string(text_line.get_text())
                            tags[-1].set_continued_tagged_string(continued_tagged_string)
                            continue  # skip second tag of such a pair
                    except IndexError:
                        pass
                    tag.text_line_text = text_line.get_text()
                    tag.text_region_id = text_region.get_id()
                    tag.text_line_id = text_line.get_id()
                    tag.text_line_coords_points = text_line.get_coords_points()
                    tag.text_line_baseline_points = text_line.get_baseline_points()
                    tags.append(tag)

        return tags


# TODO: subclass TextRegion and TextLine
'''@dataclass
class Text:
    """ bla """
    
    element: etree._Element

    def get_id(self) -> str:
        """ Get 'id' attribute. """

        return self.element.attrib["id"]'''


@dataclass
class TextRegion:
    """ A representation of a Transkribus PAGE XML 'TextRegion' element. """

    element: etree._Element

    def get_id(self) -> str:
        """ Get 'id' attribute. """

        return self.element.attrib["id"]

    def get_text_lines(self):
        """ Get all 'TextLine' elements of the document. """

        return [TextLine(element=element) for element in
                self.element.findall(".//{http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15}TextLine")]


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
    text_line_text: str = None
    text_region_id: str = None
    text_line_id: str = None
    text_line_coords_points: str = None
    text_line_baseline_points: str = None
    continued_tagged_string: str = None

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

    def set_continued_tagged_string(self,
                                    continued_tagged_string: str):
        """ Set combined tagged string.

        A continued tagged string is the concatenation of two tagged strings if the tags have parameter
        'continued' both set to 'true' and are adjacent in the PAGE XML document.

        :param continued_tagged_string: the combined tagged string
        """

        self.continued_tagged_string = continued_tagged_string


class Client:
    """ bla """

    @staticmethod
    def extract_from_file(file_path: str) -> None:
        """ Extract tags from file with Transkribus PAGE XML documents.

        :param file_path:
        """

        pass

    @staticmethod
    def extract_from_dir(dir_path: str) -> None:
        """ Extract tags from directory with Transkribus PAGE XML documents.

        :param dir_path: the complete path to the directory
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

        aggregated = Client.get_aggregated(tags)
        header = Client.get_header(aggregated)

        # todo: write to csv here
        for tag in tags:
            print(tag)

    @staticmethod
    def get_aggregated(tags: List[Tag]):
        """ Get aggregated parameters per tag.

        :param tags: the tags
        """

        aggregated = dict()
        for tag in tags:
            try:
                aggregated[tag.get_name()].update(tag.get_parameters())
            except KeyError:
                aggregated[tag.get_name()] = tag.get_parameters()

        return aggregated

    @staticmethod
    def get_header(tag_names_parameters: dict):
        """ Get header.

        :param tag_names_parameters: aggregated tag names and parameters
        """

        parameters = {}
        for parameter in tag_names_parameters.values():
            parameters.update(parameter)

        main = ["tag_name",
                "tagged_string",
                "continued_tagged_string"]

        meta = ["text_line_text",
                "text_region_id",
                "text_line_id",
                "text_line_coords_points",
                "text_line_baseline_points"]

        return main + list(parameters.keys()) + meta


Client.extract_from_dir(dir_path=f"{TESTS}/data/")
