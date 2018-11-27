from shell_args_generator.ArgWrapper import ArgWrapper
from shell_args_generator.arg_builder.common import read_template_from_file
from shell_args_generator.arg_parser.arg_entity.Argument import Argument


class BashBuilder:
    def __init__(self, __wrapper: ArgWrapper, __main_template_path: str, __case_template_path: str, __props):
        self.__TEMPLATE_BASH = read_template_from_file(__main_template_path)
        self.__TEMPLATE_CASE = read_template_from_file(__case_template_path)

        self.__FLAGS_PATTERN = __props["bash_template_flags_pattern"]
        self.__CASE_PATTERN = __props["bash_template_case_pattern"]
        self.__CASE_SHORT_FLAG = __props["bash_case_short_flag_pattern"]
        self.__CASE_LONG_FLAG = __props["bash_case_long_flag_pattern"]
        self.__CASE_LONG_NAME = __props["bash_case_long_name_pattern"]
        self.__CASE_FLAGS = __props["bash_case_flag_options_pattern"]
        self.__wrapper = __wrapper

    def generate_flags(self) -> str:
        res = ""
        arguments = self.__wrapper.get_arguments()
        for arg in arguments:
            assert isinstance(arg, Argument)
            base_name = self.transfer_to_name(arg.get_long_flag())
            options = arg.get_options()
            if len(options) == 0:
                res += base_name + "_flag=0\n"
            else:
                for option in range(0, len(options)):
                    res += base_name + "_arg_" + str(option) + "=\"\"\n"
        return res

    def generate_options(self, __argument: Argument) -> str:
        res = ""
        assert isinstance(__argument, Argument)
        base_name = self.transfer_to_name(__argument.get_long_flag())
        options = __argument.get_options()
        if len(options) == 0:
            res += base_name + "_flag=1\n"
        else:
            for option in range(0, len(options)):
                if option >= 1:
                    res += "\t"
                res += base_name + "_arg_" + str(option) + "=$2\n"
                res += "\tshift\n"
        res += "\t;;\n"
        return res

    def generate_case(self, argument: Argument) -> str:
        return self.__TEMPLATE_CASE.replace(self.__CASE_SHORT_FLAG, argument.get_short_flag()) \
            .replace(self.__CASE_LONG_FLAG, argument.get_long_flag()) \
            .replace(self.__CASE_LONG_NAME, self.transfer_to_name(argument.get_long_flag())) \
            .replace(self.__CASE_FLAGS, self.generate_options(argument))

    def generate_bash(self) -> str:
        cases = ""
        for arg in self.__wrapper.get_arguments():
            cases += self.generate_case(arg)
        return self.__TEMPLATE_BASH.replace(self.__FLAGS_PATTERN, self.generate_flags()) \
            .replace(self.__CASE_PATTERN, cases)

    def generate_bash_to_file(self, __output_file: str) -> None:
        file = open(__output_file, "w+")
        file.write(self.generate_bash())
        file.flush()
        file.close()

    @staticmethod
    def transfer_to_name(long_flag: str) -> str:
        temp = long_flag
        if temp is not None and len(temp) > 0:
            while temp.startswith("-"):
                temp = temp[1:]
        return temp
