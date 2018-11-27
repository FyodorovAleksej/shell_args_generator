import re

from shell_args_generator.arg_parser.AbstractParser import AbstractParser


class TitleParser(AbstractParser):
    def __init__(self, __start_expression: str):
        super().__init__()
        self.__START_EXPRESSION = re.compile(__start_expression)
        self.__DATA_EXPRESSION = re.compile(r"\((\d{2})[.:\-](\d{2})[.:\-](\d{4})\)")
        self.__TITLE_EXPRESSION = re.compile(r"(\[.+?\])")
        self.__DESCRIPTION_EXPRESSION = re.compile(r":\s*(\".+?\")")
        self.__AUTHOR_EXPRESSION = re.compile(r"(#.+)")

    def begin_with(self, __line: str) -> bool:
        return True if re.fullmatch(self.__START_EXPRESSION, __line) else False

    def parse_content(self, __text_lines: list) -> dict:
        text = ""
        for line in __text_lines:
            text += line
        return {"date": self.find_date_in_text(text),
                "title": self.find_title_in_text(text),
                "description": self.find_description_in_text(text),
                "author": self.find_author_in_text(text)}

    def find_date_in_text(self, __text: str):
        dates = re.search(self.__DATA_EXPRESSION, __text)
        if dates is not None and len(dates.groups()) >= 1:
            temp = dates[0]
            if temp is not None and len(temp) > 0:
                while temp.startswith("("):
                    temp = temp[1:]
            if temp is not None and len(temp) > 0:
                while temp.endswith(")"):
                    temp = temp[:-1]
            return temp
        return None

    def find_title_in_text(self, __text: str):
        titles = re.search(self.__TITLE_EXPRESSION, __text)
        if titles is not None and len(titles.groups()) >= 1:
            title = titles[0]
            if title is not None and len(title) > 0:
                while title.startswith("["):
                    title = title[1:]
            if title is not None and len(title) > 0:
                while title.endswith("]"):
                    title = title[:-1]
            return title
        return None

    def find_description_in_text(self, __text: str):
        descriptions = re.search(self.__DESCRIPTION_EXPRESSION, __text)
        if descriptions is not None and len(descriptions.groups()) >= 1:
            temp = descriptions[0]
            if temp is not None and len(temp) > 0:
                while temp.startswith(":") or temp.startswith(" ") or temp.startswith("\t"):
                    temp = temp[1:]
            if temp is not None and len(temp) > 0:
                while temp.startswith("\""):
                    temp = temp[1:]
            if temp is not None and len(temp) > 0:
                while temp.endswith("\""):
                    temp = temp[:-1]
            return temp
        return None

    def find_author_in_text(self, __text: str):
        authors = re.search(self.__AUTHOR_EXPRESSION, __text)
        if authors is not None and len(authors.groups()) >= 1:
            temp = authors[0]
            if temp is not None and len(temp) > 0:
                while temp.startswith("#"):
                    temp = temp[1:]
            if temp is not None and len(temp) > 0:
                while temp.startswith(" ") or temp.startswith("\t"):
                    temp = temp[1:]
            return temp
        return None
