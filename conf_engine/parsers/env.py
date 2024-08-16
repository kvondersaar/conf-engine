import os

from conf_engine.core.exceptions import ValueNotFound
from conf_engine.options import Option

class EnvironmentParser:
    def __init__(self, namespace: str = None, **kwargs):
        """
        :param namespace: Defines the namespace to be prepended when
            doing an ENV var lookup.
        """
        self.namespace = namespace.upper() if namespace else None

    def get_option_value(self, option: Option, group: str = None):
        # Replace group hypens with underscores.
        group = group.replace('-', '_') if group else None
        # Append group name.
        env_name = option.name.upper() if not group else group.upper() + '_' + option.name.upper()
        # Append namespace.
        env_name = env_name if not self.namespace else self.namespace + '_' + env_name
        value = os.getenv(env_name)
        if value:
            return value
        else:
            raise ValueNotFound(option)


