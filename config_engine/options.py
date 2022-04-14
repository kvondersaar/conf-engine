from typing import Callable, Iterable, Union

import config_engine.types as t


class Option:
    def __init__(self, name, option_type: t.Type = None):
        self.name = name
        self.option_type = option_type if option_type else t.String()

    def __str__(self):
        return self.name

    def __call__(self, value):
        return self.option_type(value)


class StringOption(Option):
    def __init__(self, name, option_type: t.String = None, ignore_case: bool = False, max_length: int = None,
                 choices: Iterable = None, type_name: str = 'string type'):
        option_type = t.String(ignore_case=ignore_case, max_length=max_length, choices=choices, type_name=type_name)
        super().__init__(name, option_type=option_type)


class NumberOption(Option):
    def __init__(self, name, option_type: t.Number = None, minimum: Union[int, float] = None,
                 maximum: Union[int, float] = None, choices: Iterable = None,
                 type_name: str = 'number type', cast: Callable = int):
        option_type = t.Number(minimum=minimum, maximum=maximum, choices=choices, type_name=type_name, cast=cast)
        super().__init__(name, option_type=option_type)


class BooleanOption(Option):
    def __init__(self, name, option_type=t.Boolean()):
        super().__init__(name, option_type=option_type)
