import re

from shell_args_generator import ArgWrapper
from shell_args_generator.arg_builder.common import read_template_from_file
from shell_args_generator.arg_parser.arg_entity.Argument import Argument


class ManBuilder:
    def __init__(self, __wrapper: ArgWrapper, __main_template_path: str, __option_template_path: str, __props: dict):
        self.__TEMPLATE_MAN = read_template_from_file(__main_template_path)
        self.__TEMPLATE_OPTION = read_template_from_file(__option_template_path)

        self.__TITLE_PATTERN = __props["man_template_title_pattern"]
        self.__LEVEL_PATTERN = __props["man_template_level_pattern"]
        self.__NAME_PATTERN = __props["man_template_name_pattern"]
        self.__VERSION_PATTERN = __props["man_template_version_pattern"]
        self.__DATE_PATTERN = __props["man_template_date_pattern"]
        self.__DESCRIPTION_PATTERN = __props["man_template_description_pattern"]
        self.__AUTHOR_PATTERN = __props["man_template_author_pattern"]

        self.__FLAGS = __props["man_template_flags_pattern"]

        self.__OPTION_SHORT_FLAG = __props["man_option_flag_short_pattern"]
        self.__OPTION_LONG_FLAG = __props["man_option_flag_long_pattern"]
        self.__OPTION_USAGE = __props["man_option_flag_usage_pattern"]
        self.__OPTION_DESCRIPTION = __props["man_option_flag_description_pattern"]

        self.__wrapper = __wrapper

    @staticmethod
    def generate_usage(__argument: Argument) -> str:
        options = __argument.get_options()
        res = ""
        if options is not None:
            if len(options) == 1:
                res += "[<" + options[0][0] + "> " + options[0][1] + "]"
            elif len(options) > 1:
                temp = []
                res += "["
                for option in options:
                    temp.append("<" + option[0] + "> " + option[1])
                res += ", ".join(temp) + "]"
        return res

    @staticmethod
    def generate_date(__date: str) -> str:
        parts = re.split("[.:\-]", __date)

        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                  'August', 'September', 'October', 'November', 'December']
        months = [x.upper() for x in months]
        res = ""
        if len(parts) == 3:
            res += parts[0] + "\ \&" + months[int(parts[1]) - 1] + "\ \&" + parts[2]
        return res

    def generate_option(self, __argument: Argument) -> str:
        return self.__TEMPLATE_OPTION.replace(self.__OPTION_SHORT_FLAG, __argument.get_short_flag()) \
            .replace(self.__OPTION_LONG_FLAG, __argument.get_long_flag()) \
            .replace(self.__OPTION_USAGE, self.generate_usage(__argument)) \
            .replace(self.__OPTION_DESCRIPTION, __argument.get_description())

    def generate_man(self) -> str:
        options = ""
        for arg in self.__wrapper.get_arguments():
            options += self.generate_option(arg)
        return self.__TEMPLATE_MAN \
            .replace(self.__TITLE_PATTERN, self.__wrapper.get_title()) \
            .replace(self.__LEVEL_PATTERN, self.__wrapper.get_level()) \
            .replace(self.__NAME_PATTERN, self.__wrapper.get_name()) \
            .replace(self.__VERSION_PATTERN, self.__wrapper.get_version()) \
            .replace(self.__DATE_PATTERN, self.generate_date(self.__wrapper.get_date())) \
            .replace(self.__DESCRIPTION_PATTERN, self.__wrapper.get_description()) \
            .replace(self.__AUTHOR_PATTERN, self.__wrapper.get_author()) \
            .replace(self.__FLAGS, options)

    def generate_man_to_file(self, __output_file):
        file = open(__output_file, "w+")
        file.write(self.generate_man())
        file.flush()
        file.close()
