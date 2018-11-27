# -*- coding: utf-8 -*-

"""Console script for shellargsgenerator."""
import sys

import click

from shell_args_generator.arg_generator import ArgGenerator


@click.command()
@click.option('--parserConfig', '-pc', default="./shell_args_generator/resources/config/parser/parser_config.ini",
              help='path to parser config.')
@click.option('--builderConfig', '-bc', default="./shell_args_generator/resources/config/builder/builder_config.ini",
              help='path to builder config.')
@click.option('--input', '-i', default="./shell_args_generator/resources/template.agf", help='path to input .agf file')
@click.option('--java', '-j', is_flag=True)
@click.option('--bash', '-sh', is_flag=True)
@click.option('--man', '-m', is_flag=True)
def main(parserconfig, builderconfig, input, java, bash, man):
    parser = ArgGenerator(parserconfig, builderconfig, input)
    if java:
        parser.java_generate()
        print("java class generated")
    if bash:
        parser.bash_generate()
        print("bash script generated")
    if man:
        parser.man_generate()
        print("man page generated")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
