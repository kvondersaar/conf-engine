import sys

from conf_engine.core.exceptions import ValueNotFound
from conf_engine.options import Option, BooleanOption

class CLIParser:
    def __init__(self, namespace: str = None, **kwargs):
        """
        :param namespace: Defines the namespace to be prepended to the CLI
        option name.
        """
        self.namespace = namespace.lower() if namespace else None

    def get_option_value(self, option: Option, group: str = None):
        # Append group name.
        opt_name = option.name if not group else f'{group}-{option.name}'
        opt_name = opt_name if not self.namespace else f'{self.namespace}-{opt_name}'
        opt_name = f'--{opt_name.replace('_', '-').lower()}'

        is_boolean = isinstance(option, BooleanOption)
        is_flag = is_boolean and option.flag
        try:
            idx = sys.argv.index(opt_name)
            # If it's a boolean option and the flag is present, we return True regardless of
            # any following values.
            if is_boolean and is_flag:
                return True
            # If there's no data after
            if len(sys.argv) < idx+1:
                raise ValueNotFound(option.name)
            return sys.argv[idx+1]

        # Catch ValueError if sys.argv.index() cannot find our option.
        except ValueError as e:
            # If it's a boolean option, and flag is set, then we return False when it's not present.
            if is_boolean and is_flag:
                return False
            # Otherwise we didn't find the option at all.
            raise ValueNotFound(option.name)
        except IndexError as e:
            raise ValueNotFound(option.name)