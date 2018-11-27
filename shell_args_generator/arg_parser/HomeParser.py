import re

from shell_args_generator.arg_parser.AbstractParser import AbstractParser


class HomeParser(AbstractParser):
    def __init__(self, __start_expression: str):
        super().__init__()
        self.__START_EXPRESSION = re.compile(__start_expression)
        self.__LEVEL_EXPRESSION = re.compile(r"(#(\d+))")
        self.__NAME_EXPRESSION = re.compile(r"(\[.+?\])")
        self.__VERSION_EXPRESSION = re.compile(r"(<.+?>)")

    def begin_with(self, __text: str) -> bool:
        return True if re.fullmatch(self.__START_EXPRESSION, __text) else False

    def parse_content(self, __text_lines: list) -> dict:
        text = ""
        for line in __text_lines:
            text += line
        return {"level": self.find_level_in_text(text),
                "name": self.find_name_in_text(text),
                "version": self.find_version_in_text(text)}

    def find_level_in_text(self, __text: str):
        levels = re.search(self.__LEVEL_EXPRESSION, __text)
        if levels is not None and len(levels.groups()) >= 1:
            temp = levels.group(0)  # [0]
            if temp is not None and len(temp) > 0:
                while temp.startswith("#") or temp.startswith(" ") or temp.startswith("\t"):
                    temp = temp[1:]
            if temp is not None and len(temp) > 0:
                while temp.endswith(" ") or temp.endswith("\t"):
                    temp = temp[:-1]
            return temp
        return None

    def find_name_in_text(self, __text: str):
        names = re.search(self.__NAME_EXPRESSION, __text)
        if names is not None and len(names.groups()) >= 1:
            temp = names.group(0)  # [0]
            if temp is not None and len(temp) > 0:
                while temp.startswith("[") or temp.startswith(" ") or temp.startswith("\t"):
                    temp = temp[1:]
            if temp is not None and len(temp) > 0:
                while temp.endswith("]") or temp.endswith(" ") or temp.endswith("\t"):
                    temp = temp[:-1]
            return temp
        return None

    def find_version_in_text(self, __text: str):
        versions = re.search(self.__VERSION_EXPRESSION, __text)
        if versions is not None and len(versions.groups()) >= 1:
            temp = versions.group(0)  # [0]
            if temp is not None and len(temp) > 0:
                while temp.startswith("<") or temp.startswith(" ") or temp.startswith("\t"):
                    temp = temp[1:]
            if temp is not None and len(temp) > 0:
                while temp.endswith(">") or temp.endswith(" ") or temp.endswith("\t"):
                    temp = temp[:-1]
            return temp
        return None
