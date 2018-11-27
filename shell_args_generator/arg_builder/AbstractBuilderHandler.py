import abc


class AbstractBuilderHandler:
    def __init__(self, __handle_pattern: str, __props: dict, __template: str = None, __child_handlers: list = None):
        self.handle_pattern = __handle_pattern
        self.template = __template
        self.child_handlers = __child_handlers
        self.props = __props

    def get_handle_pattern(self) -> str:
        return self.handle_pattern

    def get_template(self) -> str:
        return self.template

    def get_child_handlers(self) -> list:
        return self.child_handlers

    def get_props(self) -> dict:
        return self.props

    @abc.abstractmethod
    def replace_pattern(self, __object) -> str:
        return ""

    def replace_text(self, __object) -> str:
        temp = self.template
        if self.child_handlers is not None and len(self.child_handlers) > 0:
            for child in self.child_handlers:
                temp = child.replace_text(__object, temp)
        return temp.replace(self.handle_pattern, self.replace_pattern(__object))
