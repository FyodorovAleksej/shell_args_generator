import re

from shell_args_generator import ArgWrapper
from shell_args_generator.arg_builder.AbstractBuilderHandler import AbstractBuilderHandler


class ManDateHandler(AbstractBuilderHandler):
    def __init__(self, __handle_pattern: str, __props: dict):
        super().__init__(__handle_pattern, __props)
        self.__months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                         'August', 'September', 'October', 'November', 'December']

    def replace_pattern(self, __wrapper: ArgWrapper):
        parts = re.split("[.:\-]", __wrapper.get_date())
        months = [x.upper() for x in self.__months]
        res = ""
        if len(parts) == 3:
            res += parts[0] + "\ \&" + months[int(parts[1]) - 1] + "\ \&" + parts[2]
        return res
