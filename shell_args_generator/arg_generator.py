# -*- coding: utf-8 -*-

from configparser import ConfigParser

from shell_args_generator.ArgWrapper import ArgWrapper
from shell_args_generator.arg_builder.bash_builder.BashBuilder import BashBuilder
from shell_args_generator.arg_builder.java_builder.JavaBuilder import JavaBuilder
from shell_args_generator.arg_builder.man_builder.ManBuilder import ManBuilder
from shell_args_generator.arg_parser.ArgsParser import ArgsParser
from shell_args_generator.arg_parser.CommonParser import CommonParser
from shell_args_generator.arg_parser.HomeParser import HomeParser
from shell_args_generator.arg_parser.TitleParser import TitleParser


def wrap_pattern(__value: str) -> str:
    return "%" + __value + "%"


def read_and_wrap_config(__path: str, __section: str) -> dict:
    config_parser = ConfigParser()
    config_parser.read(__path)
    return {k: wrap_pattern(v) for k, v in dict(config_parser[__section]).items()}


class ArgGenerator:
    def __init__(self, parser_config: str, builder_config: str, input_path: str):
        self._parser_config = parser_config
        self._builder_config = builder_config
        self._input_path = input_path

        args_parser_config = read_and_wrap_config(self._parser_config, "ARGS_PARSER")
        home_parser_config = read_and_wrap_config(self._parser_config, "HOME_PARSER")
        title_parser_config = read_and_wrap_config(self._parser_config, "TITLE_PARSER")

        bash_builder_config = read_and_wrap_config(self._builder_config, "BASH")
        man_builder_config = read_and_wrap_config(self._builder_config, "MAN")
        java_builder_config = read_and_wrap_config(self._builder_config, "JAVA")

        common = CommonParser() \
            .append_parser(HomeParser(home_parser_config["home_parser_start_expression"])) \
            .append_parser(TitleParser(title_parser_config["title_parser_start_expression"])) \
            .append_parser(ArgsParser(args_parser_config["args_parser_start_expression"]))

        file = open(self._input_path)
        text = file.read()
        file.close()

        parsed = common.parse_all_text(text)
        wrapper = ArgWrapper(parsed)

        self._bashBuilder = BashBuilder(wrapper, "./shell_args_generator/resources/templates/bash/bashTemplate.sh",
                                  "./shell_args_generator/resources/templates/bash/bashCaseTemplate.sh", bash_builder_config)
        self._manBuilder = ManBuilder(wrapper, "./shell_args_generator/resources/templates/man/manTemplate.8",
                                "./shell_args_generator/resources/templates/man/manFlagTemplate.8", man_builder_config)
        self._javaBuilder = JavaBuilder(wrapper, "./shell_args_generator/resources/templates/java/javaTemplate.java",
                                  "./shell_args_generator/resources/templates/java/javaSetValues.java",
                                  "./shell_args_generator/resources/templates/java/javaSetOption.java",
                                  "./shell_args_generator/resources/templates/java/javaOption.java",
                                  "./shell_args_generator/resources/templates/java/javaGetOption.java",
                                  "./shell_args_generator/resources/templates/java/javaCheckOption.java", java_builder_config)

    def bash_generate(self):
        self._bashBuilder.generate_bash_to_file("./res.sh")

    def java_generate(self):
        self._javaBuilder.generate_java_to_file("./CommandLineManager.java")

    def man_generate(self):
        self._manBuilder.generate_man_to_file("./res.8")
