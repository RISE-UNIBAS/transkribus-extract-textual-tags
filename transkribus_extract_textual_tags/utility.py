""" utility.py

Utility class. """

from transkribus_extract_textual_tags.tags import Tag
import csv


class Utility:
    """ Collection of utility methods. """

    @staticmethod
    def get_aggregated(tags: list[Tag]) -> dict:
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
    def get_csv_header(tag_names_parameters: dict):
        """ Get CSV header.

        :param tag_names_parameters: aggregated tag names and parameters
        """

        parameters = {}
        for parameter in tag_names_parameters.values():
            parameters.update(parameter)

        header = ["tag_name",
                  "tagged_string",
                  "continued_tagged_string",
                  "text_region_id",
                  "text_line_text",
                  "text_line_id",
                  "text_line_coords_points",
                  "text_line_baseline_points"]

        return header + list(parameters.keys())

    @staticmethod
    def write_csv(save_file_path: str,
                  tags: list[Tag]) -> None:
        """ bla

        :param save_file_path: the complete path to the save file (need not exist yet)
        :param tags: tags to be written
        """
        aggregated = Utility.get_aggregated(tags)
        header = Utility.get_csv_header(aggregated)

        with open(save_file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header)

            for tag in tags:
                print(tag.get_csv_serialization(header=header))
