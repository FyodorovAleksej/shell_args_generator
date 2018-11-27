import re

from shell_args_generator.arg_parser.AbstractParser import AbstractParser
from shell_args_generator.arg_parser.arg_entity.Argument import Argument


class ArgsParser(AbstractParser):
    def __init__(self, __start_expression: str):
        super().__init__()
        self.__START_EXPRESSION = re.compile(__start_expression)
        self.__ARG_SHORT_EXPRESSION = re.compile(r"-(\w+)")
        self.__ARG_LONG_EXPRESSION = re.compile(r"--(\w+)")
        self.__OPTION_TYPE_EXPRESSION = re.compile(r"(<.+?>)")
        self.__ARG_OPTION_EXPRESSION = re.compile(r"(\[.+?\])")
        self.__ARG_DESCRIPTION_EXPRESSION = re.compile(r":(\s*)\".+?\"")

    def begin_with(self, __line: str) -> bool:
        return True if re.fullmatch(self.__START_EXPRESSION, __line) else False

    def parse_content(self, __text_lines: list) -> dict:
        arguments = []
        for line in __text_lines:
            arg = Argument()

            arg.set_short_flag(self.find_short_in_line(line))
            arg.set_long_flag(self.find_long_in_line(line))
            arg.add_option_list(self.find_options_in_line(line))
            arg.set_description(self.find_description_in_line(line))
            arguments.append(arg)
        return {"arguments": arguments}

    def find_short_in_line(self, __line: str):
        shorts = re.search(self.__ARG_SHORT_EXPRESSION, __line)
        if shorts is not None and len(shorts.groups()) >= 1:
            return shorts.group(0)  # [0]
        return None

    def find_long_in_line(self, __line: str):
        longs = re.search(self.__ARG_LONG_EXPRESSION, __line)
        if longs is not None and len(longs.groups()) >= 1:
            return longs.group(0)  # [0]
        return None

    def find_options_in_line(self, __line: str):
        options_list = []
        options = re.search(self.__ARG_OPTION_EXPRESSION, __line)
        if options is not None and len(options.groups()) >= 1:
            options_line = options.group(0)  # [0]
            options_parts = options_line.split(",")
            for part in options_parts:
                types = re.search(self.__OPTION_TYPE_EXPRESSION, part)
                if types is not None and len(options.groups()) >= 1:
                    temp = types.group(0)  # [0]
                    raw_type = temp
                    if temp is not None and len(temp) > 0:
                        while temp.startswith("<"):
                            temp = temp[1:]
                    if temp is not None and len(temp) > 0:
                        while temp.endswith(">"):
                            temp = temp[:-1]

                    if len(part) > len(raw_type):
                        description = part[(len(raw_type) + 1):]
                        if description is not None and len(description) > 0:
                            while description.startswith(" ") or description.startswith("\t"):
                                description = description[1:]
                        if description is not None and len(description) > 0:
                            while description.endswith("]"):
                                description = description[:-1]

                        options_list.append((temp, description))
                    else:
                        options_list.append((temp, None))
                else:
                    options_list.append((None, part))
        return options_list

    def find_description_in_line(self, __line: str):
        descriptions = re.search(self.__ARG_DESCRIPTION_EXPRESSION, __line)
        if descriptions is not None and len(descriptions.groups()) >= 1:
            temp = descriptions.group(0)  # [0]
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
