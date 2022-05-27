import logging

import conf_engine.exceptions as cfg_exc
import conf_engine.parsers as parsers

from conf_engine.options import Option

REGISTERED_PARSERS = [
    parsers.EnvironmentParser,
    parsers.INIFileParser,
]


class ConfigGroup:
    def __init__(self, name):
        """
        A collection of related configuration options.
        :param name:
        """
        self._name = name
        self._opt_cache = {}

    def __getattr__(self, item: str):
        return self._get_option(item)

    def __contains__(self, item):
        return item in self._opt_cache

    def _get_option(self, option: str):
        if option in self._opt_cache:
            return self._get_option_value(self._opt_cache[option], self._name)
        raise cfg_exc.UnregisteredOption(option)

    @staticmethod
    def _get_option_value(option: Option, group):
        value = None
        value_found = False
        for parser in REGISTERED_PARSERS:
            try:
                value = parser().get_option_value(option.name, group)
                value = option.option_type(value)
                # The first parser in registered parsers list
                # should take precedence, so we return early.
                return value
            except cfg_exc.ValueNotFound:
                continue
            except Exception as e:
                logging.exception(e)
                raise e

        if option.default is not None:
            return option.option_type(option.default)
        # If we get here, then we've not found the value.
        raise cfg_exc.ValueNotFound(option.name)

    def register_options(self, options: [Option]):
        for option in options:
            self.register_option(option)

    def register_option(self, option: Option):
        if option.name in self._opt_cache and option != self._opt_cache[option.name]:
            raise cfg_exc.DuplicateOptionError(option.name)
        self._opt_cache[option.name] = option


class Configuration:
    def __init__(self):
        """
        Configuration object that represents the configuration of the application.
        """
        self._group_cache = {None: ConfigGroup(None)}

    def __getattr__(self, item):
        return self._get_group(item)

    def __contains__(self, item):
        return item in self._group_cache

    def register_options(self, options: [Option], group: str = None):
        """
        Register bulk options with the config.
        :param options: List of options.
        :param group: Group name to which options are added.
        :return:
        """

        for option in options:
            self.register_option(option, group=group)

    def register_option(self, option: Option, group: str = None, create_group: bool = True):
        """
        Register options with the config.  If group is specified, the options are
        added to the option group, otherwise options are registered to the base object.
        :param option: Option to register.
        :param group: Group name to which the option is added.
        :param create_group: Create the group if not already registered.
        :return:
        """
        if group and group not in self._group_cache:
            if create_group:
                self._group_cache[group] = ConfigGroup(group)
            else:
                raise cfg_exc.UnregisteredGroup(group)
        self._group_cache[group].register_option(option)

    @property
    def registered_parsers(self):
        return self._registered_parsers

    def _get_group(self, group: str):
        """
        Get group by its name as called during attribute access against the
        configuration object.  If the option cannot be found an UnregisteredOption
        error will be raised.

        If the option matches a group name, the group object is returned and the
        subsequent attribute access is handled by the group object.

        :param group:
        :return:
        """
        # If we find the option name in our cache, that means what was passed to
        # __getattr__() is the group value.  We return that and have the group object
        # perform the call to _get_option_value().  Otherwise, we return the default
        # group object

        if group in self._group_cache:
            return self._group_cache[group]
        else:
            return getattr(self._group_cache[None], group)
