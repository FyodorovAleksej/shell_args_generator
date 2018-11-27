class ArgWrapper:
    def __init__(self, __diction: dict):
        self.__level = None if "level" not in __diction.keys() else __diction["level"]
        self.__name = None if "name" not in __diction.keys() else __diction["name"]
        self.__version = None if "version" not in __diction.keys() else __diction["version"]
        self.__date = None if "date" not in __diction.keys() else __diction["date"]
        self.__title = None if "title" not in __diction.keys() else __diction["title"]
        self.__description = None if "description" not in __diction.keys() else __diction["description"]
        self.__author = None if "author" not in __diction.keys() else __diction["author"]
        self.__arguments = None if "arguments" not in __diction.keys() else __diction["arguments"]

    def get_level(self):
        return self.__level

    def get_name(self):
        return self.__name

    def get_version(self):
        return self.__version

    def get_date(self):
        return self.__date

    def get_title(self):
        return self.__title

    def get_description(self):
        return self.__description

    def get_author(self):
        return self.__author

    def get_arguments(self):
        return self.__arguments

    def __eq__(self, __other):
        """Overrides the default implementation"""
        if isinstance(__other, ArgWrapper):
            return self.__level == __other.__level \
                   and self.__date == __other.__date \
                   and self.__title == __other.__title \
                   and self.__description == __other.__description \
                   and self.__author == __other.__author \
                   and self.__arguments == __other.__arguments
        return False

    def __ne__(self, __other):
        return self.__eq__(__other)

    def __str__(self):
        return "<level = " + self.__level + ", " \
               + "date = " + self.__date + ", " \
               + "title = " + self.__title + ", " \
               + "description = " + self.__description + ", " \
               + "author = " + self.__author + ", " \
               + "arguments = " + self.__arguments + ">"

    def __repr__(self):
        return self.__str__()
