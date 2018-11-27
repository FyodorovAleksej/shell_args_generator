from shell_args_generator.ArgWrapper import ArgWrapper
from shell_args_generator.arg_builder.common import read_template_from_file
from shell_args_generator.arg_parser.arg_entity import Argument


class JavaBuilder:
    def __init__(self, __wrapper: ArgWrapper, __template_path: str, __set_values_path: str,
                 __set_options_path: str, __option_path: str, __get_option_path: str, __check_option_path: str,
                 __props: dict):
        self.__java_template = read_template_from_file(__template_path)
        self.__java_template_options_pattern = __props["java_template_options_pattern"]
        self.__java_template_parameters_pattern = __props["java_template_parameters_pattern"]
        self.__java_template_title_pattern = __props["java_template_title_pattern"]
        self.__java_template_create_options_pattern = __props["java_template_create_options_pattern"]
        self.__java_template_set_arguments_pattern = __props["java_template_set_arguments_pattern"]
        self.__java_template_add_options_pattern = __props["java_template_add_options_pattern"]
        self.__java_template_check_options_pattern = __props["java_template_check_options_pattern"]
        self.__java_template_set_values_pattern = __props["java_template_set_options_pattern"]
        self.__java_template_options_getters_pattern = __props["java_template_options_getters_pattern"]
        self.__java_template_description_pattern = __props["java_template_description_pattern"]
        self.__java_template_author_pattern = __props["java_template_author_pattern"]
        self.__java_template_version_pattern = __props["java_template_version_pattern"]

        self.__java_set_values_template = read_template_from_file(__set_values_path)
        self.__java_set_values_arg_name_pattern = __props["java_set_values_arg_name_pattern"]
        self.__java_set_values_option_name_pattern = __props["java_set_values_option_name_pattern"]
        self.__java_set_values_wrapper_pattern = __props["java_set_values_wrapper_pattern"]
        self.__java_set_values_wrapper_end_pattern = __props["java_set_values_wrapper_end_pattern"]

        self.__java_set_options_template = read_template_from_file(__set_options_path)
        self.__java_set_options_option_name_pattern = __props["java_set_options_option_name_pattern"]
        self.__java_set_options_arguments_count_pattern = __props["java_set_options_arguments_count_pattern"]
        self.__java_set_options_argument_description_pattern = __props["java_set_options_argument_description_pattern"]

        self.__java_option_template = read_template_from_file(__option_path)
        self.__java_option_option_name_pattern = __props["java_option_option_name_pattern"]
        self.__java_option_short_flag_pattern = __props["java_option_short_flag_pattern"]
        self.__java_option_long_flag_pattern = __props["java_option_long_flag_pattern"]
        self.__java_option_description_pattern = __props["java_option_description_pattern"]

        self.__java_get_option_template = read_template_from_file(__get_option_path)
        self.__java_get_option_arg_description_pattern = __props["java_get_option_arg_description_pattern"]
        self.__java_get_option_arg_name_pattern = __props["java_get_option_arg_name_pattern"]

        self.__java_check_option_template = read_template_from_file(__check_option_path)
        self.__java_check_option_option_name_pattern = __props["java_check_option_option_name_pattern"]
        self.__java_check_option_option_description_pattern = __props["java_check_option_option_description_pattern"]

        self.__wrapper = __wrapper

    @staticmethod
    def to_option_long_name(__argument: Argument) -> str:
        temp = __argument.get_long_flag()
        if temp is not None and len(temp) > 0:
            while temp.startswith("-"):
                temp = temp[1:]
        return temp

    @staticmethod
    def to_arg_name(__index: int, __arg_name: str) -> str:
        return __arg_name + "arg_" + str(__index)

    @staticmethod
    def to_creating_arg_name(__option: tuple, __index: int, __arg_name: str) -> str:
        return "private " + __option[0] + " " + __arg_name + "arg_" + str(__index) + ";\n"

    @staticmethod
    def to_wrapper(__option: tuple) -> str:
        if __option is not None:
            option_type = __option[0]
            if option_type == "String":
                return ""
            elif option_type == "Integer":
                return "Integer.valueOf("
            elif option_type == "Long":
                return "Long.valueOf("
            elif option_type == "Float":
                return "Float.valueOf("
            elif option_type == "Double":
                return "Double.valueOf("
            elif option_type == "Boolean":
                return "Boolean.valueOf("
        return ""

    def generate_options(self, __arguments: list) -> str:
        res = ""
        if __arguments is not None:
            for arg in __arguments:
                long_name = self.to_option_long_name(arg)
                res += "private Option " + long_name + "Option;\n"
        return res

    def generate_arguments(self, __arguments: list) -> str:
        res = ""
        if __arguments is not None:
            for arg in __arguments:
                options = arg.get_options()
                if options is not None:
                    if len(options) == 0:
                        res += "private boolean is" + self.to_option_long_name(arg) + ";\n"
                    else:
                        cur = 0
                        for option in options:
                            res += self.to_creating_arg_name(option, cur, self.to_option_long_name(arg))
                            cur += 1
        return res

    def generate_creating_options(self, __arguments: list):
        res = ""
        if __arguments is not None:
            for arg in __arguments:
                long_name = self.to_option_long_name(arg) + "Option"
                res += self.__java_option_template \
                    .replace(self.__java_option_option_name_pattern, long_name) \
                    .replace(self.__java_option_short_flag_pattern, "\"" + arg.get_short_flag()[1:] + "\"") \
                    .replace(self.__java_option_long_flag_pattern, "\"" + arg.get_long_flag()[2:] + "\"") \
                    .replace(self.__java_option_description_pattern, "\"" + arg.get_description() + "\"")
        return res

    def generate_setting_options(self, __arguments: list):
        res = ""
        if __arguments is not None:
            for arg in __arguments:
                options = arg.get_options()
                if options is not None:
                    if len(options) == 0:
                        pass
                    else:
                        cur = 0
                        for option in options:
                            res += self.__java_set_options_template \
                                .replace(self.__java_set_options_option_name_pattern,
                                         self.to_option_long_name(arg) + "Option") \
                                .replace(self.__java_set_options_arguments_count_pattern, str(len(options))) \
                                .replace(self.__java_set_options_argument_description_pattern, option[1])
                            cur += 1
        return res

    def generate_adding_options(self, __arguments: list):
        res = ""
        if __arguments is not None:
            for arg in __arguments:
                long_name = self.to_option_long_name(arg)
                res += "options.addOption(" + long_name + "Option);\n"
        return res

    def generate_checking_options(self, __arguments: list):
        res = ""
        if __arguments is not None:
            for arg in __arguments:
                options = arg.get_options()
                if options is not None:
                    if len(options) == 0:
                        pass
                    else:
                        cur = 0
                        for option in options:
                            res += self.__java_check_option_template \
                                .replace(self.__java_check_option_option_name_pattern,
                                         self.to_option_long_name(arg) + "Option") \
                                .replace(self.__java_check_option_option_description_pattern, option[1])
                            cur += 1
        return res

    def generate_setting_values(self, __arguments: list):
        res = ""
        if __arguments is not None:
            for arg in __arguments:
                options = arg.get_options()
                if options is not None:
                    if len(options) == 0:
                        pass
                    else:
                        cur = 0
                        for option in options:
                            wrapper = self.to_wrapper(option)
                            if wrapper == "":
                                res += self.__java_set_values_template \
                                    .replace(self.__java_set_values_arg_name_pattern,
                                             self.to_arg_name(cur, self.to_option_long_name(arg))) \
                                    .replace(self.__java_set_values_wrapper_pattern, wrapper) \
                                    .replace(self.__java_set_values_wrapper_end_pattern, "") \
                                    .replace(self.__java_set_values_option_name_pattern,
                                             self.to_option_long_name(arg) + "Option")
                            else:
                                res += self.__java_set_values_template \
                                    .replace(self.__java_set_values_arg_name_pattern,
                                             self.to_arg_name(cur, self.to_option_long_name(arg))) \
                                    .replace(self.__java_set_values_wrapper_pattern, wrapper) \
                                    .replace(self.__java_set_values_wrapper_end_pattern, ")") \
                                    .replace(self.__java_set_values_option_name_pattern,
                                             self.to_option_long_name(arg) + "Option")
                            cur += 1
        return res

    def generate_getters(self, __arguments: list):
        res = ""
        if __arguments is not None:
            for arg in __arguments:
                options = arg.get_options()
                if options is not None:
                    if len(options) == 0:
                        pass
                    else:
                        cur = 0
                        for option in options:
                            res += self.__java_get_option_template \
                                .replace(self.__java_get_option_arg_description_pattern, option[1]) \
                                .replace(self.__java_get_option_arg_name_pattern,
                                         self.to_arg_name(cur, self.to_option_long_name(arg)))
                            cur += 1
        return res

    def generate_java(self) -> str:
        return self.__java_template \
            .replace(self.__java_template_options_pattern, self.generate_options(self.__wrapper.get_arguments())) \
            .replace(self.__java_template_parameters_pattern, self.generate_arguments(self.__wrapper.get_arguments())) \
            .replace(self.__java_template_create_options_pattern,
                     self.generate_creating_options(self.__wrapper.get_arguments())) \
            .replace(self.__java_template_set_arguments_pattern,
                     self.generate_setting_options(self.__wrapper.get_arguments())) \
            .replace(self.__java_template_add_options_pattern,
                     self.generate_adding_options(self.__wrapper.get_arguments())) \
            .replace(self.__java_template_check_options_pattern,
                     self.generate_checking_options(self.__wrapper.get_arguments())) \
            .replace(self.__java_template_set_values_pattern,
                     self.generate_setting_values(self.__wrapper.get_arguments())) \
            .replace(self.__java_template_options_getters_pattern,
                     self.generate_getters(self.__wrapper.get_arguments())) \
            .replace(self.__java_template_title_pattern, self.__wrapper.get_title()) \
            .replace(self.__java_template_description_pattern, self.__wrapper.get_description()) \
            .replace(self.__java_template_author_pattern, self.__wrapper.get_author()) \
            .replace(self.__java_template_version_pattern, self.__wrapper.get_version())

    def generate_java_to_file(self, __output_file):
        file = open(__output_file, "w+")
        file.write(self.generate_java())
        file.flush()
        file.close()
