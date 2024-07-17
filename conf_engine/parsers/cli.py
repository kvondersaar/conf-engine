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

        try:
            idx = sys.argv.index(opt_name)
            if isinstance(option, BooleanOption):
                return True if idx else False

            return sys.argv.index(idx+1)
        except ValueError as e:
            raise ValueNotFound(option.name)
        except Exception as e:
            raise e
