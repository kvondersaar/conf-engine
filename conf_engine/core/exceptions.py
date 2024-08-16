class ConfigError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class UnregisteredOption(ConfigError):
    def __str__(self):
        return f"No option is registered with name: {self.message}"

class UnregisteredGroup(ConfigError):
    def __str__(self):
        return f"No group is registered with name: {self.message}"


class DuplicateOptionError(ConfigError):
    def __str__(self):
        return f"Option or group is already registered: {self.message}"


class ValueNotFound(ConfigError):
    def __str__(self):
        return f"Could not find a value for {self.message}."