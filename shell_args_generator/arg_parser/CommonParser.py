from shell_args_generator.arg_parser.AbstractParser import AbstractParser


class CommonParser:
    def __init__(self):
        self.__parsers = []

    def append_parser(self, __parser: AbstractParser):
        self.__parsers.append(__parser)
        return self

    def parse_all_text(self, __text: str) -> dict:
        result = {}
        current_text_lines = []
        current_parser = None

        flag = False
        lines = __text.splitlines(keepends=False)
        for line in lines:
            if line is not None and len(line) > 0:
                while line.startswith(' '):
                    line = line[1:]
            if line is not None and len(line) > 0:
                while line.endswith(' '):
                    line = line[:-1]
            for parser in self.__parsers:
                if parser.begin_with(line):
                    flag = True
                    if current_parser is None:
                        current_parser = parser
                    else:
                        result.update(current_parser.parse_content(current_text_lines))
                        current_parser = parser
                        current_text_lines.clear()
            if not flag:
                current_text_lines.append(line)
            flag = False
        result.update(current_parser.parse_content(current_text_lines))
        return result
