import abc


class AbstractParser:

    @abc.abstractmethod
    def begin_with(self, __line: str) -> bool:
        pass

    @abc.abstractmethod
    def parse_content(self, __text_lines: list) -> dict:
        pass
