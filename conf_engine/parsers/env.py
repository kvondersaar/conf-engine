import os

from conf_engine.exceptions import ValueNotFound


class EnvironmentParser:
    def get_option_value(self, option: str, group: str = None):
        env_name = option.upper() if not group else group.upper() + '_' + option.upper()
        value = os.getenv(env_name)
        if value:
            return value
        else:
            raise ValueNotFound(option)


