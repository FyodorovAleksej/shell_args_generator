class Argument:
    def __init__(self):
        self.__short_flag = None
        self.__long_flag = None
        self.__options = []
        self.__description = None

    def __str__(self):
        return "<short_flag = " + self.__short_flag + ", " + \
               "long_flag = " + self.__long_flag + ", " + \
               "options = " + str(self.__options) + ", " + \
               "description = " + self.__description + ">"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, __other):
        """Overrides the default implementation"""
        if isinstance(__other, Argument):
            return self.__short_flag == __other.__short_flag \
                   and self.__long_flag == __other.__long_flag \
                   and self.__options == __other.__options \
                   and self.__description == __other.__description
        return False

    def __ne__(self, __other):
        return not self.__eq__(__other)

    def set_short_flag(self, __value: str):
        self.__short_flag = __value
        return self

    def set_long_flag(self, __value: str):
        self.__long_flag = __value
        return self

    def add_option(self, __value: tuple):
        self.__options.append(__value)
        return self

    def add_option_list(self, options: list):
        for option in options:
            self.__options.append(option)
        return self

    def set_description(self, __value: str):
        self.__description = __value
        return self

    def get_short_flag(self) -> str:
        return self.__short_flag

    def get_long_flag(self) -> str:
        return self.__long_flag

    def get_options(self) -> list:
        return self.__options

    def get_description(self) -> str:
        return self.__description
