from typing import Callable, Iterable, Union

import conf_engine.core.types as t


class _UndefinedDefault:
    """An object that represents a default that is not defined.  Should not be
    used outside the Config Engine module itself."""
    pass


UNDEFINED = _UndefinedDefault()


class Option:
    """
    CLass representing an option to be registered with the Configuration object.
    All Options have a subset of shared properties, name, default, type, etc.
    Inheriting classes may implement additional kwargs as appropriate to their type.
    When a default is set it will be validated using the option_type specified.
    """

    def __init__(self, name, option_type: t.Type = None, default: any = UNDEFINED):
        self.name = name
        self.option_type = option_type if option_type else t.String()
        self.default = default
        if default is not UNDEFINED:
            try:
                option_type(default)
            except ValueError as e:
                raise e

    def __str__(self):
        return self.name

    def __call__(self, value):
        return self.option_type(value)

    def __eq__(self, other: 'Option'):
        return self.name == other.name and self.option_type == other.option_type


class StringOption(Option):
    def __init__(self, *args, option_type: t.String = None, ignore_case: bool = False, max_length: int = None,
                 choices: Iterable = None, type_name: str = 'string type', **kwargs):
        if not option_type:
            kwargs['option_type'] = t.String(ignore_case=ignore_case, max_length=max_length, choices=choices,
                                             type_name=type_name)
        super().__init__(*args, **kwargs)


class NumberOption(Option):
    def __init__(self, *args, option_type: t.Number = None, minimum: Union[int, float] = None,
                 maximum: Union[int, float] = None, choices: Iterable = None,
                 type_name: str = 'number type', cast: Callable = int, **kwargs):
        if not option_type:
            kwargs['option_type'] = t.Number(minimum=minimum, maximum=maximum,
                                             choices=choices, type_name=type_name, cast=cast)
        super().__init__(*args, **kwargs)


class BooleanOption(Option):
    def __init__(self, *args, option_type=t.Boolean(), flag: bool = False, **kwargs):
        kwargs['option_type'] = option_type
        self.flag = flag
        super().__init__(*args, **kwargs)
