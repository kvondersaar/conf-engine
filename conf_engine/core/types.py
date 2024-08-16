from typing import Callable, Iterable, Union

class Type:
    def __init__(self, type_name: str = 'unknown type'):
        self.type_name = type_name

    def __call__(self, value):
        """
        Value is passed to the type object for the object to verify that the value
        matches the parameters defined for the type.
        :param value:
        :return:
        """
        return True

    def __eq__(self, other: 'Type'):
        return self.type_name == other.type_name


class Number(Type):
    CAST_OPTIONS = [int, float, complex]

    def __init__(self, minimum: Union[int, float] = None, maximum: Union[int, float] = None,
                 choices: Iterable = None, type_name: str = 'number type', cast: Callable = int):
        if minimum is not None and maximum is not None and maximum < minimum:
            raise ValueError("Minimum is greater than maximum.")
        if choices:
            invalid_choices = [x for x in choices if not self._is_number(x)]
            if invalid_choices:
                raise ValueError(f"Choices {invalid_choices} are not numeric.")

        if cast and cast not in self.CAST_OPTIONS:
            raise ValueError(f"Cast must be a numeric type {self.CAST_OPTIONS}")
        self._cast = cast
        self._minimum = minimum
        self._maximum = maximum
        self._choices = [self._cast(choice) for choice in choices] if choices else []
        super().__init__(type_name=type_name)

    def __call__(self, value):
        try:
            value = self._cast(value)
        except ValueError:
            raise ValueError(f"Value {value} is not correct type {self._cast}")
        if self._maximum and value > self._maximum:
            raise ValueError(f"Value {value} exceeds the maximum value of {self._maximum}")
        if self._minimum and value < self._minimum:
            raise ValueError(f"Value {value} is less than the minimum value of {self._minimum}")
        if self._choices and value not in self._choices:
            raise ValueError(f"Valid values are {self._choices}, but found {value}.")
        return value

    @staticmethod
    def _is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def _is_integer(value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def _is_number(value):
        return Number._is_integer(value) or Number._is_float(value)


class Integer(Number):
    def __init__(self, minimum: int = None, maximum: int = None,
                 choices: Iterable = None, type_name: str = 'number type',
                 cast: Callable = int):
        super().__init__(minimum=minimum, maximum=maximum, choices=choices, type_name='integer type', cast=cast)


class Float(Number):
    def __init__(self, minimum: int = None, maximum: int = None,
                 choices: Iterable = None, type_name: str = 'number type',
                 cast: Callable = float):
        super().__init__(minimum=minimum, maximum=maximum, choices=choices, type_name='float type', cast=cast)


class String(Type):
    def __init__(self, ignore_case: bool = False, max_length: int = None,
                 choices: Iterable = None, type_name: str = 'string type'):
        self._ignore_case = ignore_case
        self._max_length = max_length
        self._choices = [x.lower() for x in choices] or [] if ignore_case and choices else choices or []
        super().__init__(type_name=type_name)

    def __call__(self, value):
        value = value.lower() if self._ignore_case else value
        if self._max_length and len(value) > self._max_length:
            raise ValueError(f"Value {value} is longer than {self._max_length}.")
        if self._choices and value not in self._choices:
            raise ValueError(f"Valid values are {self._choices}, but found {value}.")
        return value


class Boolean(Type):
    TRUE = ['true', '1', 'on', 'yes']
    FALSE = ['false', '0', 'off', 'no']

    def __init__(self, type_name: str = 'boolean type'):
        super().__init__(type_name=type_name)

    def __call__(self, value):
        value = str(value)
        if isinstance(value, bool):
            return value
        if value.lower() in self.TRUE:
            return True
        if value.lower() in self.FALSE:
            return False

        raise ValueError(f"Unexpected boolean value: {value}.")
