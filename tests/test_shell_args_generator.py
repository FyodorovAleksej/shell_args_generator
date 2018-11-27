#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `shellargsgenerator` package."""

import pytest
from click.testing import CliRunner

from shell_args_generator import cli
from shell_args_generator.arg_parser.ArgsParser import ArgsParser
from shell_args_generator.arg_parser.CommonParser import CommonParser
from shell_args_generator.arg_parser.HomeParser import HomeParser
from shell_args_generator.arg_parser.TitleParser import TitleParser
from shell_args_generator.arg_parser.arg_entity.Argument import Argument


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string

def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0

class TestStringMethods:
    def setup_class(self):
        self.args_start = "%ARGS%"
        self.home_start = "%HOME%"
        self.title_start = "%TITLE%"

    def test_common(self):
        common = CommonParser() \
            .append_parser(HomeParser(self.home_start)) \
            .append_parser(TitleParser(self.title_start)) \
            .append_parser(ArgsParser(self.args_start))

        file = open("./shell_args_generator/resources/template.agf")
        text = file.read()
        file.close()

        actual = common.parse_all_text(text)

        args = [Argument().set_short_flag("-a").set_long_flag("--assert").add_option(
            ("String", "expression")).set_description("adding expression to assert"),
                Argument().set_short_flag("-h").set_long_flag("--help").set_description("print help message"),
                Argument().set_short_flag("-uf").set_long_flag("--userfile").add_option(
                    ("String", "path")).set_description("path to user file"),
                Argument().set_short_flag("-ui").set_long_flag("--userinput").add_option(
                    ("String", "user input format")).set_description("adding expression to assert"),
                Argument().set_short_flag("-mc").set_long_flag("--maxCount").add_option(
                    ("Integer", "user max count")).add_option(("String", "user")).set_description("max count of args")]

        # -a|--assert [<String> expression] : "adding expression to assert"
        # -h|--help : "print help message"
        # -uf|--userfile [<String> path] : "path to user file"
        # -ui|--userinput [<String> user input format] : "adding expression to assert"
        # -mc|--maxCount [<Integer> user max count, <String> user] : "max count of args"

        expect = {"level": "8", "name": "EXAMPLE", "version": "1.4.0", "date": "26.10.2018",
                  "title": "Shell Args Generator",
                  "description": "project of args generator", "author": "Fyodorov Alexey <Fyodorov.aleksej@gmail.com>",
                  "arguments": args}

        assert (expect == actual)

    def test_home_begin(self):
        parser = HomeParser(self.home_start)
        test = "%HOME%"
        assert (parser.begin_with(test))

    def test_home(self):
        parser = HomeParser(self.home_start)
        test = ["#8 [START] <1.4.4>"]
        expect = {"level": "8", "name": "START", "version": "1.4.4"}
        assert (parser.parse_content(test) == expect)

    def test_title_begin(self):
        parser = TitleParser(self.title_start)
        test = "%TITLE%"
        assert (parser.begin_with(test))

    def test_title_line(self):
        parser = TitleParser(self.title_start)
        test = ["(13.23.1998) [TITLE] : \"it\'s wonderful\" #Alexey Fyodorov<Fyodorov.aleksej@gmail.com>"]
        expect = {"date": "13.23.1998",
                  "title": "TITLE",
                  "description": "it's wonderful",
                  "author": "Alexey Fyodorov<Fyodorov.aleksej@gmail.com>"}
        assert (parser.parse_content(test) == expect)

    def test_args_begin(self):
        parser = ArgsParser(self.args_start)
        test = "%ARGS%"
        assert (parser.begin_with(test))

    def test_args_lines(self):
        parser = ArgsParser(self.args_start)
        test = ["-a|--assert [<String> expression] : \"adding expression to assert\"",
                "-h|--help : \"print help message\"",
                "-uf|--userfile [<String> path] : \"path to user file\""]

        a1 = Argument().set_short_flag("-a").set_long_flag("--assert").add_option(
            ("String", "expression")).set_description("adding expression to assert")
        a2 = Argument().set_short_flag("-h").set_long_flag("--help").set_description("print help message")
        a3 = Argument().set_short_flag("-uf").set_long_flag("--userfile").add_option(
            ("String", "path")).set_description("path to user file")
        expected = {"arguments": [a1, a2, a3]}
        dicts = parser.parse_content(test)
        assert (expected == dicts)
