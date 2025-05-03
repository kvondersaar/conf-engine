import re
import sys

from conf_engine.core.exceptions import ValueNotFound
from conf_engine.options import Option, BooleanOption

class CLIParser:
    def __init__(self, namespace: str = None, **kwargs):
        """
        The CLI parser handles collection of options from arguments passed on the command line.  All option names
        are prepended with the conventional double hyphen `--` and the value follows. The equal sign is optional.
        All options are converted to lower, and all underscores replaced with hyphens.  Namespaces
        and groups are likewise separated from the option name by hyphens.  Any hyphens (or converted underscores)
        present in the namespace or group names will remain.  For example an option names "my_opt" in "example"
        would be identified by `--example-my-opt`

        The `BooleanOption` has special handing rules when utilizing the CLI parser.  If the `BooleanOption` is
        created with `flag` set to True, then it will parse the CLI looking for the option as a flag, and not
        attempt to parse any subsequent values.  If the flag is found, then the option value is `True`.
        Likewise if the option is missing then `False` is returned.  Note that this can short circuit a lookup
        by subsequent parsers in the parser chain.

        :param namespace: Defines the namespace to be prepended to the CLI
        option name.
        """
        self.namespace = namespace.lower() if namespace else None

    def get_option_value(self, option: Option, group: str = None):
        # Append group name.
        opt_name = option.name if not group else f'{group}-{option.name}'
        opt_name = opt_name if not self.namespace else f'{self.namespace}-{opt_name}'
        opt_name = f"--{opt_name.replace('_', '-').lower()}"

        is_present, value = self._parse_argv(opt_name)

        is_boolean = isinstance(option, BooleanOption)
        is_flag = is_boolean and getattr(option, 'flag')

        if is_boolean and is_flag:
            return is_present
        if value:
            return value

        raise ValueNotFound(option.name)
    @staticmethod
    def _parse_argv(opt_name: str):
        """
        Parse the value of sys.argv and return a tuple indicating if the option
        is present, and it's value.
        """

        opt_regex = fr"{opt_name}([ =]|$)"
        val_regex = fr"{opt_name}[ =](?P<value>\S*)"
        pattern = ' '.join(sys.argv)

        is_present = True if re.search(opt_regex, pattern) else False
        value = None

        val_match = re.search(val_regex, ' '.join(sys.argv))
        if val_match:
            is_present = True
            value = val_match.group('value')

        return is_present, value


