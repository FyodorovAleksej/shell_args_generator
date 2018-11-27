from shell_args_generator.arg_builder.AbstractBuilderHandler import AbstractBuilderHandler
from shell_args_generator.arg_parser.arg_entity import Argument


class ManUsageHandler(AbstractBuilderHandler):
    def __init__(self, __handle_pattern: str, __props: dict):
        super().__init__(__handle_pattern, __props)

    def replace_pattern(self, __argument: Argument):
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
